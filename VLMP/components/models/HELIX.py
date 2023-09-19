import sys, os
import itertools

import logging

from . import modelBase
from ...utils.geometry import getEx
from ...utils.geometry import boxChecker,platesChecker

from ...utils.input import getSubParameters

import random

import orthopoly

import numpy as np
from scipy.spatial import cKDTree

from pyquaternion import Quaternion

from scipy.spatial.transform import Rotation as R
from scipy.optimize import root


class HELIX(modelBase):
    """
    Component name: HELIX
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 25/04/2023

    Polimerization model for a helix.

    """

    def __computeKdst(self,var,Eb,rc):
        init = 1.0
        Kdst = root(lambda K: var - (self.kT/Eb)*((rc*rc)/(np.pi*np.pi))*((1.0-np.exp(-2.0*K))/K),init)
        varTheo = (self.kT/Eb)*((rc*rc)/(np.pi*np.pi))*((1.0-np.exp(-2.0*Kdst["x"][0]))/Kdst["x"][0])
        if np.abs(varTheo-var) > 1e-6:
            self.logger.error(f"[HELIX] Error computing Kdst")
            raise Exception("Error computing Kdst")
        return Kdst["x"][0]

    def __computeKangle(self,var,Eb):
        init = (1.0-0.5*var*(Eb/self.kT))/2.0
        Kangle = root(lambda K: var - (self.kT/Eb)*((1.0-np.exp(-2.0*K))/K),init)
        varTheo = (self.kT/Eb)*((1.0-np.exp(-2.0*Kangle["x"][0]))/Kangle["x"][0])
        if np.abs(varTheo-var) > 1e-6:
            self.logger.error(f"[HELIX] Error computing Kangle")
            raise Exception("Error computing Kangle")
        return Kangle["x"][0]


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

        sigma = 2.0*self.monomerRadius

        monomersPositions    = []
        monomersOrientations = []

        alpha = np.sqrt(self.theta0*self.theta0+self.phi0*self.phi0)

        cp = self.theta0/alpha;
        sp = self.phi0/alpha;

        cp2 = cp*cp;
        sp2 = sp*sp;

        ca = np.cos(alpha);
        sa = np.sin(alpha);

        Rtrans = np.asarray([[ca*cp2+sp2    ,-sa*cp ,(1.0-ca)*sp*cp],
                             [sa*cp         ,ca     ,-sa*sp],
                             [(1.0-ca)*sp*cp,sa*sp  ,ca*sp2+cp2]])

        r_trans = R.from_matrix(Rtrans)

        boxX,boxY,boxZ = [b/2.0 for b in self.box]

        for n in range(self.nMonomers):
            self.logger.debug(f"[HELIX] Adding monomer {n}")

            if n==0:
                x=0.0
                y=-boxY+sigma
                z=(self.theta0/(self.theta0*self.theta0+self.phi0*self.phi0)-1.0)

                Rinit = np.asarray([[ca*cp ,-sa ,-ca*sp],
                                    [sp    ,0.0 , cp],
                                    [-sa*cp,-ca , sa*sp]])

                r_init = R.from_matrix(Rinit)

                q1,q2,q3,q0 = r_init.as_quat()

            else:

                q0,q1,q2,q3 = monomersOrientations[-1]
                r_prev    = R.from_quat([q1,q2,q3,q0])
                r_current = r_prev*r_trans

                x,y,z = monomersPositions[-1]+0.5*sigma*(getEx(monomersOrientations[-1])+getEx([q0,q1,q2,q3]))

                q1,q2,q3,q0 = r_current.as_quat()


            currentMonomerPosition = np.asarray([x,y,z])
            currentMonomerOrientation = np.asarray([q0,q1,q2,q3])

            monomersPositions.append(currentMonomerPosition)
            monomersOrientations.append(currentMonomerOrientation)

        centroid = np.mean(monomersPositions,axis=0)
        monomersPositions-=centroid

        for p in monomersPositions:
            if not self.checker.check(p):
                self.logger.error(f"[HELIX] Box too small")
                raise Exception("Box too small")


        return np.asarray(monomersPositions),np.asarray(monomersOrientations)

    def __getMonomerConnections(self,position,orientation):
        connectionStart = position-self.monomerRadius*getEx(orientation)
        connectionEnd   = position+self.monomerRadius*getEx(orientation)

        return connectionStart,connectionEnd

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"mode","init",
                                                "nMonomers",
                                                "monomerRadius","patchRadius",
                                                "epsilon_mm",
                                                "Eb","rc",
                                                "theta0","phi0",
                                                "varDst","varTheta","varPhi",
                                                "Kb","Ka","Kd",
                                                "energyThreshold",
                                                "stiffnessFactor",
                                                "variant"},
                         requiredParameters  = {"nMonomers",
                                                "epsilon_mm",
                                                "Eb","rc",
                                                "theta0","phi0"},
                         definedSelections   = {"particleId"},
                         **params)

        self.logger = logging.getLogger("VLMP")

        ############################################################
        ####################  Model Parameters  ####################
        ############################################################

        self.kT = self.getUnits().getConstant("kT")

        self.init                 = params.get("init","random")
        self.mode,self.modeParams = getSubParameters("mode",params)

        if self.mode not in ["bulk","surface"]:
            self.logger.error(f"[HELIX] Mode {self.mode} not supported")
            raise Exception(f"Mode not supported")

        self.nMonomers      = params["nMonomers"]

        self.box = self.getEnsemble().getEnsembleComponent("box")

        self.monomerRadius = params.get("monomerRadius",0.5)
        self.patchRadius   = params.get("patchRadius",0.1)

        self.epsilon_mm = params["epsilon_mm"]

        self.Eb = params["Eb"]
        self.rc = params["rc"]

        self.energyThreshold = params.get("energyThreshold",-1.0)

        stiffnessFactor = params.get("stiffnessFactor",1.0)

        self.theta0 = params["theta0"]
        self.phi0   = params["phi0"]

        if self.mode=="surface":
            #Check parameters Es,beta0,El,Sl are present in params
            requiredSurfaceParams = ["Es","beta0","El","Sl","plateTop","plateBottom"]

            for sPar in requiredSurfaceParams:
                if sPar not in self.modeParams:
                    self.logger.error(f"[HELIX] Requiered parameter {sPar} for surface mode not found."
                                      f"Required parameters are {requiredSurfaceParams}")
                    raise Exception(f"Required parameter not given")

            self.Es     = self.modeParams["Es"]

            self.beta0  = self.modeParams["beta0"]

            self.El     = self.modeParams["El"]
            self.Sl     = self.modeParams["Sl"]

            self.plateTop    = self.modeParams["plateTop"]
            self.plateBottom = self.modeParams["plateBottom"]

            self.checker = platesChecker(self.box,self.plateTop,self.plateBottom,2.0*self.monomerRadius)
        else:
            self.checker = boxChecker(self.box)

        if "varDst" in params:
            varDst   = params["varDst"]
            self.Kb = self.__computeKdst(varDst,abs(self.Eb),self.rc)
            self.logger.info(f"[HELIX] K bond computed {self.Kb} for variance {varDst}")
        else:
            self.Kb = params["Kb"]
            self.logger.info(f"[HELIX] K bond {self.Kb}")

        if "varTheta" in params:
            varTheta = params["varTheta"]
            self.Ka = self.__computeKangle(varTheta,abs(self.Eb))
            self.logger.info(f"[HELIX] K theta computed {self.Ka} for variance {varTheta}")
        else:
            self.Ka = params["Ka"]
            self.logger.info(f"[HELIX] K theta {self.Ka}")

        if "varPhi" in params:
            varPhi   = params["varPhi"]
            self.Kd = self.__computeKangle(varPhi,abs(self.Eb))
            self.logger.info(f"[HELIX] K phi computed {self.Kd} for variance {varPhi}")
        else:
            self.Kd = params["Kd"]
            self.logger.info(f"[HELIX] K phi {self.Kd}")

        if stiffnessFactor != 1.0:
            self.logger.info(f"[HELIX] Applying stiffness factor {stiffnessFactor}")
            self.Ka*=stiffnessFactor
            self.Kd*=stiffnessFactor

            self.logger.info(f"[HELIX] K theta after stiffness factor {self.Ka}")
            self.logger.info(f"[HELIX] K phi after stiffness factor {self.Kd}")

        if self.Kb < 0 or self.Ka < 0 or self.Kd < 0:
            self.logger.error(f"[HELIX] Negative spring constant: Kb {self.Kb} Ka {self.Ka} Kd {self.Kd}")
            raise Exception("Negative spring constant")

        ##############################################

        self.variantName, self.variantParams = getSubParameters("variant",params)

        if self.variantName == "twoStates":
            self.logger.info(f"[HELIX] Using two states variant")

            variantAvailableParameters = {"Eb2","rc2",
                                          "theta02","phi02",
                                          "varDst2","varTheta2","varPhi2",
                                          "Kb2","Ka2","Kd2",
                                          "prob_1_to_2","prob_2_to_1"}

            variantRequiredParameters  = {"Eb2","rc2",
                                          "theta02","phi02",
                                          "prob_1_to_2","prob_2_to_1"}

            for key in self.variantParams.keys():
                if key not in variantAvailableParameters:
                    self.logger.error(f"[HELIX] Variant parameter {key} is not available for variant {self.variantName}")
                    raise Exception("Not correct variant parameter")

            for key in variantRequiredParameters:
                if key not in self.variantParams.keys():
                    self.logger.error(f"[HELIX] Variant parameter {key} is required for variant {self.variantName}")
                    raise Exception("Not correct variant parameter")

            self.Eb2 = self.variantParams["Eb2"]
            self.rc2 = self.variantParams["rc2"]

            self.theta02 = self.variantParams["theta02"]
            self.phi02   = self.variantParams["phi02"]

            if "varDst2" in self.variantParams:
                varDst2   = self.variantParams["varDst2"]
                self.Kb2 = self.__computeKdst(varDst2,abs(self.Eb2),self.rc2)
                self.logger.info(f"[HELIX] K bond 2 computed {self.Kb2} for variance {varDst2}")
            else:
                self.Kb2 = self.variantParams["Kb2"]
                self.logger.info(f"[HELIX] K bond 2 {self.Kb2}")

            if "varTheta2" in self.variantParams:
                varTheta2 = self.variantParams["varTheta2"]
                self.Ka2 = self.__computeKangle(varTheta2,abs(self.Eb2))
                self.logger.info(f"[HELIX] K theta 2 computed {self.Ka2} for variance {varTheta2}")
            else:
                self.Ka2 = self.variantParams["Ka2"]
                self.logger.info(f"[HELIX] K theta 2 {self.Ka2}")

            if "varPhi2" in self.variantParams:
                varPhi2   = self.variantParams["varPhi2"]
                self.Kd2 = self.__computeKangle(varPhi2,abs(self.Eb2))
                self.logger.info(f"[HELIX] K phi 2 computed {self.Kd2} for variance {varPhi2}")
            else:
                self.Kd2 = self.variantParams["Kd2"]
                self.logger.info(f"[HELIX] K phi 2 {self.Kd2}")

            if stiffnessFactor != 1.0:
                self.logger.info(f"[HELIX] Applying stiffness factor {stiffnessFactor}")

                self.Ka2*=stiffnessFactor
                self.Kd2*=stiffnessFactor

                self.logger.info(f"[HELIX] K2 theta after stiffness factor {self.Ka2}")
                self.logger.info(f"[HELIX] K2 phi after stiffness factor {self.Kd2}")

            if self.Kb2 < 0 or self.Ka2 < 0 or self.Kd2 < 0:
                self.logger.error(f"[HELIX] Negative spring constant: Kb2 {self.Kb2} Ka2 {self.Ka2} Kd2 {self.Kd2}")
                raise Exception("Negative spring constant")

            self.prob_0_to_1 = self.variantParams["prob_1_to_2"] #Note the different naming convention
            self.prob_1_to_0 = self.variantParams["prob_2_to_1"]

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
            p=np.around(p,2)
            q=np.around(q,2)
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

        ############Patches

        #Helix
        forceField["helix"]={}
        forceField["helix"]["type"]       = ["PatchyParticles","DynamicallyBondedPatchyParticles"]

        forceField["helix"]["patchesState"]={}
        forceField["helix"]["patchesState"]["labels"]=["id","position"]
        forceField["helix"]["patchesState"]["data"]  =[]

        for i in range(self.nMonomers):
            index=i*2
            p = [-self.monomerRadius,0.0,0.0]
            forceField["helix"]["patchesState"]["data"].append([int(index  ),list(p)])
            p = [ self.monomerRadius,0.0,0.0]
            forceField["helix"]["patchesState"]["data"].append([int(index+1),list(p)])

        forceField["helix"]["patchesGlobal"]={}
        forceField["helix"]["patchesGlobal"]["fundamental"] = {}
        forceField["helix"]["patchesGlobal"]["fundamental"]["type"]       = ["Fundamental","DynamicallyBondedPatchyParticles"]
        forceField["helix"]["patchesGlobal"]["fundamental"]["parameters"] = {"energyThreshold":self.energyThreshold}

        forceField["helix"]["patchesGlobal"]["types"]  = {}
        forceField["helix"]["patchesGlobal"]["types"]["type"]   = ["Types","Basic"]
        forceField["helix"]["patchesGlobal"]["types"]["labels"] = ["name", "mass", "radius", "charge"]
        forceField["helix"]["patchesGlobal"]["types"]["data"]   = [["S",0.0,self.patchRadius,0.0],
                                                                   ["E",0.0,self.patchRadius,0.0]]

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
        forceField["helix"]["patchesTopology"]["forceField"]["helix"]["type"]       =  ["NonBondedPatches", "Helix"]
        forceField["helix"]["patchesTopology"]["forceField"]["helix"]["parameters"] =  {"condition":"inter"}
        forceField["helix"]["patchesTopology"]["forceField"]["helix"]["labels"]     =  ["name_i", "name_j", "Eb", "Kb", "Ka", "Kd", "rc", "theta0", "phi0"]
        forceField["helix"]["patchesTopology"]["forceField"]["helix"]["data"]       =  [["S", "E",
                                                                                         self.Eb,
                                                                                         self.Kb, self.Ka, self.Kd,
                                                                                         self.rc,
                                                                                         self.theta0, self.phi0]]

        if self.variantName == "twoStates":
            forceField["helix"]["patchesTopology"]["forceField"]["helix"]["type"]   =  ["NonBondedPatches", "Helix2States"]
            forceField["helix"]["patchesTopology"]["forceField"]["helix"]["labels"] = ["name_i", "name_j",
                                                                                       "Eb0", "Kb0", "Ka0", "Kd0", "rc0", "theta0_0", "phi0_0",
                                                                                       "Eb1", "Kb1", "Ka1", "Kd1", "rc1", "theta0_1", "phi0_1",
                                                                                       "prob_0_to_1","prob_1_to_0"]
            forceField["helix"]["patchesTopology"]["forceField"]["helix"]["data"][-1].extend([self.Eb2,
                                                                                              self.Kb2, self.Ka2, self.Kd2,
                                                                                              self.rc2,
                                                                                              self.theta02, self.phi02,
                                                                                              self.prob_0_to_1,self.prob_1_to_0])

        ############Patches

        #Surface
        if(self.mode == "surface"):

            forceField["plateUp"]={}
            forceField["plateUp"]["type"]           = ["Surface", "SurfaceWCAType2"]
            forceField["plateUp"]["parameters"]     = {"surfacePosition": self.plateTop}
            forceField["plateUp"]["labels"]         = ["name", "epsilon", "sigma"]
            forceField["plateUp"]["data"]           = [["M",1.0,2.0*self.monomerRadius]]

            forceField["plateBottom"]={}
            forceField["plateBottom"]["type"]       = ["Surface", "ParabolaSurface"]
            forceField["plateBottom"]["parameters"] = {"surfacePosition":self.plateBottom+self.monomerRadius}
            forceField["plateBottom"]["labels"]     = ["name", "epsilon"]
            forceField["plateBottom"]["data"]       = [["M",self.Es]]

            #Patches

            forceField["surface"]={}
            forceField["surface"]["type"]       = ["PatchyParticles","PatchyParticles"]

            forceField["surface"]["patchesState"]={}
            forceField["surface"]["patchesState"]["labels"]=["id","position"]
            forceField["surface"]["patchesState"]["data"]  =[]

            for i in range(self.nMonomers):
                index=i
                p = [0.0,self.monomerRadius*np.cos(self.beta0),self.monomerRadius*np.sin(self.beta0)]
                forceField["surface"]["patchesState"]["data"].append([int(index),list(p)])

            forceField["surface"]["patchesGlobal"]={}
            forceField["surface"]["patchesGlobal"]["fundamental"] = {}
            forceField["surface"]["patchesGlobal"]["fundamental"]["type"]      = ["Fundamental","None"]
            forceField["surface"]["patchesGlobal"]["fundamental"]["parameters"]= {}

            forceField["surface"]["patchesGlobal"]["types"]  = {}
            forceField["surface"]["patchesGlobal"]["types"]["type"]   = ["Types","Basic"]
            forceField["surface"]["patchesGlobal"]["types"]["labels"] = ["name", "mass", "radius", "charge"]
            forceField["surface"]["patchesGlobal"]["types"]["data"]   = [["L",0.0,self.patchRadius,0.0]]

            forceField["surface"]["patchesTopology"] = {}

            forceField["surface"]["patchesTopology"]["structure"] = {}
            forceField["surface"]["patchesTopology"]["structure"]["labels"] = ["id", "type", "parentId"]
            forceField["surface"]["patchesTopology"]["structure"]["data"]   = []

            for i in range(self.nMonomers):
                forceField["surface"]["patchesTopology"]["structure"]["data"].append([i,"L",i])

            forceField["surface"]["patchesTopology"]["forceField"] = {}

            forceField["surface"]["patchesTopology"]["forceField"]["linker"]={}
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["type"]       =  ["SurfacePatches", "Linker"]
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["parameters"] =  {"surfacePosition":self.plateBottom}
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["labels"]     =  ["name", "epsilon", "sigma"]
            forceField["surface"]["patchesTopology"]["forceField"]["linker"]["data"]       =  [["L",self.El,self.Sl]]

        ##############################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)

    def processSelection(self,**params):

        sel = []
        if "particleId" in params:
            sel += params["particleId"]
        return sel
