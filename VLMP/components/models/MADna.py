import sys, os
import copy
import json

import logging

import itertools

from . import modelBase
from ...utils.input import getSubParameters

import math

import numpy as np
from scipy.spatial.transform import Rotation

class MADna(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "MADna model for DNA simulation. This model implements a coarse-grained representation
      of DNA based on the MADna force field, which provides accurate sequence-dependent
      conformational and elastic properties of double-stranded DNA. The model offers a
      balance between computational efficiency and accuracy in representing DNA structure
      and dynamics.
      <p>
      The model allows for customization of electrostatic interactions through the Debye length
      and dielectric constant parameters. The debyeFactor can be used to adjust the cutoff
      distance for these interactions.
      <p>
      A 'fast' variant of the model is available, which can be used to speed up simulations
      at the cost of some accuracy. This variant modifies how non-bonded interactions are
      computed. Non bonded interactions (WCA and Debye-Hückel) are using bonds. This means
      that the neighbor list is not used and the interactions pairs are precomputed. Thus, this approach
      is valid when beads far away in the sequence are kept separated during the simulation.
      For example, when pulling a DNA strand.
      <p>
      The model reads its core parameters from a JSON file, which can be specified using
      the inputModelData parameter. This allows for easy modification and extension of the
      model's base parameters.
      <p>
      For more details on the underlying force field, see [Assenza2022]_.",
     "parameters":{
        "sequence":{"description":"DNA sequence to be modeled. Must be a string of valid DNA bases (A, T, C, G).",
                    "type":"str"},
        "inputModelData":{"description":"Path to the JSON file containing model parameters. Allows for customization of base model parameters.",
                          "type":"str",
                          "default":"./data/MADna.json"},
        "debyeLength":{"description":"Debye length for electrostatic interactions. Controls the range of electrostatic forces.",
                       "type":"float",
                       "default":10.8},
        "dielectricConstant":{"description":"Dielectric constant of the medium. Affects the strength of electrostatic interactions.",
                              "type":"float",
                              "default":78.3},
        "debyeFactor":{"description":"Factor to scale the Debye length. Used to set the cutoff distance for electrostatic interactions.",
                       "type":"float",
                       "default":4.0},
        "variant":{"description":"Variant of the model to use. 'fast' option available for improved computational speed.",
                   "type":"str",
                   "options":["fast"],
                   "default":null}
     },
     "example":"
         {
            "type":"MADna",
            "parameters":{
                "sequence":"ATCGGATCCGAT",
                "debyeLength":10.8,
                "dielectricConstant":78.3,
                "debyeFactor":4.0,
                "variant":"fast"
            }
         }
        ",
     "references":[
         ".. [Assenza2022] Assenza, S., & Pérez, R. (2022). Accurate Sequence-Dependent Coarse-Grained Model for Conformational and Elastic Properties of Double-Stranded DNA. Journal of Chemical Theory and Computation, 18(5), 3239-3256."
     ]
    }
    """

    availableParameters = {"sequence",
                           "inputModelData",
                           "debyeLength","dielectricConstant",
                           "debyeFactor",
                           "variant"}
    requiredParameters  = {"sequence"}
    definedSelections   = {"type","strand","basePairIndex","basePairType","particleId"}

    def __alignBasePairs(self,ref,mobile):

        refSel    = ref[6:10]
        mobileSel = mobile[0:4]

        refSelCentroid    = np.mean(refSel,axis=0)
        mobileSelCentroid = np.mean(mobileSel,axis=0)

        refSel    = refSel - refSelCentroid
        mobileSel = mobileSel - mobileSelCentroid

        ##### Kabsch #####
        C = np.dot(np.transpose(mobileSel),refSel)
        V, S, W = np.linalg.svd(C)
        if (np.linalg.det(V) * np.linalg.det(W)) < 0.0:
            S[-1] = -S[-1]
            V[:, -1] = -V[:, -1]
        U = np.dot(V, W)
        ##################

        mobile = mobile.__iadd__(-mobileSelCentroid)
        mobile = np.dot(mobile,U,out=mobile)
        mobile = mobile.__iadd__(refSelCentroid)

    def __update(self,iseq,loc):

        iS_5_1 = iseq*3
        iB_5_1 = iS_5_1 + 1

        iS_5_2 = self.nAtoms - 1 - iS_5_1 - 1
        iB_5_2 = self.nAtoms - 1 - iB_5_1 + 1

        iP_1 = iS_5_1 + 2
        iP_2 = self.nAtoms - 1 - iP_1

        iS_3_1 = iS_5_1 + 3
        iB_3_1 = iS_5_1 + 4

        iS_3_2 = self.nAtoms - 1 - iS_3_1 - 1
        iB_3_2 = self.nAtoms - 1 - iB_3_1 + 1

        #print(iseq,self.nAtoms)
        #print(iS_5_1,iB_5_1,iB_5_2,iS_5_2)
        #print(" ",iP_1,iP_2)
        #print(iS_3_1,iB_3_1,iB_3_2,iS_3_2)
        #input()

        #S B 5

        if iseq==0:
            self.coordinates[iS_5_1] = loc["S_5_1"]
            self.coordinates[iB_5_1] = loc["B_5_1"]
            self.coordinates[iB_5_2] = loc["B_5_2"]
            self.coordinates[iS_5_2] = loc["S_5_2"]

            self.structure[iS_5_1] = {"type":"S","strand":1,"basePairIndex":iseq+1}
            self.structure[iB_5_1] = {"type":self.seq[iseq],"strand":1,"basePairIndex":iseq+1}
            self.structure[iB_5_2] = {"type":self.model["PAIRS"][self.seq[iseq]],"strand":2,"basePairIndex":iseq+1}
            self.structure[iS_5_2] = {"type":"S","strand":2,"basePairIndex":iseq+1}
        else:
            self.coordinates[iS_5_1] = 0.5*(loc["S_5_1"] + self.coordinates[iS_5_1])
            self.coordinates[iB_5_1] = 0.5*(loc["B_5_1"] + self.coordinates[iB_5_1])
            self.coordinates[iB_5_2] = 0.5*(loc["B_5_2"] + self.coordinates[iB_5_2])
            self.coordinates[iS_5_2] = 0.5*(loc["S_5_2"] + self.coordinates[iS_5_2])


        self.coordinates[iS_3_1] = loc["S_3_1"]
        self.coordinates[iB_3_1] = loc["B_3_1"]
        self.coordinates[iB_3_2] = loc["B_3_2"]
        self.coordinates[iS_3_2] = loc["S_3_2"]

        self.coordinates[iP_1]   = loc["P_1"]
        self.coordinates[iP_2]   = loc["P_2"]

        #######################################################################

        self.structure[iP_1]   = {"type":"P","strand":1,"basePairIndex":iseq+2}
        self.structure[iP_2]   = {"type":"P","strand":2,"basePairIndex":iseq+1} #Note P 2 belongs to previous basePair

        self.structure[iS_3_1] = {"type":"S","strand":1,"basePairIndex":iseq+2}
        self.structure[iB_3_1] = {"type":self.seq[iseq+1],"strand":1,"basePairIndex":iseq+2}
        self.structure[iB_3_2] = {"type":self.model["PAIRS"][self.seq[iseq+1]],"strand":2,"basePairIndex":iseq+2}
        self.structure[iS_3_2] = {"type":"S","strand":2,"basePairIndex":iseq+2}

        return np.asarray([self.coordinates[iS_5_1], self.coordinates[iB_5_1], self.coordinates[iB_5_2], self.coordinates[iS_5_2],
                           self.coordinates[iP_1],   self.coordinates[iP_2],
                           self.coordinates[iS_3_1], self.coordinates[iB_3_1], self.coordinates[iB_3_2], self.coordinates[iS_3_2]])


    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        units = self.getUnits()

        if units.getName() != "KcalMol_A":
            self.logger.error(f"[MADna] Units are not set correctly. Please set units to \"KcalMol_A\" (selected: {units.getName()})")
            raise Exception("Not correct units")

        ############################################################

        self.modelData = params.get("inputModelData","./data/MADna.json")
        self.modelData = os.path.join(os.path.dirname(os.path.realpath(__file__)),self.modelData)

        with open(self.modelData,"r") as f:
            self.model = json.load(f)

        self.seq    = params.get("sequence")
        self.seqLen = len(self.seq)
        self.nAtoms = self.seqLen*6-2


        self.debyeLength        = params.get("debyeLength",10.8)
        self.dielectricConstant = params.get("dielectricConstant",78.3)

        self.debyeFactor = params.get("debyeFactor",4.0)

        self.variantName, self.variantParams = getSubParameters("variant",params)
        if   self.variantName is None:
            pass
        elif self.variantName == "fast":

            variantAvailableParameters = {"fastFactor"}
            variantRequiredParameters  = set()

            for key in self.variantParams.keys():
                if key not in variantAvailableParameters:
                    self.logger.error(f"[MADna] Variant parameter {key} is not available for variant {self.variantName}")
                    raise Exception("Not correct variant parameter")

            for key in variantRequiredParameters:
                if key not in self.variantParams.keys():
                    self.logger.error(f"[MADna] Variant parameter {key} is required for variant {self.variantName}")
                    raise Exception("Not correct variant parameter")

            self.fastFactor  = params.get("fastFactor",1)
        else:
            self.logger.error(f"[MADna] Variant {self.variantName} is not available")
            raise Exception("Variant not available")

        self.__generateCoordinatesAndTopology()

    def _processSelection(self,**selection):

        indices = []
        for selType,selInfo in selection.items():
            #print(selType,selInfo,"type",type(selType),type(selInfo))
            if type(selInfo) != list:
                selection[selType]=[selInfo]

        idsSel      = set()
        typeSel     = set()
        strandSel   = set()
        basePairIndexSel = set()
        basePairTypeSel  = set()

        if "particleId" in selection.keys():
            for p in selection["particleId"]:
                idsSel.add(p)
        else:
            idsSel=set(range(self.nAtoms))

        if "type" in selection.keys():
            for t in selection["type"]:
                if t == "B":
                    typeSel.add("A")
                    typeSel.add("C")
                    typeSel.add("G")
                    typeSel.add("T")
                else:
                    typeSel.add(t)
        else:
            typeSel=set(["S","P","A","C","G","T"])

        if "strand" in selection.keys():
            for s in selection["strand"]:
                strandSel.add(s)
        else:
            strandSel=set([1,2])

        if "basePairIndex" in selection.keys():
            for bpi in selection["basePairIndex"]:
                if bpi > self.seqLen or bpi == 0:
                    self.logger.error(f"[MADna] Base pair has to be a number between 1 and {self.seqLen}. But is:{bpi}")
                    raise Exception("Base pair index out of range")
                if bpi < 0:
                    bpi = self.seqLen + bpi + 1
                basePairIndexSel.add(bpi)
        else:
            basePairIndexSel = set(list(range(self.seqLen)))

        if "basePairType" in selection.keys():
            for bpt in selection["basePairType"]:
                basePairTypeSel.add(bpt)
        else:
            basePairTypeSel = set(["A","C","G","T"])

        for info in self.structure.values():
            i=info["index"]
            t=info["type"]
            s=info["strand"]
            bpi=info["basePairIndex"]
            bpt=info["basePairType"]
            if (i in idsSel) and (t in typeSel) and (s in strandSel) and (bpi in basePairIndexSel) and (bpt in basePairTypeSel):
                indices.append(info["index"])

        return list(set(indices))

    def __generateCoordinatesAndTopology(self):

        self.coordinates = np.zeros((self.nAtoms,3))

        self.structure   = {}

        self.bonds       = []
        self.angles      = []
        self.dihedrals   = []

        self.exclusions  = []

        #######################################################
        ############ COORDINATES GENERATION STARTS ############

        nextCoord = np.zeros((10,3))

        loc = copy.deepcopy(self.model["POSITIONS"][self.seq[0:2]])

        r0 = np.asarray(loc["S_5_1"])
        for loc_el in loc:
            loc[loc_el] = np.asarray(loc[loc_el]) - r0

        prevCoord = self.__update(0,loc)

        for iseq in range(1,self.seqLen-1):
            loc = copy.deepcopy(self.model["POSITIONS"][self.seq[iseq:(iseq+2)]])

            for i,loc_el in enumerate(loc):
                nextCoord[i] = loc[loc_el]

            U = self.__alignBasePairs(prevCoord,nextCoord)

            loc = {'S_5_1': nextCoord[0], 'B_5_1': nextCoord[1], 'B_5_2': nextCoord[2], 'S_5_2': nextCoord[3],
                   'P_1':   nextCoord[4], 'P_2':   nextCoord[5],
                   'S_3_1': nextCoord[6], 'B_3_1': nextCoord[7], 'B_3_2': nextCoord[8], 'S_3_2': nextCoord[9]}

            prevCoord = self.__update(iseq,loc)

        for index,info in self.structure.items():
            info.update({"index":index})
            info.update({"basePairType":self.seq[self.structure[index]["basePairIndex"]-1]})

        #for index,info in self.structure.items():
        #    print(index,info)

        #Align chain along z axis

        p0 = self.coordinates[0]
        pf = self.coordinates[self.nAtoms//2-2]

        dr = pf - p0
        dr = dr/np.linalg.norm(dr)

        z  = np.array([0.0,0.0,-1.0])

        axis = np.cross(dr,z)
        axis = axis/np.linalg.norm(axis)

        angle = np.arccos(np.dot(dr,z))

        rot = Rotation.from_rotvec(angle * axis)
        self.coordinates = rot.apply(self.coordinates)

        #Make overall translation such that sugar center of second-to-last bp has x=0, y=0

        p0 = self.coordinates[self.nAtoms//2-5]
        pf = self.coordinates[self.nAtoms//2+3]

        trans = 0.5*(p0 + pf)
        for i in range(0,self.nAtoms):
            self.coordinates[i] -= trans


        ############# COORDINATES GENERATION ENDS #############
        #######################################################

        #######################################################
        ############# TOPOLOGY GENERATION STARTS ##############

        basePairsList = list(range(1,self.seqLen+1))

        basePairsPairs = []
        for i,bp in enumerate(basePairsList[:-1]):
            basePairsPairs.append([basePairsList[i],basePairsList[i+1]])

        #Same base pair
        for bp in basePairsList:
            t = self.seq[bp-1]
            ##SB
            i,j = self._processSelection(**{"basePairIndex":bp,"type":["S",t],"strand":1})
            bType = "SB/{}".format(t)
            self.bonds.append({"i":i,"j":j,"type":bType})

            i,j = self._processSelection(**{"basePairIndex":bp,"type":["S",self.model["PAIRS"][t]],"strand":2})
            bType = "SB/{}".format(self.model["PAIRS"][t])
            self.bonds.append({"i":j,"j":i,"type":bType})#Note index inverted!!

            ##BB-inter strand
            i,j = self._processSelection(**{"basePairIndex":bp,"type":[t,self.model["PAIRS"][t]]})
            bType = "BB-inter/{}{}".format(t,self.model["PAIRS"][t])
            self.bonds.append({"i":i,"j":j,"type":bType})

        for bpp in basePairsPairs:
            bp5,bp3 = bpp
            t5,t3 = self.seq[bp5-1],self.seq[bp3-1]

            i = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            if len(i)==1 and len(j)==1:
                i=i[0]
                j=j[0]

                #print(bp5,bp3,i,j,1)

                bType = "SP/{}{}".format(t5,t3)
                self.bonds.append({"i":i,"j":j,"type":bType})

            i = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":2})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            if len(i)==1 and len(j)==1:
                i=i[0]
                j=j[0]

                #print(bp5,bp3,i,j,1)

                bType = "PS/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.bonds.append({"i":j,"j":i,"type":bType}) #Note index inverted!!

            #########################################################################

            i = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})
            if len(i)==1 and len(j)==1:
                i=i[0]
                j=j[0]

                #print(bp5,bp3,t5,t3,i,j)

                bType = "PS/{}{}".format(t5,t3)
                self.bonds.append({"i":i,"j":j,"type":bType})

            i = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":2})
            if len(i)==1 and len(j)==1:
                i=i[0]
                j=j[0]

                #print(bp5,bp3,i,j,2)

                bType = "SP/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.bonds.append({"i":j,"j":i,"type":bType}) #Note index inverted!!

            ########################################################################

            #5BB3-intra strand
            i = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":1})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":1})
            if len(i)==1 and len(j)==1:
                i=i[0]
                j=j[0]

                bType = "BB-intra/{}{}".format(t5,t3)
                self.bonds.append({"i":i,"j":j,"type":bType})

            #5BB3-intra strand
            i = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":2})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":2})
            if len(i)==1 and len(j)==1:
                i=i[0]
                j=j[0]

                bType = "BB-intra/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.bonds.append({"i":j,"j":i,"type":bType}) #Note index inverted!!

        #########################################################################

        #Same base pair
        for bp in basePairsList:
            t = self.seq[bp-1]
            ##SBB
            i, = self._processSelection(**{"basePairIndex":bp,"type":"S","strand":1})
            j, = self._processSelection(**{"basePairIndex":bp,"type":"B","strand":1})
            k, = self._processSelection(**{"basePairIndex":bp,"type":"B","strand":2})

            aType = "SBB/{}{}".format(t,self.model["PAIRS"][t])
            self.angles.append({"i":i,"j":j,"k":k,"type":aType})

            i, = self._processSelection(**{"basePairIndex":bp,"type":"B","strand":1})
            j, = self._processSelection(**{"basePairIndex":bp,"type":"B","strand":2})
            k, = self._processSelection(**{"basePairIndex":bp,"type":"S","strand":2})

            aType = "SBB/{}{}".format(self.model["PAIRS"][t],t)
            self.angles.append({"i":k,"j":j,"k":i,"type":aType})#Note index inverted!!

        #########################################################################

        #Diferent base pair
        for bpp in basePairsPairs:
            bp5,bp3 = bpp
            t5,t3 = self.seq[bp5-1],self.seq[bp3-1]

            ########################################################################

            i = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                aType = "SPS/{}{}".format(t5,t3)
                self.angles.append({"i":i,"j":j,"k":k,"type":aType})

            i = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":2})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1:
                i = i[0]
                j = j[0]
                k = k[0]

                aType = "SPS/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.angles.append({"i":k,"j":j,"k":i,"type":aType})

            ########################################################################

            i = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
            k = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                aType = "3PSB5/{}{}".format(t5,t3)
                self.angles.append({"i":i,"j":j,"k":k,"type":aType})

            i = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":2})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                aType = "3PSB5/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.angles.append({"i":i,"j":j,"k":k,"type":aType})

            ########################################################################

            i = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                aType = "5PSB3/{}{}".format(t5,t3)
                self.angles.append({"i":i,"j":j,"k":k,"type":aType})

            i = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":2})
            k = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                aType = "5PSB3/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.angles.append({"i":i,"j":j,"k":k,"type":aType})

        #########################################################################

        for bpp in basePairsPairs:
            bp5,bp3 = bpp
            t5,t3 = self.seq[bp5-1],self.seq[bp3-1]

            #PSBB53
            i = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":1})
            l = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "PSBB53/{}{}".format(t5,t3)
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ##PSBB53
            i = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":2})
            k = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":2})
            l = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "PSBB53/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ########################################################################

            ###PSBB35
            i = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
            k = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":1})
            l = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "PSBB35/{}{}".format(t5,t3)
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ###PSBB35
            i = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":2})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":2})
            l = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "PSBB35/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ########################################################################

            ##SPSP
            if bp3+1 <= self.seqLen:
                i = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
                j = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
                k = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})
                l = self._processSelection(**{"basePairIndex":bp3+1,"type":"P","strand":1})

                if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                    i = i[0]
                    j = j[0]
                    k = k[0]
                    l = l[0]

                    dType = "SPSP/{}{}".format(t5,t3)
                    self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ##SPSP
            if bp5-1 >= 1:
                i = self._processSelection(**{"basePairIndex":bp3  ,"type":"S","strand":2})
                j = self._processSelection(**{"basePairIndex":bp5  ,"type":"P","strand":2})
                k = self._processSelection(**{"basePairIndex":bp5  ,"type":"S","strand":2})
                l = self._processSelection(**{"basePairIndex":bp5-1,"type":"P","strand":2})

                if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                    i = i[0]
                    j = j[0]
                    k = k[0]
                    l = l[0]

                    dType = "SPSP/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                    self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ########################################################################

            ##PSPS
            i = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":1})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            l = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "PSPS/{}{}".format(t5,t3)
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ##PSPS
            i = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":2})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":2})
            k = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            l = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "PSPS/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ########################################################################

            ##SPSB53
            i = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})
            l = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "SPSB53/{}{}".format(t5,t3)
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ##SPSB53
            i = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":2})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            k = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":2})
            l = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "SPSB53/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ########################################################################

            ##SPSB35
            i = self._processSelection(**{"basePairIndex":bp5,"type":"B","strand":1})
            j = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":1})
            k = self._processSelection(**{"basePairIndex":bp3,"type":"P","strand":1})
            l = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":1})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "SPSB35/{}{}".format(t5,t3)
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ##SPSB35
            i = self._processSelection(**{"basePairIndex":bp3,"type":"B","strand":2})
            j = self._processSelection(**{"basePairIndex":bp3,"type":"S","strand":2})
            k = self._processSelection(**{"basePairIndex":bp5,"type":"P","strand":2})
            l = self._processSelection(**{"basePairIndex":bp5,"type":"S","strand":2})

            if len(i)==1 and len(j)==1 and len(k)==1 and len(l)==1:
                i = i[0]
                j = j[0]
                k = k[0]
                l = l[0]

                dType = "SPSB35/{}{}".format(self.model["PAIRS"][t3],self.model["PAIRS"][t5])
                self.dihedrals.append({"i":i,"j":j,"k":k,"l":l,"type":dType})

            ########################################################################

        for i in range(self.nAtoms):
            self.exclusions.append([])

        neighbours = []
        for i in range(self.nAtoms):
            neighbours.append([])

        for bnd in self.bonds:
            neighbours[bnd["i"]].append(bnd["j"])
            neighbours[bnd["j"]].append(bnd["i"])

        for i in range(self.nAtoms):
            currentNeig = [i]
            for dst in range(1,4):
                nextNeig = []
                for i0 in currentNeig:
                    for j in neighbours[i0]:
                        nextNeig.append(j)
                        self.exclusions[i].append(j)
                currentNeig = nextNeig

        for i in range(self.nAtoms):
            self.exclusions[i] = list(set(self.exclusions[i]))
            self.exclusions[i].sort(key=int)
            if i in self.exclusions[i]:
                self.exclusions[i].remove(i)

        ############### TOPOLOGY GENERATION ENDS ##############
        #######################################################

        #Add particle types
        types = self.getTypes()

        for name,t in self.model["TYPES"].items():
            types.addType(name=name,**t)

        state  = {}
        state["labels"] = ["id","position"]
        state["data"]   = []
        for i,pos in enumerate(self.coordinates):
            state["data"].append([i,[pos[0],pos[1],pos[2]]])

        struct = {}
        struct["labels"] = ["id","type","resId","chainId"]
        struct["data"] = []
        for index,info in self.structure.items():

            typ = info["type"]
            res = info["basePairIndex"]
            ch  = info["strand"]

            struct["data"].append([index,typ,res,ch])

        forceField = {}

        #NL
        forceField["nl"] = {}
        forceField["nl"]["type"]       = ["VerletConditionalListSet", "nonExcluded"]
        forceField["nl"]["parameters"] = {"cutOffVerletFactor": 1.5}
        forceField["nl"]["labels"]     = ["id", "id_list"]
        forceField["nl"]["data"] = []

        for i in range(self.nAtoms):
            forceField["nl"]["data"].append([i,self.exclusions[i]])

        #WCA
        forceField["WCA"] = {}
        forceField["WCA"]["type"]       = ["NonBonded", "WCAType2"]
        forceField["WCA"]["parameters"] = {"cutOffFactor": 2.5,
                                           "condition":"nonExcluded"}

        forceField["WCA"]["labels"] = ["name_i", "name_j", "epsilon", "sigma"]
        forceField["WCA"]["data"]   = []

        for t1,info1 in self.model["TYPES"].items():
            for t2,info2 in self.model["TYPES"].items():
                forceField["WCA"]["data"].append([t1,t2,1.0,info1["radius"]+info2["radius"]])

        #DH
        forceField["DH"] = {}
        forceField["DH"]["type"]       = ["NonBonded", "DebyeHuckel"]
        forceField["DH"]["parameters"] = {"cutOffFactor": self.debyeFactor,
                                          "debyeLength":self.debyeLength,
                                          "dielectricConstant":self.dielectricConstant,
                                          "condition":"nonExcluded"}

        #BONDS
        forceField["BONDS"] = {}
        forceField["BONDS"]["type"]   = ["Bond2", "Harmonic"]
        forceField["BONDS"]["parameters"] = {}
        forceField["BONDS"]["labels"]     = ["id_i", "id_j", "K", "r0"]
        forceField["BONDS"]["data"]       = []

        for bnd in self.bonds:
            forceField["BONDS"]["data"].append([bnd["i"],bnd["j"],
                                                self.model["BONDS"][bnd["type"]]["K"],
                                                self.model["BONDS"][bnd["type"]]["r0"]])

        #ANGLES
        forceField["ANGLES"] = {}
        forceField["ANGLES"]["type"]   = ["Bond3", "HarmonicAngular"]
        forceField["ANGLES"]["parameters"] = {}
        forceField["ANGLES"]["labels"]     = ["id_i", "id_j", "id_k", "K", "theta0"]
        forceField["ANGLES"]["data"]       = []

        for ang in self.angles:
            forceField["ANGLES"]["data"].append([ang["i"],ang["j"],ang["k"],
                                                self.model["ANGLES"][ang["type"]]["K"],
                                                self.model["ANGLES"][ang["type"]]["theta0"]])

        #DIHEDRALS
        forceField["DIHEDRALS"] = {}
        forceField["DIHEDRALS"]["type"]   = ["Bond4", "Dihedral"]
        forceField["DIHEDRALS"]["parameters"] = {}
        forceField["DIHEDRALS"]["labels"]     = ["id_i", "id_j", "id_k", "id_l", "n", "K", "phi0"]
        forceField["DIHEDRALS"]["data"]       = []

        for dih in self.dihedrals:
            forceField["DIHEDRALS"]["data"].append([dih["i"],dih["j"],dih["k"],dih["l"],
                                                    1,
                                                    self.model["DIHEDRALS"][dih["type"]]["K"],
                                                    self.model["DIHEDRALS"][dih["type"]]["phi0"]])

        #######################################################
        ####################### VARIANT #######################

        if self.variantName == "fast":

            del forceField["WCA"]
            del forceField["DH"]

            PHOSPHATE_DISTANCE = 3.4

            cutOff      = self.debyeFactor*self.debyeLength
            madnafast_n = math.ceil(self.fastFactor*(cutOff/PHOSPHATE_DISTANCE))

            phosphateIndex_basePair = []
            for bp in range(self.seqLen):
                index = self._processSelection(**{"basePairIndex":bp+1,"type":"P"})
                phosphateIndex_basePair+=[[i,bp+1] for i in index]

            forceField["BONDS_DH"] = {}
            forceField["BONDS_DH"]["type"]       = ["Bond2", "DebyeHuckel"]
            forceField["BONDS_DH"]["parameters"] = {}
            forceField["BONDS_DH"]["labels"]     = ["id_i", "id_j", "chgProduct", "dielectricConstant", "debyeLength", "cutOff"]
            forceField["BONDS_DH"]["data"]       = []

            chgProduct = self.model["TYPES"]["P"]["charge"]
            chgProduct = chgProduct*chgProduct
            for ph1,ph2 in itertools.combinations(phosphateIndex_basePair,2):
                if(abs(ph1[1]-ph2[1])<madnafast_n):
                    forceField["BONDS_DH"]["data"].append([ph1[0],ph2[0],chgProduct,self.dielectricConstant,self.debyeLength,cutOff])

        ##################### VARIANT END #####################
        #######################################################

        self.setState(state)
        self.setStructure(struct)
        self.setForceField(forceField)

    def processSelection(self,selectionType,selectionOptions):
        #Options is always a string

        if selectionType == "type":
            #Options has to be a list of strings
            #Example: ["S","P"]
            options = [str(x) for x in selectionOptions.split()]
            for opt in options:
                if opt not in ["S","P","B"]:
                    self.logger.error(f"[MADna] Type has to be one of the following: S, P, B. But is:{opt}")
                    raise Exception("Type not recognized")
            return self._processSelection(**{"type":options})

        if selectionType == "strand":
            #Options has to be a list of integers
            #Example: [1,2]
            options = [int(x) for x in selectionOptions.split()]
            for opt in options:
                if opt not in [1,2]:
                    self.logger.error(f"[MADna] Strand has to be 1 or 2. But is:{opt}")
                    raise Exception("Strand not recognized")
            return self._processSelection(**{"strand":options})

        if selectionType == "basePairIndex":
            #Options to be a list of integers
            options = [int(x) for x in selectionOptions.split()]
            return self._processSelection(**{"basePairIndex":options})

        if selectionType == "particleId":
            #Options to be a list of integers
            options = [int(x) for x in selectionOptions.split()]
            return self._processSelection(**{"particleId":options})

        return None


