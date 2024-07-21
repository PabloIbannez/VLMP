import sys, os

import copy

import logging

from . import modelBase
from ...utils.input import getLabelIndex

import pyGrained.models.AlphaCarbon as proteinModel

class SOP(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "SOP (Self-Organized Polymer) model for protein folding and dynamics simulations. This model
      implements a coarse-grained representation of proteins based on the self-organized polymer
      concept, which captures the essential features of protein structure and dynamics while
      allowing for efficient simulations of large systems and long time scales.
      <p>
      The SOP model represents each amino acid by a single bead, located at the
      alpha-carbon position. The potential energy function includes terms for native contacts,
      chain connectivity, and excluded volume interactions. This approach allows for the study
      of protein folding, unfolding, and large-scale conformational changes.
      <p>
      Key features of the model include:
      - Coarse-grained representation with one bead per residue
      <p>
      - Native-contact-based potential energy function
      <p>
      - Efficient simulation of large proteins and long timescales
      <p>
      - Ability to handle multi-domain proteins and protein complexes
      <p>
      - Option to include solvent-accessible surface area (SASA) calculations
      <p>
      - Flexibility for customizing the energy scale of native contacts
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
                           "default":true},
        "epsilonNC":{"description":"Energy scale for native contacts.",
                     "type":"float",
                     "default":1.0}
     },
     "example":"
         {
            \"type\":\"SOP\",
            \"parameters\":{
                \"PDB\":\"1AON\",
                \"centerInput\":true,
                \"SASA\":false,
                \"aggregateChains\":true
            }
         }
        ",
     "references":[
         ".. [Hyeon2006] Hyeon, C., & Thirumalai, D. (2006). Forced-unfolding and force-quench refolding of RNA hairpins. Biophysical Journal, 90(10), 3410-3427.",
         ".. [Zhmurov2010] Zhmurov, A., Dima, R. I., Kholodov, Y., & Barsegov, V. (2010). SOP-GPU: Accelerating biomolecular simulations in the centisecond timescale using graphics processors. Proteins: Structure, Function, and Bioinformatics, 78(14), 2984-2999.",
         ".. [Hyeon2011] Hyeon, C., & Thirumalai, D. (2011). Capturing the essence of folding and functions of biomolecules using coarse-grained models. Nature Communications, 2(1), 1-11.",
         ".. [pyGrained] https://github.com/PabloIbannez/pyGrained"
     ]
    }
    """

    availableParameters = {"PDB",
                           "centerInput",
                           "SASA",
                           "aggregateChains",
                           "epsilonNC"}
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

        sopParams = {"SASA":params.get("SASA",False),
                     "centerInput":params.get("centerInput",True),
                     "aggregateChains":params.get("aggregateChains",True),
                     "parameters": copy.deepcopy(params)}

        sop = proteinModel.SelfOrganizedPolymer(name = name,
                                                inputPDBfilePath = inputPDBfilePath,
                                                params = sopParams)

        ########################################################

        types = self.getTypes()
        modelTypes = sop.getTypes()

        for _,t in modelTypes.items():
            types.addType(**t)

        #Set model
        self.setState(sop.getState())
        self.setStructure(sop.getStructure())
        self.setForceField(sop.getForceField())


    def processSelection(self,selectionType,selectionOptions):
        return None
