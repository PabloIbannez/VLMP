import sys, os
import itertools

import copy

import logging

from . import modelBase
from ...utils.geometry import getEx

import random

import orthopoly

import numpy as np
from scipy.spatial import cKDTree

from pyquaternion import Quaternion

from scipy.spatial.transform import Rotation as R
from scipy.optimize import root


class LEMON(modelBase):
    """
    Component name: LEMON
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 15/06/2023

    """

    def __generateHelix(self,yOffset=0.0,center=True,monomersOffset=0):

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

        for n in range(self.nMonomers+monomersOffset):
            if n > monomersOffset:
                self.logger.debug(f"[LEMON] Adding monomer {n}")

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

        #Remove the first monomersOffset monomers
        monomersPositions    = monomersPositions[monomersOffset:]
        monomersOrientations = monomersOrientations[monomersOffset:]

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
                                                "Eb","rc",
                                                "Kb","Ka","Kd",
                                                "stiffnessFactor",
                                                "epsilonLipids",
                                                "muLipids",
                                                "chiLipids",
                                                "thetaLipids"},
                         requiredParameters  = {"nMonomers","box",
                                                "pitch","monomersPerTurn",
                                                "Eb","rc",
                                                "Kb","Ka","Kd",
                                                "epsilonLipids",
                                                "muLipids",
                                                "chiLipids",
                                                "thetaLipids"},
                         definedSelections   = {"particleId"},
                         **params)

        self.logger = logging.getLogger("VLMP")

        ############################################################
        ####################  Model Parameters  ####################
        ############################################################

        self.kT = self.getUnits().getConstant("kT")

        self.init      = params.get("init","tube")

        self.nMonomers      = params["nMonomers"]

        self.box = params["box"]

        self.monomerRadius = params.get("monomerRadius",0.5)
        self.patchRadius   = params.get("patchRadius",0.1)

        self.pitch           = params["pitch"]
        self.monomersPerTurn = params["monomersPerTurn"]

        self.Eb = params["Eb"]
        self.rc = params["rc"]

        self.Kb = params["Kb"]
        self.Ka = params["Ka"]
        self.Kd = params["Kd"]

        stiffnessFactor = params.get("stiffnessFactor",1.0)
        if stiffnessFactor != 1.0:
            self.logger.info(f"[LEMON] Applying stiffness factor{stiffnessFactor}")
            self.Ka*=stiffnessFactor
            self.Kb*=stiffnessFactor

            self.logger.info(f"[LEMON] Kt theta after stiffness factor {self.Ka}")
            self.logger.info(f"[LEMON] Kt phi after stiffness factor {self.Kd}")

        def equationSystem(vars, nc, pitch, sigma):
            phi0, theta0 = vars

            a = pitch/(np.pi*2)
            b = nc*sigma/(np.pi*2)

            R = np.sqrt(b**2-a**2)

            alpha = np.sqrt(phi0**2+theta0**2)

            eq1 = phi0/alpha - pitch/(sigma*nc)
            eq2 = np.cos(alpha)*(theta0**2/alpha**2)+phi0**2/alpha**2-(a**2+np.cos(2*np.pi/nc)*(R**2))/(a**2+R**2)

            return [eq1, eq2]

        self.phi0,self.theta0 = root(equationSystem,
                                     [np.pi/2,np.pi/2],
                                     args=(self.monomersPerTurn,self.pitch,self.monomerRadius*2.0),tol=1e-12).x

        self.logger.info(f"[LEMON] Computing theta0 {self.theta0}")
        self.logger.info(f"[LEMON] Computing phi0 {self.phi0}")

        ##############################################

        #Lipids
        self.epsilonLipids = params["epsilonLipids"]
        self.muLipids      = params["muLipids"]
        self.chiLipids     = params["chiLipids"]
        self.thetaLipids   = params["thetaLipids"]

        self.logger.info(f"[LEMON] Epilson lipids {self.epsilonLipids}")
        self.logger.info(f"[LEMON] Mu lipids {self.muLipids}")
        self.logger.info(f"[LEMON] Chi lipids {self.chiLipids}")
        self.logger.info(f"[LEMON] Theta lipids {self.thetaLipids}")

        ##############################################

        self.logger.info(f"[LEMON] Generating LEMON model with {self.nMonomers} monomers")

        if self.init == "tube":
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

            monomersPerOffset = int(self.monomersPerTurn/self.pitch)

            self.monomersPositions    = np.zeros((0,3))
            self.monomersOrientations = np.zeros((0,4))
            self.monomersHelixId      = np.zeros((0,1),dtype=int)
            for i in range(self.pitch):
                self.nMonomers = monomersPerTube[i]
                mPos,mOri = self.__generateHelix(yOffset=i*2.0*self.monomerRadius,center=False,monomersOffset=self.monomersPerTurn-monomersPerOffset*i)
                self.monomersPositions    = np.vstack((self.monomersPositions,mPos))
                self.monomersOrientations = np.vstack((self.monomersOrientations,mOri))
                #i is the helix id
                self.monomersHelixId      = np.vstack((self.monomersHelixId,np.ones((self.nMonomers,1),dtype=int)*i))


            centroid = np.mean(self.monomersPositions,axis=0)
            self.monomersPositions-=centroid

            self.nMonomers = nTotalMonomers #Restore
        else:
            self.logger.error(f"[LEMON] Init mode {self.init} is not avaible")
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
            #modelId is the helix id
            structure["data"].append([int(i),"M",int(self.monomersHelixId[i])])

        ##############################################

        forceField = {}

        #Verlet list
        forceField["verletListParticles"]={}
        forceField["verletListParticles"]["type"]       =  ["VerletConditionalListSet", "intra_inter"]
        forceField["verletListParticles"]["parameters"] =  {"cutOffVerletFactor":1.5}

        #WCA
        forceField["MonomerMonomerIntra"]={}
        forceField["MonomerMonomerIntra"]["type"]       =  ["NonBonded", "WCAType2"]
        forceField["MonomerMonomerIntra"]["parameters"] =  {"cutOffFactor":2.5,"condition":"intra"}
        forceField["MonomerMonomerIntra"]["labels"]     =  ["name_i", "name_j", "epsilon", "sigma"]
        forceField["MonomerMonomerIntra"]["data"]       =  [["M", "M", 1.0, 2.0*self.monomerRadius]]

        #ATZBERGER
        forceField["MonomerMonomerInter"] = {}
        forceField["MonomerMonomerInter"]["type"] = ["NonBonded", "Atzberger"]
        forceField["MonomerMonomerInter"]["parameters"] = {"condition":"inter","axis":[0.0,-1.0,0.0]}
        forceField["MonomerMonomerInter"]["labels"] = ["name_i", "name_j", "radius", "epsilon", "mu", "chi", "theta"]
        forceField["MonomerMonomerInter"]["data"]   = [
            ["M","M",self.monomerRadius,self.epsilonLipids,self.muLipids,self.chiLipids,self.thetaLipids]
        ]

        ############Patches

        forceField["lemon"]={}
        forceField["lemon"]["type"]       = ["PatchyParticles","DynamicallyBondedPatchyParticles"]

        forceField["lemon"]["patchesState"]={}
        forceField["lemon"]["patchesState"]["labels"]=["id","position"]
        forceField["lemon"]["patchesState"]["data"]  =[]

        for i in range(self.nMonomers):

            index=i*2
            p = [-self.monomerRadius,0.0,0.0]
            forceField["lemon"]["patchesState"]["data"].append([int(index  ),list(p)])
            p = [ self.monomerRadius,0.0,0.0]
            forceField["lemon"]["patchesState"]["data"].append([int(index+1),list(p)])

        forceField["lemon"]["patchesGlobal"]={}
        forceField["lemon"]["patchesGlobal"]["fundamental"] = {}
        forceField["lemon"]["patchesGlobal"]["fundamental"]["type"]      = ["Fundamental","DynamicallyBondedPatchyParticles"]
        forceField["lemon"]["patchesGlobal"]["fundamental"]["parameters"]={"energyThreshold":0.0}

        forceField["lemon"]["patchesGlobal"]["types"]  = {}
        forceField["lemon"]["patchesGlobal"]["types"]["type"]   = ["Types","Basic"]
        forceField["lemon"]["patchesGlobal"]["types"]["labels"] = ["name", "mass", "radius", "charge"]
        forceField["lemon"]["patchesGlobal"]["types"]["data"]   = [["S",0.0,self.patchRadius,0.0],
                                                                      ["E",0.0,self.patchRadius,0.0]]

        forceField["lemon"]["patchesTopology"]={}

        forceField["lemon"]["patchesTopology"]["structure"]={}
        forceField["lemon"]["patchesTopology"]["structure"]["labels"] = ["id", "type", "parentId"]
        forceField["lemon"]["patchesTopology"]["structure"]["data"]   = []

        for i in range(self.nMonomers):
            index=i*2
            forceField["lemon"]["patchesTopology"]["structure"]["data"].append([index  ,"E",i])
            forceField["lemon"]["patchesTopology"]["structure"]["data"].append([index+1,"S",i])

        forceField["lemon"]["patchesTopology"]["forceField"] = {}

        #Verlet list
        forceField["lemon"]["patchesTopology"]["forceField"]["verletList"]={}
        forceField["lemon"]["patchesTopology"]["forceField"]["verletList"]["type"]       =  ["VerletConditionalListSet", "interDifferentType"]
        forceField["lemon"]["patchesTopology"]["forceField"]["verletList"]["parameters"] =  {"cutOffVerletFactor":3.0}

        forceField["lemon"]["patchesTopology"]["forceField"]["transversal"]={}
        forceField["lemon"]["patchesTopology"]["forceField"]["transversal"]["type"]       =  ["NonBondedPatches", "Helix"]
        forceField["lemon"]["patchesTopology"]["forceField"]["transversal"]["parameters"] =  {"condition":"inter"}

        forceField["lemon"]["patchesTopology"]["forceField"]["transversal"]["labels"]     =  ["name_i", "name_j", "Eb", "Kb", "Ka", "Kd", "rc", "theta0", "phi0"]
        forceField["lemon"]["patchesTopology"]["forceField"]["transversal"]["data"]       =  [["S", "E",
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
