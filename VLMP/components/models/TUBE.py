import sys, os
import itertools

import copy

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

    def __generateRandomPositions(self,monomersPositions = [],monomersOrientations = []):

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

            x=-boxX+self.monomerRadius+(n+1)*2.0*self.monomerRadius
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

        alpha = np.sqrt(self.theta0T*self.theta0T+self.phi0T*self.phi0T)

        cp = self.theta0T/alpha;
        sp = self.phi0T/alpha;

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
                z=(self.theta0T/(self.theta0T*self.theta0T+self.phi0T*self.phi0T)-1.0)

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
                                                "nMonomers","box",
                                                "monomerRadius","patchRadius",
                                                "pitch","monomersPerTurn",
                                                "epsilon_mm",
                                                "EbT","rcT",
                                                "KbT","KaT","KdT",
                                                "stiffnessFactorT",
                                                "EbL","rcL",
                                                "KbL","KaL","KdL",
                                                "theta0L",
                                                "phi0L",
                                                "stiffnessFactorL"},
                         requiredParameters  = {"nMonomers","box",
                                                "pitch","monomersPerTurn",
                                                "epsilon_mm",
                                                "EbT","rcT",
                                                "KbT","KaT","KdT",
                                                "EbL","rcL",
                                                "KbL","KaL","KdL",
                                                "theta0L"},
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

        self.pitch           = params["pitch"]
        self.monomersPerTurn = params["monomersPerTurn"]

        self.epsilon_mm = params["epsilon_mm"]

        #Transversal

        self.EbT = params["EbT"]
        self.rcT = params["rcT"]

        self.KbT = params["KbT"]
        self.KaT = params["KaT"]
        self.KdT = params["KdT"]

        stiffnessFactor = params.get("stiffnessFactorT",1.0)
        if stiffnessFactor != 1.0:
            self.logger.info(f"[TUBE] Applying stiffness factor (T) {stiffnessFactor}")
            self.KaT*=stiffnessFactor
            self.KbT*=stiffnessFactor

            self.logger.info(f"[TUBE] Kt theta after stiffness factor {self.KaT}")
            self.logger.info(f"[TUBE] Kt phi after stiffness factor {self.KdT}")

        def equationSystem(vars, nc, pitch, sigma):
            phi0, theta0 = vars

            a = pitch/(np.pi*2)
            b = nc*sigma/(np.pi*2)

            R = np.sqrt(b**2-a**2)

            alpha = np.sqrt(phi0**2+theta0**2)

            eq1 = phi0/alpha - pitch/(sigma*nc)
            eq2 = np.cos(alpha)*(theta0**2/alpha**2)+phi0**2/alpha**2-(a**2+np.cos(2*np.pi/nc)*(R**2))/(a**2+R**2)

            return [eq1, eq2]

        self.phi0T,self.theta0T = root(equationSystem,
                                       [np.pi/2,np.pi/2],
                                       args=(self.monomersPerTurn,self.pitch,self.monomerRadius*2.0),tol=1e-12).x

        self.logger.info(f"[TUBE] Computing theta0T {self.theta0T}")
        self.logger.info(f"[TUBE] Computing phi0T {self.phi0T}")

        #Longitudinal

        self.EbL = params["EbL"]
        self.rcL = params["rcL"]

        self.KbL = params["KbL"]
        self.KaL = params["KaL"]
        self.KdL = params["KdL"]

        stiffnessFactor = params.get("stiffnessFactorL",1.0)
        if stiffnessFactor != 1.0:
            self.logger.info(f"[TUBE] Applying stiffness factor (L) {stiffnessFactor}")
            self.KaL*=stiffnessFactor
            self.KbL*=stiffnessFactor

            self.logger.info(f"[TUBE] Kl theta after stiffness factor {self.KaL}")
            self.logger.info(f"[TUBE] Kl phi after stiffness factor {self.KdL}")

        self.theta0L = params["theta0L"]
        self.phi0L   = params.get("phi0L",0.0)

        alpha = np.sqrt(self.theta0T**2+self.phi0T**2)

        cp = self.theta0T/alpha;
        sp = self.phi0T/alpha;

        ca = np.cos(alpha);
        sa = np.sin(alpha);

        rot = np.asarray([[ca*cp ,-sa ,-ca*sp],
                          [sp    ,0.0 , cp],
                          [-sa*cp,-ca , sa*sp]])

        vector = np.asarray([0,1,0])*self.monomerRadius*2.0


        self.Lplus  = np.dot(rot.T,vector)*self.monomerRadius
        self.Lminus = -copy.deepcopy(self.Lplus)

        ##############################################

        self.logger.info(f"[TUBE] Generating TUBE model with {self.nMonomers} monomers")

        if   self.init == "random":
            self.monomersPositions,self.monomersOrientations = self.__generateRandomPositions()
        elif self.init == "line":
            self.monomersPositions,self.monomersOrientations = self.__generateLine()
        elif self.init == "helix":
            self.monomersPositions,self.monomersOrientations = self.__generateHelix()
        elif self.init == "tube":
            nTotalMonomers = self.nMonomers #Backup

            monomersPerTube = [0 for i in range(self.pitch)]
            n=0
            i=0
            while n < self.nMonomers:
                if i >= self.pitch:
                    i=0
                monomersPerTube[i]+=1
                n+=1
                i+=1

            self.monomersPositions = np.zeros((0,3))
            self.monomersOrientations = np.zeros((0,4))
            for i in range(self.pitch):
                self.nMonomers = monomersPerTube[i]
                mPos,mOri = self.__generateHelix(yOffset=i*2.0*self.monomerRadius,center=False)
                self.monomersPositions    = np.vstack((self.monomersPositions,mPos))
                self.monomersOrientations = np.vstack((self.monomersOrientations,mOri))

            centroid = np.mean(self.monomersPositions,axis=0)
            self.monomersPositions-=centroid

            self.nMonomers = nTotalMonomers #Restore
        elif self.init == "nucleus":
            nTotalMonomers = self.nMonomers #Backup
            nucleusMonomers = self.monomersPerTurn*2*self.pitch

            if nucleusMonomers > self.nMonomers:
                logging.error(f"[TUBE] Nucleus monomers {nucleusMonomers} larger than total monomers {self.nMonomers}")
                raise Exception("Nucleus monomers larger than total monomers")

            monomersPerTube = [0 for i in range(self.pitch)]
            n=0
            i=0
            while n < nucleusMonomers:
                if i >= self.pitch:
                    i=0
                monomersPerTube[i]+=1
                n+=1
                i+=1

            self.monomersPositions = np.zeros((0,3))
            self.monomersOrientations = np.zeros((0,4))
            for i in range(self.pitch):
                self.nMonomers = monomersPerTube[i]
                mPos,mOri = self.__generateHelix(yOffset=i*2.0*self.monomerRadius,center=False)
                self.monomersPositions    = np.vstack((self.monomersPositions,mPos))
                self.monomersOrientations = np.vstack((self.monomersOrientations,mOri))

            centroid = np.mean(self.monomersPositions,axis=0)
            self.monomersPositions-=centroid

            self.nMonomers = nTotalMonomers - nucleusMonomers

            self.monomersPositions,self.monomersOrientations = self.__generateRandomPositions(self.monomersPositions.tolist(),
                                                                                              self.monomersOrientations.tolist())

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

        forceField["tube"]={}
        forceField["tube"]["type"]       = ["PatchyParticles","DynamicallyBondedPatchyParticles"]

        forceField["tube"]["patchesState"]={}
        forceField["tube"]["patchesState"]["labels"]=["id","position"]
        forceField["tube"]["patchesState"]["data"]  =[]

        for i in range(self.nMonomers):

            #Transversal
            index=i*4
            p = [-self.monomerRadius,0.0,0.0]
            forceField["tube"]["patchesState"]["data"].append([int(index  ),list(p)])
            p = [ self.monomerRadius,0.0,0.0]
            forceField["tube"]["patchesState"]["data"].append([int(index+1),list(p)])

            #Longitudinal
            index=i*4
            p = copy.deepcopy(self.Lplus)
            forceField["tube"]["patchesState"]["data"].append([int(index+2),list(p)])
            p = copy.deepcopy(self.Lminus)
            forceField["tube"]["patchesState"]["data"].append([int(index+3),list(p)])

        forceField["tube"]["patchesGlobal"]={}
        forceField["tube"]["patchesGlobal"]["fundamental"] = {}
        forceField["tube"]["patchesGlobal"]["fundamental"]["type"]      = ["Fundamental","DynamicallyBondedPatchyParticles"]
        forceField["tube"]["patchesGlobal"]["fundamental"]["parameters"]={"energyThreshold":0.0}

        forceField["tube"]["patchesGlobal"]["types"]  = {}
        forceField["tube"]["patchesGlobal"]["types"]["type"]   = ["Types","Basic"]
        forceField["tube"]["patchesGlobal"]["types"]["labels"] = ["name", "mass", "radius", "charge"]
        forceField["tube"]["patchesGlobal"]["types"]["data"]   = [["St",0.0,self.patchRadius,0.0],
                                                                  ["Et",0.0,self.patchRadius,0.0],
                                                                  ["Sl",0.0,self.patchRadius,0.0],
                                                                  ["El",0.0,self.patchRadius,0.0]]

        forceField["tube"]["patchesTopology"]={}

        forceField["tube"]["patchesTopology"]["structure"]={}
        forceField["tube"]["patchesTopology"]["structure"]["labels"] = ["id", "type", "parentId"]
        forceField["tube"]["patchesTopology"]["structure"]["data"]   = []

        for i in range(self.nMonomers):
            index=i*4
            forceField["tube"]["patchesTopology"]["structure"]["data"].append([index  ,"Et",i])
            forceField["tube"]["patchesTopology"]["structure"]["data"].append([index+1,"St",i])
            forceField["tube"]["patchesTopology"]["structure"]["data"].append([index+2,"El",i])
            forceField["tube"]["patchesTopology"]["structure"]["data"].append([index+3,"Sl",i])

        forceField["tube"]["patchesTopology"]["forceField"] = {}

        forceField["tube"]["patchesTopology"]["forceField"]["groups"] = {}
        forceField["tube"]["patchesTopology"]["forceField"]["groups"]["type"] = ["Groups","GroupsList"]
        forceField["tube"]["patchesTopology"]["forceField"]["groups"]["parameters"] = {}
        forceField["tube"]["patchesTopology"]["forceField"]["groups"]["labels"] = ["name", "type", "selection"]
        forceField["tube"]["patchesTopology"]["forceField"]["groups"]["data"]   = [
            ["trans","Types",["St","Et"]],
            ["long","Types",["Sl","El"]]
        ]


        #Verlet list
        forceField["tube"]["patchesTopology"]["forceField"]["verletList"]={}
        forceField["tube"]["patchesTopology"]["forceField"]["verletList"]["type"]       =  ["VerletConditionalListSet", "interDifferentType"]
        forceField["tube"]["patchesTopology"]["forceField"]["verletList"]["parameters"] =  {"cutOffVerletFactor":3.0}

        forceField["tube"]["patchesTopology"]["forceField"]["transversal"]={}
        forceField["tube"]["patchesTopology"]["forceField"]["transversal"]["type"]       =  ["NonBondedPatches", "Helix"]
        forceField["tube"]["patchesTopology"]["forceField"]["transversal"]["parameters"] =  {"condition":"inter",
                                                                                             "startType":"St",
                                                                                             "endType":"Et",
                                                                                             "group":"trans"}
        forceField["tube"]["patchesTopology"]["forceField"]["transversal"]["labels"]     =  ["name_i", "name_j", "Eb", "Kb", "Ka", "Kd", "rc", "theta0", "phi0"]
        forceField["tube"]["patchesTopology"]["forceField"]["transversal"]["data"]       =  [["St", "Et",
                                                                                              self.EbT,
                                                                                              self.KbT, self.KaT, self.KdT,
                                                                                              self.rcT,
                                                                                              self.theta0T, self.phi0T]]
        forceField["tube"]["patchesTopology"]["forceField"]["longitudinal"]={}
        forceField["tube"]["patchesTopology"]["forceField"]["longitudinal"]["type"]       =  ["NonBondedPatches", "Helix"]
        forceField["tube"]["patchesTopology"]["forceField"]["longitudinal"]["parameters"] =  {"condition":"inter",
                                                                                              "startType":"Sl",
                                                                                              "endType":"El",
                                                                                              "group":"long"}
        forceField["tube"]["patchesTopology"]["forceField"]["longitudinal"]["labels"]     =  ["name_i", "name_j", "Eb", "Kb", "Ka", "Kd", "rc", "theta0", "phi0"]
        forceField["tube"]["patchesTopology"]["forceField"]["longitudinal"]["data"]       =  [["Sl", "El",
                                                                                              self.EbL,
                                                                                              self.KbL, self.KaL, self.KdL,
                                                                                              self.rcL,
                                                                                              self.theta0L, self.phi0L]]

        ##############################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)

    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel
