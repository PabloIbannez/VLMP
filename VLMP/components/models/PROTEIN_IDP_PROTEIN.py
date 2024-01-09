import sys, os

import json

import copy

import logging

import numpy as np
from scipy.spatial.transform import Rotation as R

from scipy.spatial import KDTree

from ..types import basic

from . import modelBase

from . import IDP # intrinsic disorder protein model
from . import ENM # protein model

import pyUAMMD

class PROTEIN_IDP_PROTEIN(modelBase):
    """
    Component name: PROTEIN_IDP_PROTEIN
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 02/01/2024

    Intrinsic disorder protein model merged with protein model (ENM)

    Reference: https://journals.aps.org/pre/pdf/10.1103/PhysRevE.90.042709

    """
    def __loadProtein(self,name,PDB,types,PRTN_types):

        typesPDB = basic(name="PDB_types",units= self.getUnits())

        prot = ENM.ENM(name = name + "_PRTN",
                       units = self.getUnits(),
                       types = typesPDB,
                       ensemble = self.getEnsemble(),
                       PDB = PDB)

        state      = prot.getState()
        structure  = prot.getStructure()
        forcefield = prot.getForceField()

        structure_str = json.dumps(structure)

        # Rename all keys in forcefield adding the suffix "_PRTN"
        forcefield = {key + "_PRTN":value for key,value in forcefield.items()}
        forcefield_str = json.dumps(forcefield)

        # Rename all types in typesPDB adding the suffix "_PRTN"
        for _,t in typesPDB.getTypes().items():
            newName = t["name"] + "_PRTN"
            structure_str = structure_str.replace(t["name"],newName)
            forcefield_str = forcefield_str.replace(t["name"],newName)
            t["name"] = newName
            PRTN_types.add(newName)
            types.addType(**t)

        structure = json.loads(structure_str)
        forcefield = json.loads(forcefield_str)

        # Iterate over forcefield each non-bonded interaction, now acts on typeGroup2
        for key,value in forcefield.items():
            entryType,_ = value["type"]
            if entryType == "NonBonded":
                forcefield[key]["parameters"]["condition"] = "typeGroup2Intra"

        protSim = pyUAMMD.simulation({"state":state, "topology":{ "structure":structure, "forceField":forcefield}})

        return copy.deepcopy(protSim)

    def __addConnection(self,forceField,ids_conn_start,ids_conn_end):

        # 0-1 2-3

        # bonds: 2-3
        bonds = [[ids_conn_start[1],ids_conn_end[0]]]

        # angles: 0-1-2 1-2-3
        angles = [[ids_conn_start[0],ids_conn_start[1],ids_conn_end[0]],
                  [ids_conn_start[1],ids_conn_end[0],ids_conn_end[1]]]

        # dihedrals: 0-1-2-3
        dihedrals = [[ids_conn_start[0],ids_conn_start[1],ids_conn_end[0],ids_conn_end[1]]]

        exclusions = {}
        for i in ids_conn_start + ids_conn_end:
            exclusions[i] = []

        exclusions[bonds[0][0]].extend([bonds[0][1]])
        exclusions[bonds[0][1]].extend([bonds[0][0]])

        exclusions[angles[0][0]].extend([angles[0][1],angles[0][2]])
        exclusions[angles[0][1]].extend([angles[0][0],angles[0][2]])
        exclusions[angles[0][2]].extend([angles[0][0],angles[0][1]])

        exclusions[angles[1][0]].extend([angles[1][1],angles[1][2]])
        exclusions[angles[1][1]].extend([angles[1][0],angles[1][2]])
        exclusions[angles[1][2]].extend([angles[1][0],angles[1][1]])

        #exclusions[dihedrals[0][0]].extend([dihedrals[0][1],dihedrals[0][2],dihedrals[0][3]])
        #exclusions[dihedrals[0][1]].extend([dihedrals[0][0],dihedrals[0][2],dihedrals[0][3]])
        #exclusions[dihedrals[0][2]].extend([dihedrals[0][0],dihedrals[0][1],dihedrals[0][3]])
        #exclusions[dihedrals[0][3]].extend([dihedrals[0][0],dihedrals[0][1],dihedrals[0][2]])

        ##############################################################

        addBonds     = False
        addAngles    = False
        addDihedrals = False
        for entry in forceField:
            if forceField[entry]["type"][0] == "Bond2":
                if "IDP" in entry:
                    forceField[entry]["data"].extend(bonds)
                    addBonds = True
            elif forceField[entry]["type"][0] == "Bond3":
                if "IDP" in entry:
                    forceField[entry]["data"].extend(angles)
                    addAngles = True
            elif forceField[entry]["type"][0] == "Bond4":
                if "IDP" in entry:
                    forceField[entry]["data"].extend(dihedrals)
                    addDihedrals = True

        if not addBonds:
            self.logger.error("No Bond2 IDP entry found in forcefield")
            raise RuntimeError("Entry not found")
        if not addAngles:
            self.logger.error("No Bond3 IDP entry found in forcefield")
            raise RuntimeError("Entry not found")
        if not addDihedrals:
            self.logger.error("No Bond4 IDP entry found in forcefield")
            raise RuntimeError("Entry not found")

        nlIdIndex     = forceField["nl"]["labels"].index("id")
        nlIdListIndex = forceField["nl"]["labels"].index("id_list")

        for k in exclusions:
            found = False
            for excl in forceField["nl"]["data"]:
                if k == excl[nlIdIndex]:
                    excl[nlIdListIndex].extend(exclusions[k])
                    excl[nlIdListIndex] = list(set(excl[nlIdListIndex]))
                    found = True
                    break
            if not found:
                forceField["nl"]["data"].append([k,exclusions[k]])

    def __fixProteinPos(self,sim,IDPids,PDBids,modeIDP,modePDB,maxTries):

        positionsIndex = sim["state"]["labels"].index("position")

        IDPpositions = []
        for i in IDPids:
            IDPpositions.append(sim["state"]["data"][i][positionsIndex])

        PDBpositions = []
        for i in PDBids:
            PDBpositions.append(sim["state"]["data"][i][positionsIndex])

        dstIDP = np.array(IDPpositions[1]) - np.array(IDPpositions[0])
        dstIDP = np.linalg.norm(dstIDP)

        if modeIDP == "start":
            idp_sel_pos = np.array(IDPpositions[0])  + np.asarray([0,0,-dstIDP])
        elif modeIDP == "end":
            idp_sel_pos = np.array(IDPpositions[-1]) + np.asarray([0,0, dstIDP])
        else:
            self.logger.error("Mode not recognized")
            raise RuntimeError("Mode not implemented")

        if modePDB == "start":
            pdb_sel_pos = np.array(PDBpositions[0])
            ignoreIndex = 0
        elif modePDB == "end":
            pdb_sel_pos = np.array(PDBpositions[-1])
            ignoreIndex = len(PDBpositions) - 1
        else:
            self.logger.error("Mode not recognized")
            raise RuntimeError("Mode not implemented")

        translation = pdb_sel_pos - idp_sel_pos

        # Translate protein positions
        for i in range(len(PDBpositions)):
            PDBpositions[i] = np.array(PDBpositions[i]) - translation

        center = idp_sel_pos

        # We rotate randomly the protein, the center of rotation is the selected position
        # Then we compute the minimal distance between protein and IDP.
        # We use KDTree

        tree = KDTree(IDPpositions)

        cTry    = 0
        overlap = True
        self.logger.debug("Fixing protein position ...")

        while overlap:

            if cTry >= maxTries:
                self.logger.error("Max tries reached")
                raise RuntimeError("Max tries reached")

            if cTry == 0:
                pass
            else:
                rotation = R.random()

                for i in range(len(PDBpositions)):
                    PDBpositions[i] = rotation.apply(PDBpositions[i] - center) + center

            overlap = False
            for i, point in enumerate(PDBpositions):
                distance, index = tree.query(point)
                # Check if the distance is within the threshold
                if distance < dstIDP*1.01 and i != ignoreIndex:
                    overlap = True
                    break

            cTry += 1
            self.logger.debug(f"Try {cTry}/{maxTries} ...")

        for i,index in enumerate(PDBids):
            sim["state"]["data"][index][positionsIndex] = PDBpositions[i].tolist()


    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"sequence",
                                                "PDB1","PDB2",
                                                "PDB1_conn","PDB2_conn",
                                                "cutOffVerletFactor"},
                         requiredParameters  = {"sequence"},
                         definedSelections   = {"particleId"},
                         **params)

        maxTries = 1000

        seq  = params["sequence"]

        PDB1 = params.get("PDB1",None)
        PDB2 = params.get("PDB2",None)

        cutOffVerletFactor = params.get("cutOffVerletFactor",1.1)

        if PDB1 is not None:
            PDB1_conn = params.get("PDB1_conn","end")
            if PDB1_conn not in ["end","start"]:
                self.logger.error("PDB1 connection must be either 'end' or 'start'")
                raise Exception("Error in input parameters")

        if PDB2 is not None:
            PDB2_conn = params.get("PDB2_conn","end")
            if PDB2_conn not in ["end","start"]:
                self.logger.error("PDB2 connection must be either 'end' or 'start'")
                raise Exception("Error in input parameters")

        if "PDB1_conn" in params and "PDB1" not in params:
            self.logger.error("PDB1 connection defined but not PDB1")
            raise Exception("Error in input parameters")

        if "PDB2_conn" in params and "PDB2" not in params:
            self.logger.error("PDB2 connection defined but not PDB2")
            raise Exception("Error in input parameters")

        types = self.getTypes()

        IDP_types  = set()
        PRTN_types = set()

        # IDP

        typesIDP = basic(name="IDP_types",units= self.getUnits())

        idp = IDP(name = name + "_IDP",
                  units = self.getUnits(),
                  types = typesIDP,
                  ensemble = self.getEnsemble(),
                  sequence = seq)

        state      = idp.getState()
        structure  = idp.getStructure()
        forcefield = idp.getForceField()

        structure_str = json.dumps(structure)

        # Rename all keys in forcefield adding the suffix "_IDP"
        forcefield = {key + "_IDP":value for key,value in forcefield.items()}
        forcefield_str = json.dumps(forcefield)

        # Rename all types in typesIDP adding the suffix "_IDP"
        for _,t in typesIDP.getTypes().items():
            newName = t["name"] + "_IDP"
            structure_str  = structure_str.replace(t["name"],newName)
            forcefield_str = forcefield_str.replace(t["name"],newName)
            t["name"] = newName
            IDP_types.add(newName)
            types.addType(**t)

        structure  = json.loads(structure_str)
        forcefield = json.loads(forcefield_str)

        # Iterate over forcefield each non-bonded interaction, now acts on typeGroup1
        for key,value in forcefield.items():
            entryType,_ = value["type"]
            if entryType == "NonBonded":
                forcefield[key]["parameters"]["condition"] = "typeGroup1Intra"

        sim = pyUAMMD.simulation({"state":state, "topology":{ "structure":structure, "forceField":forcefield}})

        IDP_len = sim.getNumberOfParticles()

        ############################################################

        # PROT1
        if PDB1 is not None:
            prot1Sim = self.__loadProtein(name,PDB1,types,PRTN_types)

        # PROT2
        if PDB2 is not None:
            prot2Sim = self.__loadProtein(name,PDB2,types,PRTN_types)

        ############################################################

        # Merge three simulations

        if PDB1 is not None:
            sim.append(prot1Sim,mode = "modelId")
        if PDB2 is not None:
            sim.append(prot2Sim,mode = "modelId")

        forceField = copy.deepcopy(sim["topology"]["forceField"])

        # Remove all neighbor lists
        labels = ["id","id_list"]
        data   = []

        entriesToRemove = []
        for entry in forceField:
            entryType,_ = forceField[entry]["type"]
            if entryType == "VerletConditionalListSet":

                cutOffVerletFactor = min(cutOffVerletFactor,forceField[entry]["parameters"]["cutOffVerletFactor"])
                data += forceField[entry]["data"]

                entriesToRemove.append(entry)

        for entry in entriesToRemove:
            del forceField[entry]

        forceField["nl"] = {}
        forceField["nl"]["type"]       = ["VerletConditionalListSet","nonExclTypeGroup1Intra_nonExclTypeGroup2Intra_nonExclInter_nonExclNoGroup"]
        forceField["nl"]["parameters"] = {"cutOffVerletFactor":cutOffVerletFactor,
                                          "typeGroup1":sorted(list(IDP_types)),
                                          "typeGroup2":sorted(list(PRTN_types))}

        forceField["nl"]["labels"]     = labels
        forceField["nl"]["data"]       = data

        ############################################################
        # Add connections between IDP and PROT

        IDP_start = [0,1]
        IDP_end   = [IDP_len-2,IDP_len-1]

        # <Prot1> ------- <IDP> ------- <Prot2>

        IDPids    = [i for i in range(IDP_len)]

        if PDB1 is not None:

            PDB1len = prot1Sim.getNumberOfParticles()-1 # Since id starts at 0
            if PDB1_conn == "start":
                ids     = [IDP_len+1,IDP_len]
            else:
                # PDB1_conn == "end"
                ids     = [IDP_len+PDB1len-1,IDP_len+PDB1len]

            self.__addConnection(forceField,ids,IDP_start)
            PDBids = [i for i in range(IDP_len, IDP_len+PDB1len+1)]
            self.__fixProteinPos(sim,IDPids,PDBids,"start",PDB1_conn,maxTries)

            PDB1offset = IDP_len+PDB1len+1
        else:
            PDB1offset = IDP_len

        if PDB2 is not None:

            PDB2len = prot2Sim.getNumberOfParticles()-1
            if PDB2_conn == "start":
                ids     = [PDB1offset,PDB1offset+1]
            else:
                # PDB2_conn == "end"
                ids     = [PDB1offset+PDB2len,PDB1offset+PDB2len-1]

            self.__addConnection(forceField,IDP_end,ids)
            PDBids = [i for i in range(PDB1offset, PDB1offset+PDB2len+1)]
            self.__fixProteinPos(sim,IDPids,PDBids,"end",PDB2_conn,maxTries)

        ############################################################

        self.setState(copy.deepcopy(sim["state"]))
        self.setStructure(copy.deepcopy(sim["topology"]["structure"]))
        self.setForceField(copy.deepcopy(forceField))

    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel
