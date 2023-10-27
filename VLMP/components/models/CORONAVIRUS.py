import sys, os
import json

import copy
import itertools

import logging

import random

from scipy.spatial import cKDTree

import numpy as np
import orthopoly

from . import modelBase

from ...utils.input import getLabelIndex

from ...utils.geometry import quaternionFromVectors
from ...utils.geometry import getEz

from scipy.spatial.transform import Rotation as R

class CORONAVIRUS(modelBase):
    """
    Component name: CORONAVIRUS
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 4/04/2023

    Coronoavirus model

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"nLipids",
                                                "lipidRadius",
                                                "vesicleRadius",
                                                "center",
                                                "nSpikes",
                                                "epsilonLipids_kT",
                                                "muLipids","chiLipids",
                                                "thetaLipids",
                                                "epsilonLipidLipidWithProtein_kT",
                                                "muLipidLipidWithProtein","chiLipidLipidWithProtein",
                                                "thetaLipidLipidWithProtein",
                                                "epsilonLipidWithProtein_kT",
                                                "muLipidWithProtein","chiLipidWithProtein",
                                                "thetaLipidWithProtein",
                                                "proteinProteinEpsilon_kT",
                                                "proteinLipidEpsilon_kT",
                                                "proteinSurfaceEpsilon_kT",
                                                "proteinPeakSurfaceEpsilon_kT",
                                                "peakProteins",
                                                "lipidSurfaceEpsilon_kT",
                                                "surface",
                                                "surfacePosition",
                                                "inputModelData"},
                         requiredParameters  = set(),
                         definedSelections   = {"particleId","type"},
                         **params)

        self.logger = logging.getLogger("VLMP")

        ############################################################
        ############################################################
        ############################################################

        units = self.getUnits()

        if units.getName() != "KcalMol_A":
            self.logger.error(f"[CORONAVIRUS] Units are not set correctly. "
                              f"Please set units to \"KcalMol_A\" (selected: {units.getName()})")
            raise Exception("Not correct units")

        ########################################################

        self.nLipids     = params.get("nLipids",1501)
        self.lipidRadius = params.get("lipidRadius",18.0)
        self.vesRadius   = params.get("vesicleRadius",400.0)

        self.center      = params.get("center",[0.0,0.0,0.0])

        self.nSpikes     = params.get("nSpikes",0)

        self.epsilonLipids = params.get("epsilonLipids_kT",5.0)
        self.muLipids      = params.get("muLipids",3.0)
        self.chiLipids     = params.get("chiLipids",7.0)
        self.thetaLipids   = params.get("thetaLipids",0.0)

        self.epsilonLipidLipidWithProtein = params.get("epsilonLipidLipidWithProtein_kT",self.epsilonLipids)
        self.muLipidLipidWithProtein      = params.get("muLipidLipidWithProtein",self.muLipids)
        self.chiLipidLipidWithProtein     = params.get("chiLipidLipidWithProtein",self.chiLipids)
        self.thetaLipidLipidWithProtein   = params.get("thetaLipidLipidWithProtein",self.thetaLipids)

        self.epsilonLipidWithProtein = params.get("epsilonLipidWithProtein_kT",self.epsilonLipids)
        self.muLipidWithProtein      = params.get("muLipidWithProtein",self.muLipids)
        self.chiLipidWithProtein     = params.get("chiLipidWithProtein",self.chiLipids)
        self.thetaLipidWithProtein   = params.get("thetaLipidWithProtein",self.thetaLipids)

        self.proteinProteinEpsilon = params.get("proteinProteinEpsilon_kT",1.0)
        self.proteinLipidEpsilon   = params.get("proteinLipidEpsilon_kT",1.0)

        self.proteinSurfaceEpsilon     = params.get("proteinSurfaceEpsilon_kT",1.0)
        self.proteinPeakSurfaceEpsilon = params.get("proteinPeakSurfaceEpsilon_kT",self.proteinSurfaceEpsilon)

        self.peakProteins = params.get("peakProtein",["S10"])

        self.lipidSurfaceEpsilon = params.get("lipidSurfaceEpsilon_kT",1.0)

        self.epsilonLipids                *= units.getConstant("kT")
        self.epsilonLipidLipidWithProtein *= units.getConstant("kT")
        self.epsilonLipidWithProtein      *= units.getConstant("kT")
        self.proteinProteinEpsilon        *= units.getConstant("kT")
        self.proteinLipidEpsilon          *= units.getConstant("kT")
        self.proteinSurfaceEpsilon        *= units.getConstant("kT")
        self.proteinPeakSurfaceEpsilon    *= units.getConstant("kT")
        self.lipidSurfaceEpsilon          *= units.getConstant("kT")

        self.surface = params.get("surface",False)
        if self.surface:
            self.surfacePosition = params.get("surfacePosition",0.0)
        if "surfacePosition" in params and not self.surface:
            self.logger.error(f"[CORONAVIRUS] surfacePosition is set but surface is not set to True")
            raise Exception("Error processing input parameters")

        self.modelData = params.get("inputModelData","./data/CORONAVIRUS.json")
        self.modelData = os.path.join(os.path.dirname(os.path.realpath(__file__)),self.modelData)

        with open(self.modelData,"r") as f:
            self.model = json.load(f)

        ########################################################

        self.__generateCoordinatesAndTopology()

    def processSelection(self,**params):

        sel = set()

        if "particleId" in params:
            sel.add(params["particleId"])

        if "type" in params:
            structure = self.getStructure()
            typeIndex = getLabelIndex("type"  ,structure["labels"])

            if params["type"] == "lipids":
                for d in structure["data"]:
                    if d[typeIndex] in ["LV","LP"]:
                        sel.add(d[0])
            elif params["type"] == "proteins":
                for d in structure["data"]:
                    if d[typeIndex] not in ["LV","LP"]:
                        sel.add(d[0])
            else:
                self.logger.error(f"[CORONAVIRUS] Unknown type {params['type']}")
                raise Exception("Unknown type")

        return list(sel)

    def __generateSphere(self,N,radius):

        if not N%2:
            self.logger.error(f"[CORONAVIRUS] The number of lipids must be odd, but is: {N}")
            raise Exception("The number of lipids must be odd")

        theta,phi = orthopoly.spherical_harmonic.grid_fibonacci(N)
        r=np.asarray([radius]*N)

        positions = np.asarray(orthopoly.spherical_harmonic.sph2cart(r, theta, phi)).T

        orientations = []
        for i,pos in enumerate(positions):

            x,y,z = pos

            q = quaternionFromVectors(np.asarray([0.0,0.0,1.0]),pos)
            orientations.append(q)

        self.lipidsIds   = np.arange(0,N)
        self.lipidsTypes = np.full((N,1),"LV")

        return positions,np.asarray(orientations)

    def __getProteinMaxRadius(self):
        # Load spike positions
        pTypes = self.spikeModel["particleTypes"]

        radiusIndex = getLabelIndex("radius",pTypes["labels"])
        radii = np.asarray([x[radiusIndex] for x in pTypes["data"]])

        r = np.amax(radii)

        self.logger.debug(f"[CORONAVIRUS] Max radius: {r}")

        return r

    def __addSpike(self):
        #Last spike bead is removed, it is considred to be a lipid

        added = False

        spikeCoordTemplate     = self.spikeModel["coordinates"]
        spikeStructureTemplate = self.spikeModel["structure"]

        spikeBondsTemplate       = self.spikeModel["bonds"]
        spikeProtAnglesTemplate  = self.spikeModel["anglesProt"]
        spikeLipidAnglesTemplate = self.spikeModel["anglesProtLipid"]

        offSet = self.lipidsPositions.shape[0]+self.spikePositions.shape[0]

        #Add positions
        while(not added):
            self.logger.debug(f"[CORONAVIRUS] Trying to add the spike {self.addedSpikes+1}")

            # Select random lipid
            lipidId = random.randint(0,self.nLipids-1)

            # Load spike positions
            posIndex = getLabelIndex("positions",spikeCoordTemplate["labels"])
            currentSpikePositions = np.asarray([x[posIndex] for x in spikeCoordTemplate["data"]])

            # Aling spike
            currentSpikePositions = currentSpikePositions-currentSpikePositions[-1]

            v1 = currentSpikePositions[-2]-currentSpikePositions[-1]
            v2 = getEz(self.lipidsOrientations[lipidId])

            q0,q1,q2,q3=quaternionFromVectors(v1,v2)
            rot = R.from_quat(np.asarray([q1,q2,q3,q0]))

            currentSpikePositions = rot.apply(currentSpikePositions)
            currentSpikePositions = currentSpikePositions+self.lipidsPositions[lipidId]

            # Check if spike clash

            if self.spikePositions.any():
                minDst,minDstIndex = cKDTree(self.spikePositions).query(currentSpikePositions, 1)
                minDst = np.amin(minDst)
            else:
                minDst = np.inf

            if minDst > 1.5*(2.0*self.proteinMaxRadius):
                #Remove last
                currentSpikePositions = currentSpikePositions[:-1]

                self.spikePositions   = np.append(self.spikePositions,currentSpikePositions,axis=0)

                orientation = quaternionFromVectors(np.asarray([0.0,0.0,1.0]),currentSpikePositions[-1])
                orientation = orientation*np.ones((currentSpikePositions.shape[0],1))

                self.spikeOrientations = np.append(self.spikeOrientations,orientation,axis=0)
                added = True

        ##Add ids
        idIndex   = getLabelIndex("id"  ,spikeStructureTemplate["labels"])
        typeIndex = getLabelIndex("type",spikeStructureTemplate["labels"])

        currentIds   = [x[idIndex]   for x in spikeStructureTemplate["data"]]
        currentTypes = [x[typeIndex] for x in spikeStructureTemplate["data"]]
        #Remove last
        spikeBaseBeadId   = currentIds[-1]
        spikeBaseBeadType = currentTypes[-1]

        currentIds      = currentIds[:-1]
        currentTypes    = currentTypes[:-1]

        self.spikeIds   = np.append(self.spikeIds,np.asarray(currentIds).T.reshape(-1,1)+offSet,axis=0)
        self.spikeTypes = np.append(self.spikeTypes,np.asarray(currentTypes).T.reshape(-1,1),axis=0)

        currentMdls  = [self.addedSpikes+1]*len(currentIds)
        self.spikeMdls  = np.append(self.spikeMdls,np.asarray(currentMdls).T.reshape(-1,1),axis=0)
        #Change lipid type
        self.lipidsTypes[lipidId]="LP"

        ###########################################

        id_iIndex = getLabelIndex("id_i",spikeBondsTemplate["labels"])
        id_jIndex = getLabelIndex("id_j",spikeBondsTemplate["labels"])
        r0Index   = getLabelIndex("r0"  ,spikeBondsTemplate["labels"])

        for bnd in spikeBondsTemplate["data"]:
            id_i = bnd[id_iIndex]
            id_j = bnd[id_jIndex]
            r0   = bnd[r0Index]

            if id_i == spikeBaseBeadId:
                id_i = lipidId
            else:
                id_i += offSet

            if id_j == spikeBaseBeadId:
                id_j = lipidId
            else:
                id_j += offSet

            self.bonds.append([id_i,id_j,r0])

        ###########################################

        id_iIndex = getLabelIndex("id_i",spikeProtAnglesTemplate["labels"])
        id_jIndex = getLabelIndex("id_j",spikeProtAnglesTemplate["labels"])
        id_kIndex = getLabelIndex("id_k",spikeProtAnglesTemplate["labels"])
        nameIndex = getLabelIndex("name",spikeProtAnglesTemplate["labels"])

        for bnd in spikeProtAnglesTemplate["data"]:
            id_i = bnd[id_iIndex]
            id_j = bnd[id_jIndex]
            id_k = bnd[id_kIndex]
            name = bnd[nameIndex]

            if id_i == spikeBaseBeadId:
                id_i = lipidId
            else:
                id_i += offSet

            if id_j == spikeBaseBeadId:
                id_j = lipidId
            else:
                id_j += offSet

            if id_k == spikeBaseBeadId:
                id_k = lipidId
            else:
                id_k += offSet

            self.angProt.append([id_i,id_j,id_k,name])

        ###########################################

        id_iIndex = getLabelIndex("id_i",spikeLipidAnglesTemplate["labels"])
        id_jIndex = getLabelIndex("id_j",spikeLipidAnglesTemplate["labels"])
        nameIndex = getLabelIndex("name",spikeLipidAnglesTemplate["labels"])
        refIndex  = getLabelIndex("reference",spikeLipidAnglesTemplate["labels"])

        for bnd in spikeLipidAnglesTemplate["data"]:
            id_i = bnd[id_iIndex]
            id_j = bnd[id_jIndex]
            name = bnd[nameIndex]
            ref  = bnd[refIndex]

            if id_i == spikeBaseBeadId:
                id_i = lipidId
            else:
                id_i += offSet

            if id_j == spikeBaseBeadId:
                id_j = lipidId
            else:
                id_j += offSet

            if ref == spikeBaseBeadId:
                ref = lipidId
            else:
                ref += offSet

            self.angLipidProt.append([id_i,id_j,name,ref])

        ###########################################

        self.logger.debug(f"[CORONAVIRUS] Added spike {self.addedSpikes+1}")
        self.addedSpikes+=1

    def __addSpikes(self):
        for n in range(self.nSpikes):
            self.logger.debug(f"[CORONAVIRUS] Adding spike {n+1}/{self.nSpikes}")
            self.__addSpike()

        self.logger.debug(f"[CORONAVIRUS] SpikeIds shape:{self.spikeIds.shape}")
        self.logger.debug(f"[CORONAVIRUS] SpikeTypes shape:{self.spikeTypes.shape}")
        self.logger.debug(f"[CORONAVIRUS] SpikePositions shape:{self.spikePositions.shape}")
        self.logger.debug(f"[CORONAVIRUS] SpikeOrientations shape:{self.spikeOrientations.shape}")

    def __generateExclusions(self):

        excl = {}

        for bnd in self.bonds:
            i,j,_ = bnd
            excl[i]=[]
            excl[j]=[]
        for ang in self.angProt:
            i,j,k,_ = ang
            excl[i]=[]
            excl[j]=[]
            excl[k]=[]
        for ang in self.angLipidProt:
            i,j,_,_ = ang
            excl[i]=[]
            excl[j]=[]

        for bnd in self.bonds:
            i,j,_ = bnd
            excl[i].append(j)
            excl[j].append(i)
        for ang in self.angProt:
            i,j,k,_ = ang
            excl[i].append(j)
            excl[i].append(k)

            excl[j].append(i)
            excl[j].append(k)

            excl[k].append(i)
            excl[k].append(j)
        for ang in self.angLipidProt:
            i,j,_,_ = ang
            excl[i].append(j)
            excl[j].append(i)

        self.exclusions = {i:sorted(list(set(data))) for i,data in excl.items()}


    def __generateCoordinatesAndTopology(self):

        ########################################################
        ############# COORDINATES GENERATION STARTS ############
        ########################################################

        self.logger.info(f"[CORONAVIRUS] Generating CORONAVIRUS model with {self.nLipids} lipids "
                         f"and vesicle radius of {self.vesRadius} with {self.nSpikes} spikes")

        self.lipidsPositions,self.lipidsOrientations = self.__generateSphere(self.nLipids,
                                                                             self.vesRadius)

        #Spikes
        self.spikeModel = self.model["spike"]

        #Generate bonds with enm

        self.spikeModel["bonds"] = {}
        self.spikeModel["bonds"]["labels"] = ["id_i", "id_j", "r0"]
        self.spikeModel["bonds"]["data"]   = []

        id_index  = getLabelIndex("id"       ,self.spikeModel["coordinates"]["labels"])
        pos_index = getLabelIndex("positions",self.spikeModel["coordinates"]["labels"])

        coord = self.spikeModel["coordinates"]["data"]

        ##############################################################

        for d in self.model["spike"]["anglesProt"]["data"]:
            if d[3] == "knee":
                link1,link2,link3 = d[0],d[1],d[2]
                avoidIds = [link1,link2]
                break

        for c in coord:
            id_ = int(c[id_index][1::])
            if id_ == link1:
                link1pos = np.asarray(c[pos_index])
            if id_ == link2:
                link2pos = np.asarray(c[pos_index])
            if id_ == link3:
                link3pos = np.asarray(c[pos_index])

        self.spikeModel["bonds"]["data"].append([link1,link2,np.linalg.norm(link1pos-link2pos)])
        self.spikeModel["bonds"]["data"].append([link2,link3,np.linalg.norm(link2pos-link3pos)])

        ##############################################################

        for c1,c2 in itertools.combinations(coord,r=2):
            if(c1[id_index]==c2[id_index]):
                continue

            id1 = int(c1[id_index][1::])
            id2 = int(c2[id_index][1::])

            if id1 in avoidIds:
                continue
            if id2 in avoidIds:
                continue

            p1 = np.asarray(c1[pos_index])
            p2 = np.asarray(c2[pos_index])

            r0 = np.linalg.norm(p1-p2)

            if r0 < self.model["spike"]["parameters"]["bonds"]["bondsProtProt"]["cutOff"]:
                self.spikeModel["bonds"]["data"].append([id1,id2,r0])

        #########################

        self.proteinMaxRadius = self.__getProteinMaxRadius()

        self.addedSpikes  = 0

        self.spikeIds          = np.empty((0,1),dtype=int)
        self.spikeTypes        = np.empty((0,1),dtype=int)
        self.spikeMdls         = np.empty((0,1),dtype=int)
        self.spikePositions    = np.empty((0,3))
        self.spikeOrientations = np.empty((0,4))

        self.bonds        = []
        self.angLipidProt = []
        self.angProt      = []

        self.__addSpikes()

        #Move to center
        for p in self.lipidsPositions:
            p[0]=p[0]+self.center[0]
            p[1]=p[1]+self.center[1]
            p[2]=p[2]+self.center[2]
        for p in self.spikePositions:
            p[0]=p[0]+self.center[0]
            p[1]=p[1]+self.center[1]
            p[2]=p[2]+self.center[2]

        ##Compute initial center

        tpy2radius = {}
        for t in ["LV","LP"]:
            tpy2radius[t]=self.lipidRadius
        for t in self.model["spike"]["particleTypes"]["data"]:
            tpy2radius[t[0]]=t[2]

        minPos = float(self.lipidsPositions[0][2]-tpy2radius[self.lipidsTypes[0][0]])
        for [t],p in zip(self.lipidsTypes,self.lipidsPositions):
            v = float(p[2]-tpy2radius[t])
            minPos=min(minPos,v)
        for [t],p in zip(self.spikeTypes,self.spikePositions):
            v = float(p[2]-tpy2radius[t])
            minPos=min(minPos,v)

        if self.surface:
            surfPos = self.surfacePosition
            if(minPos < surfPos):
                trans = surfPos - minPos + 0.01
                for p in self.lipidsPositions:
                    p[2]=p[2]+trans
                for p in self.spikePositions:
                    p[2]=p[2]+trans

        #############################################################
        #############################################################
        #############################################################

        types = self.getTypes()

        tpy2radius = {}
        for t in ["LV","LP"]:
            tpy2radius[t]=self.lipidRadius
            types.addType(name=t,mass=1.0,radius=self.lipidRadius)
        for t in self.model["spike"]["particleTypes"]["data"]:
            tName,tMass,tRadius,tCharge = t
            tpy2radius[t[0]]=tRadius
            types.addType(name=tName,mass=tMass,radius=tRadius,charge=tCharge)

        state = {}

        state = {}
        state["labels"]=["id","position","direction"]
        state["data"]  =[]

        for i,p,q in zip(self.lipidsIds,self.lipidsPositions,self.lipidsOrientations):
            p=np.around(p,2)
            state["data"].append([int(i),list(p),list(q)])
        for i,p,q in zip(self.spikeIds,self.spikePositions,self.spikeOrientations):
            p=np.around(p,2)
            state["data"].append([int(i),list(p),list(q)])

        structure={}
        structure["labels"] = ["id", "type", "modelId"]
        structure["data"]   = []

        id2tpy = {}
        for id,t in zip(self.lipidsIds,self.lipidsTypes):
            id = int(id)
            t  = str(t[0])
            id2tpy[id]=t
            structure["data"].append([id,t,0])
        for id,t,m in zip(self.spikeIds,self.spikeTypes,self.spikeMdls):
            id = int(id)
            t  = str(t[0])
            id2tpy[id]=t
            structure["data"].append([id,t,int(m[0])])

        forceField = {}

        forceField["groups"] = {}
        forceField["groups"]["type"] = ["Groups","GroupsList"]
        forceField["groups"]["parameters"] = {}
        forceField["groups"]["labels"] = ["name", "type", "selection"]
        forceField["groups"]["data"]   = [
            ["pgLipids","Types",["LV","LP"]]
        ]

        self.__generateExclusions()

        forceField["verletList"] = {}
        forceField["verletList"]["type"]       = ["VerletConditionalListSet", "nonExclIntra_nonExclInter"]
        forceField["verletList"]["parameters"] = {"cutOffVerletFactor":1.2}
        forceField["verletList"]["labels"]     = ["id","id_list"]
        forceField["verletList"]["data"]       = []

        for i,excl in self.exclusions.items():
            forceField["verletList"]["data"].append([i,excl])

        #Lipids

        forceField["lipidsLipids"] = {}
        forceField["lipidsLipids"]["type"] = ["NonBonded", "Zhang"]
        forceField["lipidsLipids"]["parameters"] = {"condition":"intra","group":"pgLipids"}
        forceField["lipidsLipids"]["labels"] = ["name_i", "name_j", "radius", "epsilon", "mu", "chi", "theta"]
        forceField["lipidsLipids"]["data"]   = [
            ["LV","LV",self.lipidRadius,self.epsilonLipids,self.muLipids,self.chiLipids,self.thetaLipids],
            ["LV","LP",self.lipidRadius,self.epsilonLipidLipidWithProtein,self.muLipidLipidWithProtein,self.chiLipidLipidWithProtein,self.thetaLipidLipidWithProtein],
            ["LP","LV",self.lipidRadius,self.epsilonLipidLipidWithProtein,self.muLipidLipidWithProtein,self.chiLipidLipidWithProtein,self.thetaLipidLipidWithProtein],
            ["LP","LP",self.lipidRadius,self.epsilonLipidWithProtein,self.muLipidWithProtein,self.chiLipidWithProtein,self.thetaLipidWithProtein]
        ]

        forceField["nonPolar"] = {}
        forceField["nonPolar"]["type"] = ["NonBonded", "GeneralLennardJonesType2"]
        forceField["nonPolar"]["parameters"] = {"cutOffFactor": 2.5,"condition":"inter"}
        forceField["nonPolar"]["labels"] = ["name_i", "name_j", "epsilon", "sigma"]
        forceField["nonPolar"]["data"]   = []

        for t1 in tpy2radius.keys():
            for t2 in tpy2radius.keys():
                is1lipid = t1 in ["LV","LP"]
                is2lipid = t2 in ["LV","LP"]

                r1 = tpy2radius[t1]
                r2 = tpy2radius[t2]

                if is1lipid and is2lipid:
                    forceField["nonPolar"]["data"].append([t1,t2,0.0,0.0])
                if is1lipid and not is2lipid:
                    forceField["nonPolar"]["data"].append([t1,t2,self.proteinLipidEpsilon,r1+r2])
                if not is1lipid and is2lipid:
                    forceField["nonPolar"]["data"].append([t1,t2,self.proteinLipidEpsilon,r1+r2])
                if not is1lipid and not is2lipid:
                    forceField["nonPolar"]["data"].append([t1,t2,self.proteinProteinEpsilon,r1+r2])

        #Bonds
        if self.nSpikes > 0:

            Kpp = self.model["spike"]["parameters"]["bonds"]["bondsProtProt"]["K"]
            Kpl = self.model["spike"]["parameters"]["bonds"]["bondsLipidsProt"]["K"]

            forceField["bonds"] = {}
            forceField["bonds"]["type"]       = ["Bond2","Harmonic"]
            forceField["bonds"]["labels"]     = ["id_i","id_j","r0","K"]
            forceField["bonds"]["parameters"] = {}
            forceField["bonds"]["data"]       = []

            for i,j,r0 in self.bonds:
                if "L" in id2tpy[i] or "L" in id2tpy[j]:
                    K=Kpl
                else:
                    K=Kpp
                forceField["bonds"]["data"].append([i,j,r0,K])

            #angles
            angParam = self.model["spike"]["parameters"]["angles"]["anglesProt"]

            forceField["angProt"] = {}
            forceField["angProt"]["type"]       = ["Bond3","HarmonicAngular"]
            forceField["angProt"]["labels"]     = ["id_i","id_j","id_k","theta0","K"]
            forceField["angProt"]["parameters"] = {}
            forceField["angProt"]["data"]       = []

            for i,j,k,name in self.angProt:
                theta0 = angParam[name]["theta"]
                K      = angParam[name]["K"]
                forceField["angProt"]["data"].append([i,j,k,np.pi-np.radians(theta0),K])

            ########

            #angParam = self.model["spike"]["parameters"]["angles"]["anglesProtLipid"]

            #forceField["angLipidProt"] = {}
            #forceField["angLipidProt"]["type"]       = ["Bond2","Alignment"]
            #forceField["angLipidProt"]["labels"]     = ["id_i","id_j","theta0","K","reference"]
            #forceField["angLipidProt"]["parameters"] = {}
            #forceField["angLipidProt"]["data"]       = []

            #for i,j,name,ref in self.angLipidProt:
            #    theta0 = angParam[name]["theta"]
            #    K      = angParam[name]["K"]
            #    forceField["angLipidProt"]["data"].append([i,j,np.pi-np.radians(theta0),K,ref])

        if self.surface:
            forceField["surface"] = {}
            forceField["surface"]["type"]       = ["Surface", "SurfaceGeneralLennardJonesType2"]
            forceField["surface"]["parameters"] = {"surfacePosition":self.surfacePosition}
            forceField["surface"]["labels"] = ["name","epsilon","sigma"]
            forceField["surface"]["data"]   = []

            for t in tpy2radius.keys():
                isLipid = t in ["LV","LP"]
                r       = tpy2radius[t]

                if isLipid:
                    forceField["surface"]["data"].append([t,self.lipidSurfaceEpsilon,r])
                else:
                    isPeakProtein = t in self.peakProteins
                    if isPeakProtein:
                        forceField["surface"]["data"].append([t,self.proteinPeakSurfaceEpsilon,r])
                    else:
                        forceField["surface"]["data"].append([t,self.proteinSurfaceEpsilon,r])

        #############################################################
        #############################################################
        #############################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)
