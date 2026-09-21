import sys, os

import copy

import logging

from ... import DEBUG_MODE
from . import modelBase

import pyGrained.models.AdaptiveCG as proteinModel

class AdaptiveCG(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "AdaptiveCG (Adaptive Coarse-Grained) model for protein simulations. The bead mapping
      follows the CG mapping of [Monago2025]_, which places the beads by minimizing the
      total moment of inertia of the atoms about the bead they are assigned to.
      <p>
      In the sharp limit the mapping indicator of Eq. 1 becomes the characteristic function
      of the Voronoi cell of a bead, the assignment reduces to nearest bead, and the
      optimization becomes Lloyd's algorithm. It is therefore implemented as a mass-weighted
      k-means, which is exact rather than approximate: the converged bead is the mass
      centroid of its own Voronoi cell.
      <p>
      Key features of the AdaptiveCG model include:
      <p>
      - Bead placement by mass-weighted k-means, one bead per `resolution` atoms
      <p>
      - Coarse-graining done once per chain class and spread to the whole assembly
      <p>
      - Bonds: an elastic network within each chain
      <p>
      - Native contacts: Morse interactions between beads of different chains
      <p>
      Bonds are always intra-chain and native contacts always inter-chain. This is not
      configurable: the two are complementary by construction, which is what makes the
      chain interfaces the only part of the force field that carries the assembly energy.
      <p>
      This model uses the [pyGrained]_ library to create the AdaptiveCG representation.
      ",
     "parameters":{
        "PDB":{"description":"Path to the input PDB file.",
               "type":"str"},
        "resolution":{"description":"Resolution of the coarse-graining, number of atoms per bead. The bead count of a chain is int(N/resolution)+1.",
                      "type":"float"},
        "bondsModel":{"description":"Model used for bonded interactions. Only ENM is available, with parameters enmCut and K.",
                      "type":"dict"},
        "nativeContactsModel":{"description":"Model used for native contact interactions. Only cutOff is available, with parameters ncCut, epsilon, D and eps0.",
                               "type":"dict"},
        "minBeads":{"description":"Minimum number of beads per chain.",
                    "type":"int",
                    "default":1},
        "seed":{"description":"Seed of the k-means initialization. The mapping is reproducible for a fixed seed.",
                "type":"int",
                "default":0},
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
            \"type\":\"AdaptiveCG\",
            \"parameters\":{
                \"PDB\":\"capsid.pdb\",
                \"resolution\":250,
                \"bondsModel\":{\"name\":\"ENM\",
                                \"parameters\":{\"enmCut\":20.0,\"K\":1.0}},
                \"nativeContactsModel\":{\"name\":\"cutOff\",
                                         \"parameters\":{\"ncCut\":20.0,\"epsilon\":1.0,
                                                         \"D\":1.0,\"eps0\":1.0}}
            }
         }
        ",
     "references":[
         ".. [Monago2025] Monago, C., de la Torre, J. A., Delgado-Buscalioni, R., & Espanol, P. (2025). Unraveling internal friction in a coarse-grained protein model. The Journal of Chemical Physics, 162(11), 114115.",
         ".. [pyGrained] https://github.com/PabloIbannez/pyGrained"
     ]
    }
    """

    availableParameters = {"PDB",
                           "resolution",
                           "minBeads","seed",
                           "bondsModel","nativeContactsModel",
                           "centerInput",
                           "SASA",
                           "aggregateChains",
                           "additionalExclusions"}
    requiredParameters  = {"PDB","resolution","bondsModel","nativeContactsModel"}
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

        #Unlike SBCG, no PDB ID download is accepted. The model is meant for
        #assemblies large enough that the structure is prepared beforehand.

        if params["PDB"].split(".")[-1] not in ["pdb","pqr"]:
            raise Exception("PDB parameter must be a path to a .pdb or .pqr file.")

        inputPDBfilePath = params["PDB"]

        adaptiveParams = {"SASA":params.get("SASA",False),
                          "centerInput":params.get("centerInput",True),
                          "aggregateChains":params.get("aggregateChains",True),
                          "parameters": copy.deepcopy(params),
                          "additionalExclusions": params.get("additionalExclusions",False)}

        adaptive = proteinModel.AdaptiveCG(name = name,
                                           inputPDBfilePath = inputPDBfilePath,
                                           params = adaptiveParams,
                                           debug = DEBUG_MODE)

        ########################################################

        types = self.getTypes()
        modelTypes = adaptive.getTypes()

        for _,t in modelTypes.items():
            types.addType(**t)

        self.setState(adaptive.getState())
        self.setStructure(adaptive.getStructure())
        self.setForceField(adaptive.getForceField())


    def processSelection(self,selectionType,selectionOptions):
        return None
