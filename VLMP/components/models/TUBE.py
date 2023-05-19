import sys, os
import itertools

import logging

from . import modelBase
from ...utils.utils import getEx

import random

import orthopoly

import numpy as np
from scipy.spatial import cKDTree

from pyquaternion import Quaternion

from scipy.spatial.transform import Rotation as R
from scipy.optimize import root


class TUBE(modelBase):
    """
    Component name: TUBE
    Component type: model

    Author: Pablo Ibáñez-Freire and Pablo Palacios-Alonso
    Date: 19/05/2023

    Polimerization model for a tube.

    """

    def __generateRandomPositions(self):
        monomersPositions    = []
        monomersOrientations = []

        boxX,boxY,boxZ = [b/2.0 for b in self.box]

        n=1
        while(n<=self.nMonomers):
            self.logger.debug(f"[TUBE] Trying to add monomer {n}")

            x=np.random.uniform(low=-boxX,high=boxX)
            y=np.random.uniform(low=-boxY,high=boxY)
            z=np.random.uniform(low=-boxZ,high=boxZ)

            currentMonomerPosition = np.asarray([x,y,z])

            if monomersPositions:
                minDst,minDstIndex = cKDTree(monomersPositions).query(currentMonomerPosition, 1)
            else:
                minDst = np.inf

            if minDst > 1.5*(2.0*self.monomerRadius):
                monomersPositions.append(currentMonomerPosition)
                q=Quaternion.random()
                q0,q1,q2,q3 = q
                monomersOrientations.append(np.asarray([q0,q1,q2,q3]))
                self.logger.debug(f"[TUBE] Added monomer {n}")
                n=n+1


        return np.asarray(monomersPositions),np.asarray(monomersOrientations)

    def __generateLine(self):
        monomersPositions    = []
        monomersOrientations = []

        boxX,boxY,boxZ = [b/2.0 for b in self.box]

        for n in range(self.nMonomers):
            self.logger.debug(f"[TUBE] Trying to add monomer {n}")

            x=-boxX+self.monomerRadius+(n+1)*2.2*self.monomerRadius
            y=0.0
            z=0.0

            currentMonomerPosition = np.asarray([x,y,z])

            monomersPositions.append(currentMonomerPosition)
            monomersOrientations.append(np.asarray([1.0,0.0,0.0,0.0]))

        centroid = np.mean(monomersPositions,axis=0)
        monomersPositions-=centroid

        return np.asarray(monomersPositions),np.asarray(monomersOrientations)

    def __generateHelix(self,yOffset=0.0,center=True):

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
            self.logger.debug(f"[TUBE] Adding monomer {n}")

            if n==0:
                x=0.0
                y=-boxY+sigma+yOffset
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

                q1,q2,q3,q0 = r_current.as_quat()

                x,y,z = monomersPositions[-1]+0.5*sigma*(getEx(monomersOrientations[-1])+getEx([q0,q1,q2,q3]))


            currentMonomerPosition = np.asarray([x,y,z])
            currentMonomerOrientation = np.asarray([q0,q1,q2,q3])

            monomersPositions.append(currentMonomerPosition)
            monomersOrientations.append(currentMonomerOrientation)

        if(center):
            centroid = np.mean(monomersPositions,axis=0)
            monomersPositions-=centroid

        return np.asarray(monomersPositions),np.asarray(monomersOrientations)

    def __getMonomerConnections(self,position,orientation):
        connectionStart = position-self.monomerRadius*getEx(orientation)
        connectionEnd   = position+self.monomerRadius*getEx(orientation)

        return connectionStart,connectionEnd

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"mode","init",
                                                "helixPerTube",
                                                "nMonomers","box",
                                                "monomerRadius","patchRadius",
                                                "epsilon_mm",
                                                "Eb","rc",
                                                "theta0","phi0",
                                                "Kb","Ka","Kd",
                                                "stiffnessFactor"},
                         requiredParameters  = {"nMonomers","box",
                                                "epsilon_mm",
                                                "Eb","rc",
                                                "theta0","phi0",
                                                "Kb","Ka","Kd"},
                         definedSelections   = {"particleId"},
                         **params)

        self.logger = logging.getLogger("VLMP")

        ############################################################
        ####################  Model Parameters  ####################
        ############################################################

        self.kT = self.getUnits().getConstant("kT")

        self.init      = params.get("init","random")

        self.nMonomers      = params["nMonomers"]

        self.box = params["box"]

        self.monomerRadius = params.get("monomerRadius",0.5)
        self.patchRadius   = params.get("patchRadius",0.1)

        self.epsilon_mm = params["epsilon_mm"]

        self.Eb = params["Eb"]
        self.rc = params["rc"]

        stiffnessFactor = params.get("stiffnessFactor",1.0)

        self.theta0 = params["theta0"]
        self.phi0   = params["phi0"]

        self.Kb = params["Kb"]
        self.Ka = params["Ka"]
        self.Kd = params["Kd"]

        if stiffnessFactor != 1.0:
            self.logger.info(f"[TUBE] Applying stiffness factor {stiffnessFactor}")
            self.Ka*=stiffnessFactor
            self.Kd*=stiffnessFactor

            self.logger.info(f"[TUBE] K theta after stiffness factor {self.Ka}")
            self.logger.info(f"[TUBE] K phi after stiffness factor {self.Kd}")

        if self.Kb < 0 or self.Ka < 0 or self.Kd < 0:
            self.logger.error(f"[TUBE] Negative spring constant: Kb {self.Kb} Ka {self.Ka} Kd {self.Kd}")
            raise Exception("Negative spring constant")

        ##############################################

        self.logger.info(f"[TUBE] Generating TUBE model with {self.nMonomers} monomers")

        if   self.init == "random":
            self.monomersPositions,self.monomersOrientations = self.__generateRandomPositions()
        elif self.init == "line":
            self.monomersPositions,self.monomersOrientations = self.__generateLine()
        elif self.init == "helix":
            self.monomersPositions,self.monomersOrientations = self.__generateHelix()
        elif self.init == "tube":
            if "helixPerTube" not in params:
                self.logger.error(f"[TUBE] Missing parameter helixPerTube. Required for init tube")
                raise Exception("Missing parameter")
            helixPerTube = params["helixPerTube"]
            nTotalMonomers = self.nMonomers #Backup

            monomersPerTube = [0 for i in range(helixPerTube)]
            n=0
            i=0
            while n < self.nMonomers:
                if i >= helixPerTube:
                    i=0
                monomersPerTube[i]+=1
                n+=1
                i+=1

            self.monomersPositions = np.zeros((0,3))
            self.monomersOrientations = np.zeros((0,4))
            for i in range(helixPerTube):
                self.nMonomers = monomersPerTube[i]
                mPos,mOri = self.__generateHelix(yOffset=i*2.0*self.monomerRadius,center=False)
                self.monomersPositions    = np.vstack((self.monomersPositions,mPos))
                self.monomersOrientations = np.vstack((self.monomersOrientations,mOri))

            centroid = np.mean(self.monomersPositions,axis=0)
            self.monomersPositions-=centroid

            self.nMonomers = nTotalMonomers #Restore
        else:
            self.logger.error(f"[TUBE] Init mode {self.init} is not avaible")
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
        forceField["helix"]["patchesGlobal"]["parameters"]={"energyThreshold":0.0}
        forceField["helix"]["patchesGlobal"]["labels"] = ["name", "mass", "radius", "charge"]
        forceField["helix"]["patchesGlobal"]["data"]   = [["S",0.0,self.patchRadius,0.0],
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

        ##############################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)

    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel
