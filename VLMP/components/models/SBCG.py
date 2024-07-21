import sys, os

import copy

import logging

from ... import DEBUG_MODE
from . import modelBase

import pyGrained.models.SBCG as proteinModel

class SBCG(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "SBCG (Shape-Based Coarse-Grained) model for protein simulations. This model implements a
      coarse-grained representation of proteins that maintains the overall shape and essential
      features while reducing computational complexity.
      <p>
      The SBCG approach represents proteins using a reduced number of beads, typically one bead
      for hundreds of atoms, capturing the protein.
      This reduction in degrees of freedom allows for simulations of larger systems and longer
      timescales compared to all-atom models.
      <p>
      Key features of the SBCG model include:
      <p>
      - Shape-preserving coarse-graining based on the input protein structure
      <p>
      - Flexible parameterization of the coarse-graining process
      <p>
      - Automatic generation of bonded and non-bonded interactions
      <p>
      - Support for multi-chain proteins and protein complexes
      <p>
      The model takes a PDB file as input and generates the coarse-grained representation based
      on the specified parameters. It can handle various levels of coarse-graining and allows
      for customization of the interaction potentials.
      <p>
      This model uses the [pyGrained]_ library to create the SBCG representation.
      ",
     "parameters":{
        "PDB":{"description":"Path to the input PDB file or a valid PDB ID for download.",
               "type":"str"},
        "resolution":{"description":"Resolution of the coarse-graining, number of atoms per bead.",
                      "type":"float"},
        "steps":{"description":"Number of steps in the coarse-graining refinement process.",
                 "type":"int"},
        "bondsModel":{"description":"Model used for bonded interactions.(ENM or count)",
                      "type":"str"},
        "nativeContactsModel":{"description":"Model used for native contact interactions (CA).",
                               "type":"str"},
        "centerInput":{"description":"If true, centers the input structure.",
                       "type":"bool",
                       "default":true},
        "SASA":{"description":"If true, calculates the Solvent Accessible Surface Area.",
                "type":"bool",
                "default":false},
        "aggregateChains":{"description":"If true, treats multiple chains as a single entity.",
                           "type":"bool",
                           "default":true}
     },
     "example":"
         {
            \"type\":\"SBCG\",
            \"parameters\":{
                \"PDB\":\"1ABC\",
                \"resolution\":200,
                \"steps\":1000,
                \"bondsModel\":\"ENM\",
                \"nativeContactsModel\":\"CA\",
                \"SASA\":true
            }
         }
        ",
     "references":[
         ".. [Arkhipov2006] Arkhipov, A., Freddolino, P. L., & Schulten, K. (2006). Stability and dynamics of virus capsids described by coarse-grained modeling. Structure, 14(12), 1767-1777.",
         ".. [pyGrained] https://github.com/PabloIbannez/pyGrained"
     ]
    }
    """

    availableParameters = {"PDB",
                           "resolution","steps",
                           "bondsModel","nativeContactsModel",
                           "centerInput",
                           "SASA",
                           "aggregateChains"}
    requiredParameters  = {"PDB","resolution","steps","bondsModel","nativeContactsModel"}
    definedSelections   = set()

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


    def processSelection(self,selectionType,selectionOptions):
        return None
