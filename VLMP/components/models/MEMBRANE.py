import sys, os

import copy

import logging

from . import modelBase
from ...utils.input import getLabelIndex

class MEMBRANE(modelBase):
    """
    Component name: MEMBRANE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 22/05/2024

    Alpha carbon resolution membrane model.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"position"},
                         requiredParameters  = set(),
                         definedSelections   = {"particleId"},
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

        types.addType(name="H",radius=sigmaH/2.0,charge=0.0,mass=100.0)
        types.addType(name="T",radius=sigmaT/2.0,charge=0.0,mass=100.0)

        box = self.getEnsemble().getEnsembleComponent("box")

        # Create the membrane
        nLipidsX = box[0]/(sigmaT+spacing)
        nLipidsY = box[1]/(sigmaT+spacing)

        N = nLipidsX*nLipidsY

        # Create the lipids
        dx = sigmaT + spacing
        dy = sigmaT + spacing

        lipid = ["T","T","T","H","H"]

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

        forceField["WCA"] = {}
        forceField["WCA"]["type"]       = ["NonBonded", "WCAType1"]
        forceField["WCA"]["parameters"] = {"cutOffFactor": 2.5,
                                           "condition":"inter"}

        forceField["WCA"]["labels"] = ["name_i", "name_j", "epsilon", "sigma"]
        forceField["WCA"]["data"]   = []

        forceField["WCA"]["data"].append(["T","T",eps,sigmaT])
        forceField["WCA"]["data"].append(["T","H",eps,(sigmaT+sigmaH)/2.0])
        forceField["WCA"]["data"].append(["H","H",eps,sigmaH])

        # Chapuza for the moment
        forceField["LJ"] = {}
        forceField["LJ"]["type"]       = ["NonBonded", "LennardJonesType2"]
        forceField["LJ"]["parameters"] = {"cutOffFactor": 2.5,
                                          "condition":"inter"}

        forceField["LJ"]["labels"] = ["name_i", "name_j", "epsilon", "sigma"]
        forceField["LJ"]["data"]   = []

        forceField["LJ"]["data"].append(["T","T",eps,sigmaT])
        forceField["LJ"]["data"].append(["T","H",0.0,(sigmaT+sigmaH)/2.0])
        forceField["LJ"]["data"].append(["H","H",0.0,sigmaH])

        #Set model
        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel
