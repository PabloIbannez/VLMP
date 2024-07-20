import sys, os

import requests

import copy

import logging

from . import modelBase
from ...utils.input import getLabelIndex

import pyGrained.models.AlphaCarbon as proteinModel

class ENM(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Elastic Network Model (ENM) for protein simulations. This model implements a coarse-grained
      representation of proteins, typically using one bead per residue (usually the alpha-carbon).
      ENM is based on the assumption that protein dynamics can be described by harmonic potentials
      between nearby residues.
      <p>
      The model constructs a network of springs between residues within a certain cutoff distance.
      This approach allows for efficient simulation of large-scale protein motions and normal modes,
      making it particularly useful for studying protein flexibility and conformational changes.
      <p>
      The model can be customized through various parameters, including the spring constant (K) and
      the cutoff distance for interactions (enmCut). These parameters control the strength of the
      harmonic interactions and the connectivity of the network, respectively.
      <p>
      The protein structure is input via a PDB file, which can be either a local file or downloaded
      from the RCSB PDB database if a valid PDB ID is provided.
      <p>
      This implementation also includes options for centering the input structure and handling
      multiple chains, making it versatile for various protein simulation scenarios.
      <p>
      This model uses the [pyGrained]_ library to create the ENM representation.
      ",
     "parameters":{
        "PDB":{"description":"Path to a local PDB file or a valid PDB ID for download.",
               "type":"str"},
        "centerInput":{"description":"If True, centers the input structure.",
                       "type":"bool",
                       "default":true},
        "SASA":{"description":"If True, calculates the Solvent Accessible Surface Area.",
                "type":"bool",
                "default":false},
        "aggregateChains":{"description":"If True, treats multiple chains as a single entity.",
                           "type":"bool",
                           "default":true},
        "K":{"description":"Spring constant for the harmonic interactions.",
             "type":"float",
             "default":null},
        "enmCut":{"description":"Cutoff distance for including spring connections between residues.",
                  "type":"float",
                  "default":null}
     },
     "example":"
         {
            \"type\":\"ENM\",
            \"parameters\":{
                \"PDB\":\"1ABC\",
                \"centerInput\":true,
                \"K\":1.0,
                \"enmCut\":10.0
            }
         }
        ",
     "references":[
         ".. [Tirion1996] Tirion, M. M. (1996). Large Amplitude Elastic Motions in Proteins from a Single-Parameter, Atomic Analysis. Physical Review Letters, 77(9), 1905–1908.",
         ".. [Atilgan2001] Atilgan, A. R., Durell, S. R., Jernigan, R. L., Demirel, M. C., Keskin, O., & Bahar, I. (2001). Anisotropy of Fluctuation Dynamics of Proteins with an Elastic Network Model. Biophysical Journal, 80(1), 505–515.",
         ".. [pyGrained] https://github.com/PabloIbannez/pyGrained"
     ]
    }
    """

    availableParameters = {"PDB","centerInput","SASA","aggregateChains","K","enmCut"}
    requiredParameters  = {"PDB"}
    definedSelections   = {"particleId","forceField"}

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
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
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


    def processSelection(self,selectionType,selectionOptions):
        return None

