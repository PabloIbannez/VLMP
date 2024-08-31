import sys, os

import copy

import logging

from . import modelBase
from ...utils.input import getLabelIndex

class MEMBRANE(modelBase):
    """
    {
    "warning": "This model is currently under development. Please, use it with caution.",
    }
    """

    availableParameters = {"position"}
    requiredParameters  = set()
    definedSelections   = {"particleId"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        ############################################################
        ######################  Set up model  ######################
        ############################################################

        # Now only POPC is implemented
        sigmaT = 7.111
        sigmaH = 0.65*sigmaT

        eps = 0.416
        w   = 9.867

        spacing  = sigmaT*0.1
        zSpacing = sigmaT*0.0

        lipidLen = 2.0*sigmaT + 3.0*spacing

        # Bond coefficients for POPC
        kH1_H2_POPC = 2.0*0.446
        kH2_T1_POPC = 2.0*1.073
        kT1_T2_POPC = 2.0*1.001
        kT2_T3_POPC = 2.0*0.443

        # Bond lengths for POPC
        b0_H1_H2_POPC = 5.580
        b0_H2_T1_POPC = 5.452
        b0_T1_T2_POPC = 5.050
        b0_T2_T3_POPC = 5.095

        # Angle coefficients for POPC
        kH1_H2_T1_POPC = 2.0*0.600
        kH2_T1_T2_POPC = 2.0*2.383
        kT1_T2_T3_POPC = 2.0*0.880

        # Angle equilibrium values for POPC
        theta0_H1_H2_T1_POPC = 3.142
        theta0_H2_T1_T2_POPC = 3.142
        theta0_T1_T2_T3_POPC = 3.142

        ########################################################

        types = self.getTypes()

        types.addType(name="POPC_H1",radius=sigmaH/2.0,charge=0.0,mass=100.0)
        types.addType(name="POPC_H2",radius=sigmaH/2.0,charge=0.0,mass=100.0)
        types.addType(name="POPC_T1",radius=sigmaT/2.0,charge=0.0,mass=100.0)
        types.addType(name="POPC_T2",radius=sigmaT/2.0,charge=0.0,mass=100.0)
        types.addType(name="POPC_T3",radius=sigmaT/2.0,charge=0.0,mass=100.0)

        box = self.getEnsemble().getEnsembleComponent("box")

        # Create the membrane
        nLipidsX = box[0]/(sigmaT+spacing)
        nLipidsY = box[1]/(sigmaT+spacing)

        N = nLipidsX*nLipidsY

        # Create the lipids
        dx = sigmaT + spacing
        dy = sigmaT + spacing

        lipid = ["POPC_T3","POPC_T2","POPC_T1","POPC_H2","POPC_H1"]

        lipidZ = [0.0]*len(lipid)
        lipidZ[0] = sigmaT/2.0 + zSpacing
        lipidZ[1] = lipidZ[0] + b0_H2_T1_POPC
        lipidZ[2] = lipidZ[1] + b0_T1_T2_POPC
        lipidZ[3] = lipidZ[2] + b0_T2_T3_POPC
        lipidZ[4] = lipidZ[3] + b0_T2_T3_POPC

        #Generate state
        state = {}
        state["labels"] = ["id","position"]
        state["data"]   = []

        #Generate structure
        structure = {}
        structure["labels"] = ["id","type","modelId"]
        structure["data"]   = []

        forceField = {}
        forceField["bond"] = {}
        forceField["bond"]["type"]       = ["Bond2", "Harmonic"]
        forceField["bond"]["labels"]     = ["id_i", "id_j", "K", "r0"]
        forceField["bond"]["data"]       = []

        forceField["angle"] = {}
        forceField["angle"]["type"]       = ["Bond3", "HarmonicAngular"]
        forceField["angle"]["labels"]     = ["id_i", "id_j", "id_k", "K", "theta0"]
        forceField["angle"]["data"]       = []


        index = 0
        lipidId = 0
        for i in range(int(nLipidsX)):
            for j in range(int(nLipidsY)):

                for leaflet in range(2):

                    for k,t in enumerate(lipid):
                        # The last tail particles is placed at z = sigmaT/2.0+zSpacing
                        x = i*dx + dx/2.0 - box[0]/2.0
                        y = j*dy + dy/2.0 - box[1]/2.0
                        if leaflet == 0: # Upper leaflet
                            z =   lipidZ[k]
                        else: # Lower leaflet
                            z = - lipidZ[k]

                        state["data"].append([index,[x,y,z]])
                        structure["data"].append([index,t,lipidId])

                        index += 1

                    H1 = index-1
                    H2 = index-2
                    T1 = index-3
                    T2 = index-4
                    T3 = index-5

                    # Bonds
                    forceField["bond"]["data"].append([H1,H2,kH1_H2_POPC,b0_H1_H2_POPC])
                    forceField["bond"]["data"].append([H2,T1,kH2_T1_POPC,b0_H2_T1_POPC])
                    forceField["bond"]["data"].append([T1,T2,kT1_T2_POPC,b0_T1_T2_POPC])
                    forceField["bond"]["data"].append([T2,T3,kT2_T3_POPC,b0_T2_T3_POPC])

                    # Angles
                    forceField["angle"]["data"].append([H1,H2,T1,kH1_H2_T1_POPC,theta0_H1_H2_T1_POPC])
                    forceField["angle"]["data"].append([H2,T1,T2,kH2_T1_T2_POPC,theta0_H2_T1_T2_POPC])
                    forceField["angle"]["data"].append([T1,T2,T3,kT1_T2_T3_POPC,theta0_T1_T2_T3_POPC])

                    lipidId += 1

        forceField["verletList"] = {}
        forceField["verletList"]["type"]       = ["VerletConditionalListSet", "intra_inter"]
        forceField["verletList"]["parameters"] = {"cutOffVerletFactor":1.2}

        # Repulsive part of the potential
        forceField["WCA"] = {}
        forceField["WCA"]["type"]       = ["NonBonded", "WCAType1"]
        forceField["WCA"]["parameters"] = {"cutOffFactor": 2.5,
                                           "condition":"inter"}

        forceField["WCA"]["labels"] = ["name_i", "name_j", "epsilon", "sigma"]
        forceField["WCA"]["data"]   = []

        for l1 in lipid:
            for l2 in lipid:
                typ1 = l1.split("_")[1]
                typ1 = typ1[0]

                typ2 = l2.split("_")[1]
                typ2 = typ2[0]

                if typ1 == typ2:
                    if typ1 == "H":
                        forceField["WCA"]["data"].append([l1,l2,eps,sigmaH])
                    if typ1 == "T":
                        forceField["WCA"]["data"].append([l1,l2,eps,sigmaT])
                else:
                    forceField["WCA"]["data"].append([l1,l2,eps,(sigmaT+sigmaH)/2.0])

        # Attractive part of the potential
        forceField["ATT"] = {}
        forceField["ATT"]["type"]       = ["NonBonded", "LaTorre"]
        forceField["ATT"]["parameters"] = {"condition":"inter"}

        forceField["ATT"]["labels"] = ["name_i", "name_j", "epsilon", "sigma","w"]
        forceField["ATT"]["data"]   = []

        for l1 in lipid:
            for l2 in lipid:
                typ1 = l1.split("_")[1]

                typ2 = l2.split("_")[1]

                if "H" in typ1 or "H" in typ2:
                    forceField["ATT"]["data"].append([l1,l2,0.0,0.0,0.0]) # Head-head and head-tail interactions are not considered
                    continue
                if "T1" in typ1 and "T3" in typ2:
                    forceField["ATT"]["data"].append([l1,l2,0.0,0.0,0.0]) # T1-T3 interactions are not considered
                    continue
                if "T3" in typ1 and "T1" in typ2:
                    forceField["ATT"]["data"].append([l1,l2,0.0,0.0,0.0]) # T3-T1 interactions are not considered
                    continue
                forceField["ATT"]["data"].append([l1,l2,eps,sigmaT,w])

        #Set model
        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,selectionType,selectionOptions):
        return None
