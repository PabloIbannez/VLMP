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
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "HELIX model for simulating helical polymer structures. This model is designed to create
      and simulate helical polymers, with a particular focus on representing the structures which
      emerge from the self-assembly of helical monomers. The model uses a patchy-particle approach
      to represent the monomers, with each monomer having two patches which represent the interaction
      sites on the monomer surface. An additional patch is used to represent the surface interaction,
      this additional patch interacts only with the surface and not with other monomers.
      <p>
      The helical shape is achived fixing the relative orientation of the monomers, when patches
      are close enough.
      <p>
      The model generates a helical structure based on specified parameters such as the number
      of monomers, helix radius, pitch, and helicity. It can be used to study various properties
      and behaviors of helical polymers, including their dynamics, and the effects of several
      polymer interactions.
      <p>
      Key features of the HELIX model include:
      <p>
      - Parameters for helical geometry (radius, pitch, helicity)
      <p>
      - Various initialization options (random, line, or pre-formed helix)
      <p>
      - Customizable monomer properties and interactions
      <p>
      - Support for different variants of the model, including fixed and dynamic versions
      <p>
      - Options for simulating interactions with surfaces or other environmental factors",
     "parameters":{
        "mode":{"description":"Simulation mode ('bulk' or 'surface').",
                "type":"str",
                "default":"bulk"},
        "init":{"description":"Initialization method ('random', 'line', or 'helix').",
                "type":"str",
                "default":"random"},
        "nMonomers":{"description":"Number of monomers in the helix.",
                     "type":"int"},
        "monomerRadius":{"description":"Radius of each monomer.",
                         "type":"float",
                         "default":0.5},
        "epsilon_mm":{"description":"Energy parameter for monomer-monomer interactions.",
                      "type":"float"},
        "helixRadius":{"description":"Radius of the helix.",
                       "type":"float"},
        "helixPitch":{"description":"Pitch of the helix.",
                      "type":"float"},
        "helicity":{"description":"Helicity of the structure (1.0 for right-handed, -1.0 for left-handed).",
                    "type":"float",
                    "default":1.0},
        "variant":{"description":"Variant of the model to use ('fixed', 'dynamic').",
                   "type":"str"},
        "surface":{"description":"Whether to include a surface interaction.",
                   "type":"bool",
                   "default":false},
        "surfacePosition":{"description":"Z-coordinate of the surface, if included.",
                           "type":"float",
                           "default":0.0}
     },
     "example":"
         {
            \"type\":\"HELIX\",
            \"parameters\":{
                \"mode\":\"bulk\",
                \"init\":\"helix\",
                \"nMonomers\":100,
                \"helixRadius\":10.0,
                \"helixPitch\":34.0,
                \"epsilon_mm\":1.0,
                \"variant\":\"fixed\"
            }
         }
        ",
     "warning":"This model is under development and may not be fully functional or optimized."
    }
    """

    availableParameters = {"mode","init",
                           "nMonomers",
                           "monomerRadius",
                           "epsilon_mm",
                           "helixRadius","helixPitch",
                           "helicity",
                           "variant"}
    requiredParameters  = {"nMonomers",
                           "epsilon_mm",
                           "helixRadius","helixPitch",
                           "variant"}
    definedSelections   = set()

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
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
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

        # Convert to quaternion
        q = Rotation.from_matrix(self.R_H).as_quat()
        q = [q[3],q[0],q[1],q[2]] # scalar first
        self.R_Hq = q

        connectionNext,connectionPrevious = computeConnections(self.helixRadius,self.helixPitch,self.helicity,
                                                               self.monomerRadius*2.0)

        self.e_next = list(connectionNext)
        self.e_prev = list(connectionPrevious)

        ##############################################

        # Available variants:
        #   - fixed
        #   - dynamic

        self.variantName, self.variantParams = getSubParameters("variant",params)

        if self.variantName == "fixed":

            self.logger.info(f"[HELIX] Using fixed variant")

            variantAvailableParameters  = {"Kb","Kw"}
            variantRequiredParameters   = {"Kb","Kw"}

            self.__checkVariantParameters(variantRequiredParameters,variantAvailableParameters)

            if self.init != "helix" and self.init != "line":
                self.logger.error(f"[HELIX] Init mode {self.init} is not avaible for fixedCosine variant")
                raise Exception("Init mode not available")

        elif self.variantName == "dynamic":

            self.logger.info(f"[HELIX] Using dynamicCosine variant")

            variantAvailableParameters  = {"E","Kb","Kw","rc","energyThreshold","patchRadius"}
            variantRequiredParameters   = {"E","Kb","Kw","rc"}

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

        if "fixed" == self.variantName.strip():

            forceField["helix"]={}
            forceField["helix"]["type"]       = ["Bond2", "HarmonicRAP"]

            forceField["helix"]["labels"] = ["id_i","id_j","Khrm","r0","leftConnection","rightConnection","Krap","R"]
            forceField["helix"]["data"]   = []

            Kb  = self.variantParams["Kb"]
            Kw  = self.variantParams["Kw"]

            Rq = self.R_Hq

            for i in range(self.nMonomers-1):
                forceField["helix"]["data"].append([i,i+1,Kb,0.0,self.e_prev,self.e_next,Kw,Rq])

        elif "dynamic" == self.variantName.strip():

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

            E  = self.variantParams["E"]
            Kb = self.variantParams["Kb"]
            Kw = self.variantParams["Kw"]
            rc = self.variantParams["rc"]
            Rq     = self.R_Hq
            Rqinv  = [Rq[0],-Rq[1],-Rq[2],-Rq[3]]

            forceField["helix"]["patchesTopology"]["forceField"]["helix"]["type"]       =  ["NonBondedPatches", "COSRAP"]
            forceField["helix"]["patchesTopology"]["forceField"]["helix"]["labels"]     =  ["name_i", "name_j", "E", "rc", "R", "Kswt", "Krap"]
            forceField["helix"]["patchesTopology"]["forceField"]["helix"]["data"]       =  [["S", "E", E, rc, Rq, Kb, Kw],
                                                                                            ["E", "S", E, rc, Rqinv, Kb, Kw]]
        else:
            #Not implemented yet
            self.logger.error(f"[HELIX] Variant {self.variantName} not implemented yet")
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

    def processSelection(self,selectionType,selectionOptions):
        return None
