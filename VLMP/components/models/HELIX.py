import sys, os
import itertools

import logging

from . import modelBase
from ...utils.geometry import getEx
from ...utils.geometry import boxChecker,platesChecker

from ...utils.input import getSubParameters

from ...utils.geometry.objects.helix import computeHelixMatrix, generateHelix, computeConnections, computeLinker

import random

import orthopoly

import numpy as np
from scipy.spatial import cKDTree

from pyquaternion import Quaternion

from scipy.spatial.transform import Rotation
from scipy.optimize import root


class HELIX(modelBase):
    """
    Component name: HELIX
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 25/04/2023

    Polimerization model for a helix.

    """

    def __checkVariantParameters(self,variantRequiredParameters,variantAvailableParameters):
        #Check parameters
        for vPar in variantRequiredParameters:
            if vPar not in self.variantParams:
                self.logger.error(f"[HELIX] Requiered parameter {vPar} for variant {self.variantName} not found."
                                  f"Required parameters are {variantRequiredParameters}")
                raise Exception(f"Required parameter not given")

        #Check parameters
        for vPar in self.variantParams:
            if vPar not in variantAvailableParameters:
                self.logger.error(f"[HELIX] Parameter {vPar} for variant {self.variantName} not found."
                                  f"Available parameters are {variantAvailableParameters}")
                raise Exception(f"Parameter not available")

    def __generateRandomPositions(self):
        monomersPositions    = []
        monomersOrientations = []

        boxX,boxY,boxZ = [b/2.0 for b in self.box]

        n=1
        while(n<=self.nMonomers):
            self.logger.debug(f"[HELIX] Trying to add monomer {n}")

            #We take into account the monomer radius for avoiding problems with PBC
            x=np.random.uniform(low=-boxX + self.monomerRadius, high=boxX - self.monomerRadius)
            y=np.random.uniform(low=-boxY + self.monomerRadius, high=boxY - self.monomerRadius)
            z=np.random.uniform(low=-boxZ + self.monomerRadius, high=boxZ - self.monomerRadius)

            currentMonomerPosition = np.asarray([x,y,z])

            if not self.checker.check([x,y,z]):
                continue

            if monomersPositions:
                minDst,minDstIndex = cKDTree(monomersPositions).query(currentMonomerPosition, 1)
            else:
                minDst = np.inf

            if minDst > 1.5*(2.0*self.monomerRadius):
                monomersPositions.append(currentMonomerPosition)
                q=Quaternion.random()
                q0,q1,q2,q3 = q
                monomersOrientations.append(np.asarray([q0,q1,q2,q3]))
                self.logger.debug(f"[HELIX] Added monomer {n}")
                n=n+1


        return np.asarray(monomersPositions),np.asarray(monomersOrientations)

    def __generateLine(self):
        monomersPositions    = []
        monomersOrientations = []

        boxX,boxY,boxZ = [b/2.0 for b in self.box]

        for n in range(self.nMonomers):
            self.logger.debug(f"[HELIX] Trying to add monomer {n}")

            x=-boxX+self.monomerRadius+(n+1)*2.2*self.monomerRadius
            y=0.0
            z=0.0

            currentMonomerPosition = np.asarray([x,y,z])

            monomersPositions.append(currentMonomerPosition)
            monomersOrientations.append(np.asarray([1.0,0.0,0.0,0.0]))

        centroid = np.mean(monomersPositions,axis=0)
        monomersPositions-=centroid

        for p in monomersPositions:
            if not self.checker.check(p):
                self.logger.error(f"[HELIX] Box too small")
                raise Exception("Box too small")


        return np.asarray(monomersPositions),np.asarray(monomersOrientations)

    def __generateHelix(self):

        monomersPositions,monomersOrientations = generateHelix(self.nMonomers,
                                                               self.helixRadius,self.helixPitch,
                                                               self.helicity,self.monomerRadius*2.0)

        monomersOrientationsTmp = []
        for o in monomersOrientations:
            q = Rotation.from_matrix(o).as_quat() # scalar last
            q = [q[3],q[0],q[1],q[2]] # scalar first
            monomersOrientationsTmp.append(q)

        monomersOrientations = monomersOrientationsTmp.copy()

        centroid = np.mean(monomersPositions,axis=0)
        monomersPositions-=centroid

        for p in monomersPositions:
            if not self.checker.check(p):
                self.logger.error(f"[HELIX] Box too small")
                raise Exception("Box too small")

        return np.asarray(monomersPositions),np.asarray(monomersOrientations)

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"mode","init",
                                                "nMonomers",
                                                "monomerRadius",
                                                "epsilon_mm",
                                                "helixRadius","helixPitch",
                                                "helicity",
                                                "variant"},
                         requiredParameters  = {"nMonomers",
                                                "epsilon_mm",
                                                "helixRadius","helixPitch",
                                                "variant"},
                         definedSelections   = {"particleId"},
                         **params)

        self.logger = logging.getLogger("VLMP")

        ############################################################
        ####################  Model Parameters  ####################
        ############################################################

        self.init                 = params.get("init","random")
        self.mode,self.modeParams = getSubParameters("mode",params)

        if self.mode not in ["bulk","surface"]:
            self.logger.error(f"[HELIX] Mode {self.mode} not supported")
            raise Exception(f"Mode not supported")

        self.nMonomers      = params["nMonomers"]

        self.kT  = self.getEnsemble().getEnsembleComponent("temperature")*self.getUnits().getConstant("KBOLTZ")
        self.box = self.getEnsemble().getEnsembleComponent("box")

        self.monomerRadius = params.get("monomerRadius",0.5)

        self.epsilon_mm = params["epsilon_mm"]

        self.helixRadius = params["helixRadius"]
        self.helixPitch  = params["helixPitch"]

        self.helicity = params.get("helicity",1.0)

        ##############################################

        self.R_H = computeHelixMatrix(self.helixRadius,self.helixPitch,self.helicity,
                                      self.monomerRadius*2.0)

        self.e_x = list(self.R_H[:,0])
        self.e_y = list(self.R_H[:,1])
        self.e_z = list(self.R_H[:,2])

        connectionNext,connectionPrevious = computeConnections(self.helixRadius,self.helixPitch,self.helicity,
                                                               self.monomerRadius*2.0)

        self.e_next = list(connectionNext)
        self.e_prev = list(connectionPrevious)

        ##############################################

        # Available variants:
        #   - fixedCosine
        #   - fixedExponential
        #   - dynamicCosine
        #   - dynamicExponential
        #   - twoStatesCosine
        #   - twoStatesExponential

        self.variantName, self.variantParams = getSubParameters("variant",params)

        if self.variantName == "fixedCosine":

            self.logger.info(f"[HELIX] Using fixedCosine variant")

            variantAvailableParameters  = {"E","Kb","theta_start","theta_end","phi_start","phi_end"}
            variantRequiredParameters   = {"E","Kb","theta_start","theta_end","phi_start","phi_end"}

            self.__checkVariantParameters(variantRequiredParameters,variantAvailableParameters)

            if self.init != "helix" and self.init != "line":
                self.logger.error(f"[HELIX] Init mode {self.init} is not avaible for fixedCosine variant")
                raise Exception("Init mode not available")

        elif self.variantName == "fixedExponential":

            self.logger.info(f"[HELIX] Using fixedExponential variant")

            variantAvailableParameters  = {"E","Kb","Ka","Kd"}
            variantRequiredParameters   = {"E","Kb","Ka","Kd"}

            self.__checkVariantParameters(variantRequiredParameters,variantAvailableParameters)

            #Chekc init mode is helix
            if self.init != "helix" and self.init != "line":
                self.logger.error(f"[HELIX] Init mode {self.init} is not avaible for fixedExponential variant")
                raise Exception("Init mode not available")

        elif self.variantName == "dynamicCosine":

            self.logger.info(f"[HELIX] Using dynamicCosine variant")

            variantAvailableParameters  = {"energyThreshold","Eb","theta_start","theta_end","phi_start","phi_end","r_start","rc","patchRadius"}
            variantRequiredParameters   = {"Eb","theta_start","theta_end","phi_start","phi_end","r_start","rc"}

            self.__checkVariantParameters(variantRequiredParameters,variantAvailableParameters)

            if "energyThreshold" not in self.variantParams:
                self.variantParams["energyThreshold"] = 0.0

            if "patchRadius" not in self.variantParams:
                self.variantParams["patchRadius"] = self.monomerRadius/5.0

        elif self.variantName == "dynamicExponential":

            self.logger.info(f"[HELIX] Using dynamicExponential variant")

            variantAvailableParameters  = {"energyThreshold","Eb","Ka","Kd","Kb","rc","patchRadius"}
            variantRequiredParameters   = {"Eb","Ka","Kd","Kb","rc"}

            self.__checkVariantParameters(variantRequiredParameters,variantAvailableParameters)

            if "energyThreshold" not in self.variantParams:
                self.variantParams["energyThreshold"] = 0.0

            if "patchRadius" not in self.variantParams:
                self.variantParams["patchRadius"] = self.monomerRadius/5.0

        elif self.variantName == "twoStatesCosine":

            self.logger.info(f"[HELIX] Using twoStatesCosine variant")

            variantAvailableParameters  = {"energyThreshold","patchRadius",
                                           "theta_start_0","theta_end_0","phi_start_0","phi_end_0",
                                           "theta_start_1","theta_end_1","phi_start_1","phi_end_1",
                                           "r_start_0","r_start_1","rc_0","rc_1",
                                           "prob_0_to_1","prob_1_to_0"}

            variantRequiredParameters   = {"patchRadius",
                                           "theta_start_0","theta_end_0","phi_start_0","phi_end_0",
                                           "theta_start_1","theta_end_1","phi_start_1","phi_end_1",
                                           "r_start_0","r_start_1","rc_0","rc_1",
                                           "prob_0_to_1","prob_1_to_0"}

            self.__checkVariantParameters(variantRequiredParameters,variantAvailableParameters)

            if "energyThreshold" not in self.variantParams:
                self.variantParams["energyThreshold"] = 0.0

            if "patchRadius" not in self.variantParams:
                self.variantParams["patchRadius"] = self.monomerRadius/5.0

        elif self.variantName == "twoStatesExponential":

            self.logger.info(f"[HELIX] Using twoStatesExponential variant")

            variantAvailableParameters  = {"energyThreshold","patchRadius",
                                           "Ka_0","Kd_0","Kb_0",
                                           "Ka_1","Kd_1","Kb_1",
                                           "Kb_0","Kb_1",
                                           "rc_0","rc_1",
                                           "prob_0_to_1","prob_1_to_0"}

            variantRequiredParameters   = {"patchRadius",
                                           "Ka_0","Kd_0","Kb_0",
                                           "Ka_1","Kd_1","Kb_1",
                                           "Kb_0","Kb_1",
                                           "rc_0","rc_1",
                                           "prob_0_to_1","prob_1_to_0"}

            self.__checkVariantParameters(variantRequiredParameters,variantAvailableParameters)

            if "energyThreshold" not in self.variantParams:
                self.variantParams["energyThreshold"] = 0.0

            if "patchRadius" not in self.variantParams:
                self.variantParams["patchRadius"] = self.monomerRadius/5.0

        else:
            self.logger.error(f"[HELIX] Variant {self.variantName} not available")
            raise Exception("Variant not available")

        ##############################################

        if self.mode=="surface":
            #Check parameters Es,beta0,El,Sl are present in params
            requiredSurfaceParams = ["Es","beta0","El","Sl","plateTop","plateBottom"]

            for sPar in requiredSurfaceParams:
                if sPar not in self.modeParams:
                    self.logger.error(f"[HELIX] Requiered parameter {sPar} for surface mode not found."
                                      f"Required parameters are {requiredSurfaceParams}")
                    raise Exception(f"Required parameter not given")

            plateTop    = self.modeParams["plateTop"]
            plateBottom = self.modeParams["plateBottom"]

            self.checker = platesChecker(self.box,plateTop,plateBottom,2.0*self.monomerRadius)
        else:
            self.checker = boxChecker(self.box)

        ##############################################

        self.logger.info(f"[HELIX] Generating HELIX model with {self.nMonomers} monomers")

        if   self.init == "random":
            self.monomersPositions,self.monomersOrientations = self.__generateRandomPositions()
        elif self.init == "line":
            self.monomersPositions,self.monomersOrientations = self.__generateLine()
        elif self.init == "helix":
            self.monomersPositions,self.monomersOrientations = self.__generateHelix()
        else:
            self.logger.error(f"[HELIX] Init mode {self.init} is not avaible")
            raise Exception("Init mode not available")

        ##############################################

        types = self.getTypes()

        types.addType(name="M",radius=self.monomerRadius)

        ##############################################

        state = {}
        state["labels"]=["id","position","direction"]
        state["data"]  =[]

        for i,[p,q] in enumerate(zip(self.monomersPositions,self.monomersOrientations)):
            state["data"].append([int(i),list(p),list(q)])

        ##############################################

        structure = {}
        structure["labels"] = ["id", "type", "modelId"]
        structure["data"]   = []

        for i in range(self.nMonomers):
            structure["data"].append([int(i),"M",int(i)])

        ##############################################

        forceField = {}

        #Verlet list
        forceField["verletListParticles"]={}
        forceField["verletListParticles"]["type"]       =  ["VerletConditionalListSet", "all"]
        forceField["verletListParticles"]["parameters"] =  {"cutOffVerletFactor":1.5}

        #WCA
        forceField["MonomerMonomer"]={}
        forceField["MonomerMonomer"]["type"]       =  ["NonBonded", "GeneralLennardJonesType2"]
        forceField["MonomerMonomer"]["parameters"] =  {"cutOffFactor":2.5,"condition":"all"}
        forceField["MonomerMonomer"]["labels"]     =  ["name_i", "name_j", "epsilon", "sigma"]
        forceField["MonomerMonomer"]["data"]       =  [["M", "M", self.epsilon_mm, 2.0*self.monomerRadius]]

        ############Helix

        if "fixed" in self.variantName:

            forceField["helix"]={}
            if self.variantName == "fixedCosine":
                forceField["helix"]["type"]       = ["Bond2", "HelixCosine"]
            elif self.variantName == "fixedExponential":
                forceField["helix"]["type"]       = ["Bond2", "HelixExponential"]

            forceField["helix"]["parameters"] =  self.variantParams.copy()

            forceField["helix"]["parameters"]["e_x"] = self.e_x
            forceField["helix"]["parameters"]["e_y"] = self.e_y
            forceField["helix"]["parameters"]["e_z"] = self.e_z

            forceField["helix"]["parameters"]["e_next"] = self.e_next
            forceField["helix"]["parameters"]["e_prev"] = self.e_prev

            forceField["helix"]["labels"] = ["id_i","id_j"]
            forceField["helix"]["data"]   = []

            for i in range(self.nMonomers-1):
                forceField["helix"]["data"].append([i,i+1])

        if "dynamic" in self.variantName or "twoStates" in self.variantName:

            patchRadius = self.variantParams["patchRadius"]

            #Helix
            forceField["helix"]={}
            forceField["helix"]["type"]       = ["PatchyParticles","DynamicallyBondedPatchyParticles"]

            forceField["helix"]["patchesState"]={}
            forceField["helix"]["patchesState"]["labels"]=["id","position"]
            forceField["helix"]["patchesState"]["data"]  =[]

            for i in range(self.nMonomers):
                index=i*2
                p = self.e_prev
                forceField["helix"]["patchesState"]["data"].append([int(index  ),list(p)])
                p = self.e_next
                forceField["helix"]["patchesState"]["data"].append([int(index+1),list(p)])

            forceField["helix"]["patchesGlobal"]={}
            forceField["helix"]["patchesGlobal"]["fundamental"] = {}
            forceField["helix"]["patchesGlobal"]["fundamental"]["type"]       = ["Fundamental","DynamicallyBondedPatchyParticles"]
            forceField["helix"]["patchesGlobal"]["fundamental"]["parameters"] = {"energyThreshold":self.variantParams["energyThreshold"]}

            forceField["helix"]["patchesGlobal"]["types"]  = {}
            forceField["helix"]["patchesGlobal"]["types"]["type"]   = ["Types","Basic"]
            forceField["helix"]["patchesGlobal"]["types"]["labels"] = ["name", "mass", "radius", "charge"]
            forceField["helix"]["patchesGlobal"]["types"]["data"]   = [["S",0.0,patchRadius,0.0],
                                                                       ["E",0.0,patchRadius,0.0]]

            forceField["helix"]["patchesTopology"]={}

            forceField["helix"]["patchesTopology"]["structure"]={}
            forceField["helix"]["patchesTopology"]["structure"]["labels"] = ["id", "type", "parentId"]
            forceField["helix"]["patchesTopology"]["structure"]["data"]   = []

            for i in range(self.nMonomers):
                index=i*2
                forceField["helix"]["patchesTopology"]["structure"]["data"].append([index  ,"E",i])
                forceField["helix"]["patchesTopology"]["structure"]["data"].append([index+1,"S",i])

            forceField["helix"]["patchesTopology"]["forceField"] = {}

            #Verlet list
            forceField["helix"]["patchesTopology"]["forceField"]["verletList"]={}
            forceField["helix"]["patchesTopology"]["forceField"]["verletList"]["type"]       =  ["VerletConditionalListSet", "interDifferentType"]
            forceField["helix"]["patchesTopology"]["forceField"]["verletList"]["parameters"] =  {"cutOffVerletFactor":3.0}

            forceField["helix"]["patchesTopology"]["forceField"]["helix"]={}
            forceField["helix"]["patchesTopology"]["forceField"]["helix"]["parameters"] =  {"condition":"inter"}

            if self.variantName == "dynamicCosine":
                forceField["helix"]["patchesTopology"]["forceField"]["helix"]["type"]       =  ["NonBondedPatches", "HelixCosine"]
                forceField["helix"]["patchesTopology"]["forceField"]["helix"]["labels"]     =  ["name_i", "name_j", "Eb", "theta_start", "theta_end", "phi_start", "phi_end", "r_start", "rc", "e_x", "e_y", "e_z"]
                forceField["helix"]["patchesTopology"]["forceField"]["helix"]["data"]       =  [["S", "E",
                                                                                                 self.variantParams["Eb"],
                                                                                                 self.variantParams["theta_start"], self.variantParams["theta_end"],
                                                                                                 self.variantParams["phi_start"], self.variantParams["phi_end"],
                                                                                                 self.variantParams["r_start"], self.variantParams["rc"],
                                                                                                 self.e_x,self.e_y,self.e_z]]
            elif self.variantName == "dynamicExponential":
                forceField["helix"]["patchesTopology"]["forceField"]["helix"]["type"]       =  ["NonBondedPatches", "HelixExponential"]
                forceField["helix"]["patchesTopology"]["forceField"]["helix"]["labels"]     =  ["name_i", "name_j", "Eb", "Kb", "Ka", "Kd", "rc", "e_x", "e_y", "e_z"]
                forceField["helix"]["patchesTopology"]["forceField"]["helix"]["data"]       =  [["S", "E",
                                                                                                 self.variantParams["Eb"], self.variantParams["Kb"],
                                                                                                 self.variantParams["Ka"], self.variantParams["Kd"],
                                                                                                 self.variantParams["rc"],
                                                                                                 self.e_x,self.e_y,self.e_z]]

            else:
                #Not implemented yet
                raise Exception("Not implemented yet")

        #############Patches

        #Surface
        if(self.mode == "surface"):

            beta0  = self.modeParams["beta0"]
            linker = computeLinker(self.helixRadius,self.helixPitch,self.helicity,2.0*self.monomerRadius,beta0)

            if "patchRadius" not in self.variantParams:
                patchRadius = self.monomerRadius/5.0

            forceField["plateUp"]={}
            forceField["plateUp"]["type"]           = ["Surface", "SurfaceWCAType2"]
            forceField["plateUp"]["parameters"]     = {"surfacePosition": plateTop}
            forceField["plateUp"]["labels"]         = ["name", "epsilon", "sigma"]
            forceField["plateUp"]["data"]           = [["M",1.0,2.0*self.monomerRadius]]

            forceField["plateBottom"]={}
            forceField["plateBottom"]["type"]       = ["Surface", "ParabolaSurface"]
            forceField["plateBottom"]["parameters"] = {"surfacePosition":plateBottom+self.monomerRadius}
            forceField["plateBottom"]["labels"]     = ["name", "epsilon"]
            forceField["plateBottom"]["data"]       = [["M",self.modeParams["Es"]]]

            #Patches

            forceField["surface"]={}
            forceField["surface"]["type"]       = ["PatchyParticles","PatchyParticles"]

            forceField["surface"]["patchesState"]={}
            forceField["surface"]["patchesState"]["labels"]=["id","position"]
            forceField["surface"]["patchesState"]["data"]  =[]

            for i in range(self.nMonomers):
                index=i
                forceField["surface"]["patchesState"]["data"].append([int(index),list(linker)])

            forceField["surface"]["patchesGlobal"]={}
            forceField["surface"]["patchesGlobal"]["fundamental"] = {}
            forceField["surface"]["patchesGlobal"]["fundamental"]["type"]      = ["Fundamental","None"]
            forceField["surface"]["patchesGlobal"]["fundamental"]["parameters"]= {}

            forceField["surface"]["patchesGlobal"]["types"]  = {}
            forceField["surface"]["patchesGlobal"]["types"]["type"]   = ["Types","Basic"]
            forceField["surface"]["patchesGlobal"]["types"]["labels"] = ["name", "mass", "radius", "charge"]
            forceField["surface"]["patchesGlobal"]["types"]["data"]   = [["L",0.0,patchRadius,0.0]]

            forceField["surface"]["patchesTopology"] = {}

            forceField["surface"]["patchesTopology"]["structure"] = {}
            forceField["surface"]["patchesTopology"]["structure"]["labels"] = ["id", "type", "parentId"]
            forceField["surface"]["patchesTopology"]["structure"]["data"]   = []

            for i in range(self.nMonomers):
                forceField["surface"]["patchesTopology"]["structure"]["data"].append([i,"L",i])

            forceField["surface"]["patchesTopology"]["forceField"] = {}

            forceField["surface"]["patchesTopology"]["forceField"]["linker"]={}
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["type"]       =  ["SurfacePatches", "Linker"]
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["parameters"] =  {"surfacePosition":plateBottom}
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["labels"]     =  ["name", "epsilon", "sigma"]
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["data"]       =  [["L",
                                                                                                self.modeParams["El"],
                                                                                                self.modeParams["Sl"]]]

        ##############################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)

    def processSelection(self,**params):

        sel = []
        if "particleId" in params:
            sel += params["particleId"]
        return sel
