from VLMP.components.models import modelBase

import os

import json

import numpy as np
import icosphere

class ICOSPHERE(modelBase):
    """
    Component name: ICOSPHERE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 18/06/2023

    Icosphere model
    """

    def __loadData(self,name):

        try:

            with open(self.modelData,"r") as f:
                data = json.load(f)
        except:
            self.logger.warning("[ICOSPHERE] Error opening model data from {} (loading)".format(self.modelData))
            return None

        try:
            d = data[str(self.resolution)][name].copy()
        except:
            self.logger.warning("[ICOSPHERE] Error loading {} from model data".format(name))
            return None

        return d

    def __saveToData(self,d,name):

        try:
            with open(self.modelData,"r") as f:
                data = json.load(f)
        except:
            self.logger.warning("[ICOSPHERE] Error opening model data from {} (saving)".format(self.modelData))
            return

        try:
            if str(self.resolution) not in data:
                data[str(self.resolution)] = {}
            data[str(self.resolution)][name] = d.copy()

            with open(self.modelData,"w") as f:
                json.dump(data,f)
        except:
            self.logger.warning("[ICOSPHERE] Error saving model data to {}".format(self.modelData))
            return

        return

    def __generateBonds(self,faces):

        bonds = self.__loadData("bonds")

        if bonds is None:
            bonds = set()
            for face in faces:
                bonds.add(tuple(sorted([int(face[0]),int(face[1])])))
                bonds.add(tuple(sorted([int(face[1]),int(face[2])])))
                bonds.add(tuple(sorted([int(face[2]),int(face[0])])))
            bonds = list(bonds)

            self.__saveToData(bonds,"bonds")

        return bonds.copy()

    def __generateDihedrals(self,faces):

        dihedrals = self.__loadData("dihedrals")

        if dihedrals is None:

            dihedrals = []

            # List all pairs of faces that share an edge
            facesPairs = set()
            for i in range(len(faces)):
                for j in range(i+1,len(faces)):
                    if len(set(faces[i]).intersection(set(faces[j]))) == 2:
                        facesPairs.add((i,j))

            for facePair in facesPairs:
                face1 = faces[facePair[0]]
                face2 = faces[facePair[1]]

                common = set(face1).intersection(set(face2))

                if len(common) == 2:
                    face1Id = list(set(face1).difference(common))[0]
                    face2Id = list(set(face2).difference(common))[0]

                    i = int(face1Id)
                    j = int(common.pop())
                    k = int(common.pop())
                    l = int(face2Id)

                    dihedrals.append([i,j,k,l])
                else:
                    self.log("Faces do not share an edge, faces: {} {}".format(face1,face2))
                    raise Exception("Faces do not share an edge")

            self.__saveToData(dihedrals,"dihedrals")

        return dihedrals.copy()

    def __generateExclusions(self,bonds):

        exclusions = self.__loadData("exclusions")

        if exclusions is None:

            exclusionsTmp = {}

            for bnd in bonds:
                i,j = bnd
                exclusionsTmp[i] = []
                exclusionsTmp[j] = []
            for bnd in bonds:
                i,j = bnd
                exclusionsTmp[i].append(j)
                exclusionsTmp[j].append(i)

            exclusionsTmp = {i:sorted(list(set(data))) for i,data in exclusionsTmp.items()}

            exclusions = []
            for i,excl in exclusionsTmp.items():
                exclusions.append([i,excl.copy()])

            #Sort according i
            exclusions = sorted(exclusions,key=lambda x: x[0])

            self.__saveToData(exclusions,"exclusions")

        return exclusions.copy()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"particleName",
                                                "particleMass","particleRadius","particleCharge",
                                                "position",
                                                "resolution",
                                                "radius",
                                                "Kb",
                                                "Kd",
                                                "steric"},
                         requiredParameters  = {"particleName"},
                         definedSelections   = {"particleId"},
                         **params)

        ############################################################

        self.modelData = "./data/ICOSPHERE.json"
        self.modelData = os.path.join(os.path.dirname(os.path.realpath(__file__)),self.modelData)

        ############################################################

        particleName = params["particleName"]

        particleMass   = params.get("particleMass",1.0)
        particleRadius = params.get("particleRadius",1.0)
        particleCharge = params.get("particleCharge",0.0)

        types = self.getTypes()
        types.addType(name = particleName,
                      mass = particleMass,
                      radius = particleRadius,
                      charge = particleCharge)

        position = params.get("position",np.array([0.0,0.0,0.0]))

        self.resolution = params.get("resolution",1)
        radius          = params.get("radius",1.0)

        Kb = params.get("Kb",1.0)
        Kd = params.get("Kd",0.0)

        steric = params.get("steric",False)

        ############################################################

        vertices,faces = icosphere.icosphere(nu = self.resolution)

        #Update the vertices
        for i in range(len(vertices)):
            vertices[i] = radius*vertices[i]+position

        state = {}
        state["labels"] = ["id","position"]

        state["data"] = []
        for i,vertex in enumerate(vertices):
            x,y,z = vertex
            state["data"].append([i,[x,y,z]])

        structure = {}
        structure["labels"] = ["id","type"]

        structure["data"] = []
        for i,face in enumerate(vertices):
            structure["data"].append([i,particleName])

        forceField = {}

        forceField["bonds"] = {}
        forceField["bonds"]["type"]       = ["Bond2","Harmonic"]
        forceField["bonds"]["labels"]     = ["id_i","id_j","r0","K"]
        forceField["bonds"]["parameters"] = {}
        forceField["bonds"]["data"]       = []

        bonds = self.__generateBonds(faces)

        for bond in bonds:
            dst = np.linalg.norm(vertices[bond[0]]-vertices[bond[1]])
            forceField["bonds"]["data"].append([bond[0],bond[1],dst,Kb])

        if Kd > 0.0:

            forceField["dihedrals"] = {}
            forceField["dihedrals"]["type"]       = ["Bond4","Dihedral"]
            forceField["dihedrals"]["labels"]     = ["id_i","id_j","id_k","id_l","phi0","K","n"]
            forceField["dihedrals"]["parameters"] = {}
            forceField["dihedrals"]["data"]       = []

            dihedrals = self.__generateDihedrals(faces)

            for dihedral in dihedrals:
                i,j,k,l = dihedral
                forceField["dihedrals"]["data"].append([i,j,k,l,0.0,Kd,1])

        if steric:

            exclusions = self.__generateExclusions(bonds)

            forceField["verletList"] = {}
            forceField["verletList"]["type"]       = ["VerletConditionalListSet", "nonExclIntra_nonExclInter"]
            forceField["verletList"]["parameters"] = {"cutOffVerletFactor":1.2}
            forceField["verletList"]["labels"]     = ["id","id_list"]
            forceField["verletList"]["data"]       = []

            for i,excl in exclusions:
                forceField["verletList"]["data"].append([i,excl])

            forceField["steric"] = {}
            forceField["steric"]["type"] = ["NonBonded", "WCAType2"]
            forceField["steric"]["parameters"] = {"cutOffFactor": 2.5,"condition":"intra"}
            forceField["steric"]["labels"] = ["name_i", "name_j", "epsilon", "sigma"]
            forceField["steric"]["data"]   = []

            forceField["steric"]["data"].append([particleName,particleName,1.0,pow(2.0,1.0/6.0)*particleRadius])

        ############################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel

