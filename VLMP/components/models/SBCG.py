import sys, os

import copy

import logging

from ... import DEBUG_MODE
from . import modelBase

import pyGrained.models.SBCG as proteinModel

class SBCG(modelBase):
    """
    Component name: SBCG
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 23/03/2023

    Shape Based Coarse Grained.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"PDB",
                                                "resolution","steps",
                                                "bondsModel","nativeContactsModel",
                                                "centerInput",
                                                "SASA",
                                                "aggregateChains"},
                         requiredParameters  = {"PDB","resolution","steps","bondsModel","nativeContactsModel"},
                         definedSelections   = {"particleId"},
                         **params)

        ############################################################
        ######################  Set up model  ######################
        ############################################################

        #Check if PDB is a file or a PDB ID.
        #PDB is considered a file if it has a .pdb or .pqr extension.
        #If it is a file, it is loaded as a PDB file.
        #If it is a PDB ID, PDB file is downloaded from the RCSB PDB database.

        if params["PDB"].split(".")[-1] in ["pdb","pqr"]:
            inputPDBfilePath = params["PDB"]
        else:
            raise NotImplementedError("PDB ID download not implemented yet.")

        sbcgParams = {"SASA":params.get("SASA",True),
                      "centerInput":params.get("centerInput",True),
                      "aggregateChains":params.get("aggregateChains",True),
                      "parameters": copy.deepcopy(params)}

        sbcg = proteinModel.SBCG(name = name,
                                 inputPDBfilePath = inputPDBfilePath,
                                 params = sbcgParams,
                                 debug = DEBUG_MODE)

        ########################################################

        types = self.getTypes()
        modelTypes = sbcg.getTypes()

        for _,t in modelTypes.items():
            types.addType(**t)

        self.setState(sbcg.getState())
        self.setStructure(sbcg.getStructure())
        self.setForceField(sbcg.getForceField())


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel
