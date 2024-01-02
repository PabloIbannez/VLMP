import sys, os

import copy

import logging

from . import modelBase
from ...utils.input import getLabelIndex

import pyGrained.models.AlphaCarbon as proteinModel

class ENM(modelBase):
    """
    Component name: ENM
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 24/03/2023

    Elastic Network Model (ENM) model for proteins.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"PDB",
                                                "centerInput",
                                                "SASA",
                                                "aggregateChains",
                                                "K",
                                                "enmCut"},
                         requiredParameters  = {"PDB"},
                         definedSelections   = {"particleId","forceField"},
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

        enmParams = {"SASA":params.get("SASA",False),
                     "centerInput":params.get("centerInput",True),
                     "aggregateChains":params.get("aggregateChains",True),
                     "parameters": copy.deepcopy(params)}

        enm = proteinModel.ElasticNetworkModel(name = name,
                                               inputPDBfilePath = inputPDBfilePath,
                                               params = enmParams)

        ########################################################

        types = self.getTypes()
        modelTypes = enm.getTypes()

        for _,t in modelTypes.items():
            types.addType(**t)

        #Set model
        self.setState(enm.getState())
        self.setStructure(enm.getStructure())
        self.setForceField(enm.getForceField())


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        if "forceField" in params:
            sel += self.getForceFieldSelection(params["forceField"])

        return sel
