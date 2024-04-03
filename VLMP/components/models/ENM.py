import sys, os

import requests

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

    def __isValidPDB(self, id_pdb):
        """Checks if the PDB ID is valid."""
        return len(id_pdb) == 4 and id_pdb.isalnum()

    def __downloadPDB(self, id_pdb, file_path):
        url = f"https://files.rcsb.org/download/{id_pdb}.pdb"
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"PDB {id_pdb} downloaded successfully.")
        else:
            self.logger.error(f"Error downloading the PDB {id_pdb}. Please verify the PDB ID.")
            raise RuntimeError("Error downloading the PDB,")


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

        downloadedPDB = False
        if params["PDB"].split(".")[-1] in ["pdb","pqr"]:
            inputPDBfilePath = params["PDB"]
        else:
            pdb_id = params["PDB"]
            if self.__isValidPDB(pdb_id):
                downloadedPDB = True
                inputPDBfilePath = f"tmp_{pdb_id}.pdb"
                self.__downloadPDB(params["PDB"], inputPDBfilePath)
            else:
                self.logger.error("The PDB ID is not valid")
                raise RuntimeError("Invalid PDB ID")


        enmParams = {"SASA":params.get("SASA",False),
                     "centerInput":params.get("centerInput",True),
                     "aggregateChains":params.get("aggregateChains",True),
                     "parameters": copy.deepcopy(params)}

        enm = proteinModel.ElasticNetworkModel(name = name,
                                               inputPDBfilePath = inputPDBfilePath,
                                               params = enmParams)
        if downloadedPDB:
            os.remove(inputPDBfilePath)
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

