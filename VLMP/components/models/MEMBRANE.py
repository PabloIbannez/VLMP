import sys, os

import copy

import logging
import random

from . import modelBase
from ...utils.input import getLabelIndex

class MEMBRANE(modelBase):
    """
    {
    "warning": "This model is currently under development. Please, use it with caution.",
    }
    """

    availableParameters = {"position","composition"}
    requiredParameters  = set()
    definedSelections   = {"particleId"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        mebranePosition = params.get("position",0.0)
        if "composition" in params:
            composition     = params.get("composition")

            if "POPC" not in composition:
                self.logger.error("POPC not found in composition")
                raise ValueError("POPC not found in composition")
            if "DPPC" not in composition:
                self.logger.error("DPPC not found in composition")
                raise ValueError("DPPC not found in composition")

            total = 0.0
            for key in composition:
                if key not in ["POPC","DPPC"]:
                    self.logger.error("Lipid type not supported")
                    raise ValueError("Lipid type not supported")
                total += composition[key]
            if total != 1.0:
                self.logger.error(f"Composition does not sum 1.0, sum = {total}")
                raise ValueError("Composition does not sum 1.0")
        else:
            composition     = params.get("composition",{"POPC":1.0,"DPPC":0.0})

        availableLipids = ["POPC","DPPC"]
        lipidsPercentage  = [composition["POPC"],composition["DPPC"]]


        ############################################################
        ######################  Set up model  ######################
        ############################################################

        # Parameters

        lipidsBase = ["T3","T2","T1","H2","H1"]

        sigmaT_POPC = 7.111
        sigmaT_DPPC = 6.900

        lipidsTypes = {}
        lipidsTypes["POPC"] = {"sigmaT":sigmaT_POPC,
                               "sigmaH":0.65*sigmaT_POPC,
                               "eps":0.416,
                               "w":9.867,
                               "bonds":{
                                   "H1_H2": {"K":2.0*0.446,"r0":5.580},
                                   "H2_T1": {"K":2.0*1.073,"r0":5.452},
                                   "T1_T2": {"K":2.0*1.001,"r0":5.050},
                                   "T2_T3": {"K":2.0*0.443,"r0":5.095}},
                               "angles":{
                                   "H1_H2_T1": {"K":2.0*0.600,"theta0":3.142},
                                   "H2_T1_T2": {"K":2.0*2.383,"theta0":3.142},
                                   "T1_T2_T3": {"K":2.0*0.880,"theta0":3.142}}}

        lipidsTypes["POPC"]["types"] = {}
        for l in lipidsBase:
            if l in ["H1","H2"]:
                sgm = lipidsTypes["POPC"]["sigmaH"]
            else:
                sgm = lipidsTypes["POPC"]["sigmaT"]
            lipidsTypes["POPC"]["types"][l] = {"radius":sgm/2.0,
                                               "charge":0.0,
                                               "mass":100.0}

        lipidsTypes["DPPC"] = {"sigmaT":sigmaT_DPPC,
                               "sigmaH":0.65*sigmaT_DPPC,
                               "eps":0.464,
                               "w":10.318,
                               "bonds":{
                                   "H1_H2": {"K":2.0*0.471,"r0":5.417},
                                   "H2_T1": {"K":2.0*1.320,"r0":5.824},
                                   "T1_T2": {"K":2.0*0.875,"r0":6.312},
                                   "T2_T3": {"K":2.0*0.280,"r0":6.299}},
                               "angles":{
                                   "H1_H2_T1": {"K":2.0*0.582,"theta0":3.142},
                                   "H2_T1_T2": {"K":2.0*3.357,"theta0":3.142},
                                   "T1_T2_T3": {"K":2.0*4.823,"theta0":3.142}}}

        lipidsTypes["DPPC"]["types"] = {}
        for l in lipidsBase:
            if l in ["H1","H2"]:
                sgm = lipidsTypes["DPPC"]["sigmaH"]
            else:
                sgm = lipidsTypes["DPPC"]["sigmaT"]
            lipidsTypes["DPPC"]["types"][l] = {"radius":sgm/2.0,
                                               "charge":0.0,
                                               "mass":100.0}

        # We use the largest sigmaT to define the spacing
        sigmaT = max([lipidsTypes["POPC"]["sigmaT"],lipidsTypes["DPPC"]["sigmaT"]])

        spacing  = sigmaT*0.1
        zSpacing = sigmaT*0.0

        ########################################################

        types = self.getTypes()
        for key in lipidsTypes:
            for l in lipidsTypes[key]["types"]:
                types.addType(name=f"{key}_{l}",**lipidsTypes[key]["types"][l])

        box = self.getEnsemble().getEnsembleComponent("box")

        # Create the membrane
        nLipidsX = box[0]/(sigmaT+spacing)
        nLipidsY = box[1]/(sigmaT+spacing)

        N = nLipidsX*nLipidsY

        # Create the lipids
        dx = sigmaT + spacing
        dy = sigmaT + spacing

        lipidZ = {}

        lipidZ["POPC"] = [0.0]*len(lipidsBase)
        lipidZ["POPC"][0] = sigmaT_POPC/2.0 + zSpacing
        lipidZ["POPC"][1] = lipidZ["POPC"][0] + lipidsTypes["POPC"]["bonds"]["H1_H2"]["r0"]
        lipidZ["POPC"][2] = lipidZ["POPC"][1] + lipidsTypes["POPC"]["bonds"]["H2_T1"]["r0"]
        lipidZ["POPC"][3] = lipidZ["POPC"][2] + lipidsTypes["POPC"]["bonds"]["T1_T2"]["r0"]
        lipidZ["POPC"][4] = lipidZ["POPC"][3] + lipidsTypes["POPC"]["bonds"]["T2_T3"]["r0"]

        lipidZ["DPPC"] = [0.0]*len(lipidsBase)
        lipidZ["DPPC"][0] = sigmaT_DPPC/2.0 + zSpacing
        lipidZ["DPPC"][1] = lipidZ["DPPC"][0] + lipidsTypes["DPPC"]["bonds"]["H1_H2"]["r0"]
        lipidZ["DPPC"][2] = lipidZ["DPPC"][1] + lipidsTypes["DPPC"]["bonds"]["H2_T1"]["r0"]
        lipidZ["DPPC"][3] = lipidZ["DPPC"][2] + lipidsTypes["DPPC"]["bonds"]["T1_T2"]["r0"]
        lipidZ["DPPC"][4] = lipidZ["DPPC"][3] + lipidsTypes["DPPC"]["bonds"]["T2_T3"]["r0"]

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

                    selectedLipid = random.choices(availableLipids,
                                                   weights=lipidsPercentage)[0]

                    for k,t in enumerate(lipidsBase):

                        beadType = f"{selectedLipid}_{t}"

                        # The last tail particles is placed at z = sigmaT/2.0+zSpacing
                        x = i*dx + dx/2.0 - box[0]/2.0
                        y = j*dy + dy/2.0 - box[1]/2.0
                        if leaflet == 0: # Upper leaflet
                            z =   lipidZ[selectedLipid][k]
                        else: # Lower leaflet
                            z = - lipidZ[selectedLipid][k]

                        state["data"].append([index,[x,y,z]])
                        structure["data"].append([index,beadType,lipidId])

                        index += 1

                    H1 = index-1
                    H2 = index-2
                    T1 = index-3
                    T2 = index-4
                    T3 = index-5

                    # Bonds
                    kH1_H2 = lipidsTypes[selectedLipid]["bonds"]["H1_H2"]["K"]
                    kH2_T1 = lipidsTypes[selectedLipid]["bonds"]["H2_T1"]["K"]
                    kT1_T2 = lipidsTypes[selectedLipid]["bonds"]["T1_T2"]["K"]
                    kT2_T3 = lipidsTypes[selectedLipid]["bonds"]["T2_T3"]["K"]

                    b0_H1_H2 = lipidsTypes[selectedLipid]["bonds"]["H1_H2"]["r0"]
                    b0_H2_T1 = lipidsTypes[selectedLipid]["bonds"]["H2_T1"]["r0"]
                    b0_T1_T2 = lipidsTypes[selectedLipid]["bonds"]["T1_T2"]["r0"]
                    b0_T2_T3 = lipidsTypes[selectedLipid]["bonds"]["T2_T3"]["r0"]

                    forceField["bond"]["data"].append([H1,H2,kH1_H2,b0_H1_H2])
                    forceField["bond"]["data"].append([H2,T1,kH2_T1,b0_H2_T1])
                    forceField["bond"]["data"].append([T1,T2,kT1_T2,b0_T1_T2])
                    forceField["bond"]["data"].append([T2,T3,kT2_T3,b0_T2_T3])

                    kH1_H2_T1 = lipidsTypes[selectedLipid]["angles"]["H1_H2_T1"]["K"]
                    kH2_T1_T2 = lipidsTypes[selectedLipid]["angles"]["H2_T1_T2"]["K"]
                    kT1_T2_T3 = lipidsTypes[selectedLipid]["angles"]["T1_T2_T3"]["K"]

                    theta0_H1_H2_T1 = lipidsTypes[selectedLipid]["angles"]["H1_H2_T1"]["theta0"]
                    theta0_H2_T1_T2 = lipidsTypes[selectedLipid]["angles"]["H2_T1_T2"]["theta0"]
                    theta0_T1_T2_T3 = lipidsTypes[selectedLipid]["angles"]["T1_T2_T3"]["theta0"]

                    # Angles
                    forceField["angle"]["data"].append([H1,H2,T1,kH1_H2_T1,theta0_H1_H2_T1])
                    forceField["angle"]["data"].append([H2,T1,T2,kH2_T1_T2,theta0_H2_T1_T2])
                    forceField["angle"]["data"].append([T1,T2,T3,kT1_T2_T3,theta0_T1_T2_T3])

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

        # Attractive part of the potential
        forceField["ATT"] = {}
        forceField["ATT"]["type"]       = ["NonBonded", "LaTorre"]
        forceField["ATT"]["parameters"] = {"condition":"inter"}

        forceField["ATT"]["labels"] = ["name_i", "name_j", "epsilon", "sigma","w"]
        forceField["ATT"]["data"]   = []

        # Fill the force field

        for la1 in availableLipids:
            for l1 in lipidsTypes[la1]["types"]:
                for la2 in availableLipids:
                    for l2 in lipidsTypes[la2]["types"]:
                        typ1 = l1[0]
                        typ2 = l2[0]

                        if typ1 == "H":
                            sgm1 = lipidsTypes[la1]["sigmaH"]
                        if typ1 == "T":
                            sgm1 = lipidsTypes[la1]["sigmaT"]
                        if typ2 == "H":
                            sgm2 = lipidsTypes[la2]["sigmaH"]
                        if typ2 == "T":
                            sgm2 = lipidsTypes[la2]["sigmaT"]

                        eps1 = lipidsTypes[la1]["eps"]
                        eps2 = lipidsTypes[la2]["eps"]

                        w1 = lipidsTypes[la1]["w"]
                        w2 = lipidsTypes[la2]["w"]

                        eps = (eps1*eps2)**0.5
                        sgm = (sgm1+sgm2)/2.0
                        w   = (w1+w2)/2.0

                        name1 = f"{la1}_{l1}"
                        name2 = f"{la2}_{l2}"

                        forceField["WCA"]["data"].append([name1,name2,eps,sgm])

                        if "H" in typ1 or "H" in typ2:
                            eps = 0.0
                            sgm = 0.0
                            w   = 0.0
                        if "T1" in typ1 and "T3" in typ2:
                            eps = 0.0
                            sgm = 0.0
                            w   = 0.0
                        if "T3" in typ1 and "T1" in typ2:
                            eps = 0.0
                            sgm = 0.0
                            w   = 0.0

                        forceField["ATT"]["data"].append([name1,name2,eps,sgm,w])

        #Set model
        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,selectionType,selectionOptions):
        return None
