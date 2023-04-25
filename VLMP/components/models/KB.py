import sys, os

import copy

import logging

from . import modelBase

import pyGrained.models.AlphaCarbon as proteinModel

class KB(modelBase):
    """
    Component name: KB
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 25/03/2023

    Karanicolas Brooks.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"PDB",
                                                "centerInput",
                                                "SASA",
                                                "aggregateChains"},
                         requiredParameters  = {"PDB"},
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

        kbParams = {"SASA":params.get("SASA",False),
                    "centerInput":params.get("centerInput",True),
                    "aggregateChains":params.get("aggregateChains",True),
                    "parameters": copy.deepcopy(params)}

        kb = proteinModel.KaranicolasBrooks(name = name,
                                            inputPDBfilePath = inputPDBfilePath,
                                            params = kbParams)

        ########################################################

        types = self.getTypes()
        modelTypes = kb.getTypes()

        for _,t in modelTypes.items():
            types.addType(**t)

        self.setState(kb.getState())
        self.setStructure(kb.getStructure())
        self.setForceField(kb.getForceField())


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel
