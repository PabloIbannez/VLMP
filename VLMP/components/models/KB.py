import sys, os

import copy

import logging

from . import modelBase

import pyGrained.models.AlphaCarbon as proteinModel

class KB(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "KB (Karanicolas Brooks) model for protein folding simulations. This model implements a
      structure-based coarse-grained representation of proteins, based on the work of Karanicolas
      and Brooks. It is particularly effective for studying protein folding mechanisms and
      dynamics.
      <p>
      The KB model represents each amino acid by a single bead located at the alpha-carbon
      position. The potential energy function is derived from the native structure of the
      protein and includes terms for bonds, angles, dihedrals, and non-bonded interactions.
      This approach allows for efficient simulations while maintaining the essential features
      of protein folding landscapes.
      <p>
      Key features of the model include:
      <p>
      - Coarse-grained representation with one bead per residue
      <p>
      - Native-structure-based potential energy function
      <p>
      - Efficient simulation of large proteins and long timescales
      <p>
      - Option to include solvent-accessible surface area (SASA) calculations
      <p>
      - Ability to handle multi-chain proteins and protein complexes
      <p>
      The model reads protein structures from PDB files and can handle both local files and
      PDB IDs for direct download from the RCSB PDB database.
      <p>
      This model uses the [pyGrained]_ library to create the coarse-grained representation of the
      protein.
      ",
     "parameters":{
        "PDB":{"description":"Path to a local PDB file or a valid PDB ID for download.",
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
            \"type\":\"KB\",
            \"parameters\":{
                \"PDB\":\"1UBQ\",
                \"centerInput\":true,
                \"SASA\":true,
                \"aggregateChains\":false
            }
         }
        ",
     "references":[
         ".. [Karanicolas2002] Karanicolas, J., & Brooks, C. L. (2002). The origins of asymmetry in the folding transition states of protein L and protein G. Protein Science, 11(10), 2351-2361.",
         ".. [Karanicolas2003] Karanicolas, J., & Brooks, C. L. (2003). Improved Gō-like models demonstrate the robustness of protein folding mechanisms towards non-native interactions. Journal of Molecular Biology, 334(2), 309-325.",
         ".. [Karanicolas2003b] Karanicolas, J., & Brooks, C. L. (2003). The structural basis for biphasic kinetics in the folding of the WW domain from a formin-binding protein: Lessons for protein design? Proceedings of the National Academy of Sciences, 100(7), 3954-3959.",
         ".. [pyGrained] https://github.com/PabloIbannez/pyGrained"
     ]
    }
    """

    availableParameters = {"PDB",
                           "centerInput",
                           "SASA",
                           "aggregateChains"}
    requiredParameters  = {"PDB"}
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


    def processSelection(self,selectionType,selectionOptions):
        return None
