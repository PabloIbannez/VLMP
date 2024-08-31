import sys, os

import logging

from . import modelBase

import numpy as np

class WLC(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "WLC (Worm-Like Chain, [WLC]_) model for simulating polymer chains, particularly suitable for
      modeling DNA or other semi-flexible biopolymers. This model implements a discretized
      version of the continuous worm-like chain, representing the polymer as a series of
      connected beads with bending rigidity.
      <p>
      The WLC model captures the essential physics of semi-flexible polymers, including
      their entropic elasticity and persistence length.
      <p>
      Key features of the model include:
      <p>
      - Customizable number of beads to represent the polymer chain
      <p>
      - Adjustable bond length and bending rigidity
      <p>
      - Option to add excluded volume interactions (not included by default)
      <p>",
     "parameters":{
        "N":{"description":"Number of particles (beads) in the chain.",
             "type":"int"},
        "mass":{"description":"Mass of each particle.",
                "type":"float",
                "default":1.0},
        "b":{"description":"Equilibrium distance between consecutive particles.",
             "type":"float",
             "default":1.0},
        "Kb":{"description":"Spring constant for bonds.",
              "type":"float",
              "default":1.0},
        "Ka":{"description":"Spring constant for angles (bending rigidity).",
              "type":"float",
              "default":1.0},
        "typeName":{"description":"Name identifier for the particle type.",
                    "type":"str",
                    "default":"A"}
     },
     "example":"
         {
            \"type\":\"WLC\",
            \"parameters\":{
                \"N\":100,
                \"b\":0.34,
                \"Kb\":100.0,
                \"Ka\":2.0,
                \"typeName\":\"DNA\"
            }
         }
        ",
     "references":[
         ".. [WLC] https://en.wikipedia.org/wiki/Worm-like_chain",
     ]
    }
    """

    availableParameters = {"N","mass","b","Kb","Ka","typeName"}
    requiredParameters  = {"N"}
    definedSelections   = {"polymerIndex"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        ############################################################
        ####################  Model Parameters  ####################
        ############################################################

        #Read the number of particles
        self.N = params["N"]

        #Read the particle mass and the distance between two consecutive particles
        mass = params.get("mass",1.0)
        b    = params.get("b",1.0)

        #Read values for the spring constant for bonds and angles
        Kb = params.get("Kb",1.0)
        Ka = params.get("Ka",1.0)

        typeName = params.get("typeName","A")

        self.logger.debug(f"[WLC] Generating a WLC model with {self.N} particles")
        self.logger.debug(f"[WLC] Parameters: mass={mass}, b={b}, Kb={Kb}, Ka={Ka}")

        ########################################################
        ############### Generate the WLC model #################
        ########################################################

        #Add particle types
        types = self.getTypes()
        radius = 0.5*b
        types.addType(name=typeName,mass=mass,radius=radius)

        #Generate positions, a line along the z axis
        state = {}
        state["labels"] = ["id","position"]
        state["data"]   = []
        for i in range(self.N):
            state["data"].append([i, [0.0,0.0,i*b-0.5*(self.N-1)*b]])

        #Generate structure
        structure = {}
        structure["labels"] = ["id","type"]
        structure["data"]   = []
        for i in range(self.N):
            structure["data"].append([i,typeName])

        #Generate forceField
        forceField = {}

        forceField["bonds_wlc"] = {}
        forceField["bonds_wlc"]["type"]       = ["Bond2","Harmonic"]
        forceField["bonds_wlc"]["parameters"] = {}
        forceField["bonds_wlc"]["labels"]     = ["id_i","id_j","K","r0"]
        forceField["bonds_wlc"]["data"]       = []

        for i in range(self.N-1):
            forceField["bonds_wlc"]["data"].append([i,i+1,Kb,b])

        forceField["angles_wlc"] = {}
        forceField["angles_wlc"]["type"]       = ["Bond3","KratkyPorod"]
        forceField["angles_wlc"]["parameters"] = {}
        forceField["angles_wlc"]["labels"]     = ["id_i","id_j","id_k","K"]
        forceField["angles_wlc"]["data"]       = []

        for i in range(self.N-2):
            forceField["angles_wlc"]["data"].append([i,i+1,i+2,Ka])

        ########################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,selectionType,selectionOptions):

        if selectionType == "polymerIndex":
            sel = []
            # Convert selectionOptions to a list of ints
            indices = selectionOptions.split()
            indices = [int(i) for i in indices]
            for pIndex in indices:
                if pIndex < -self.N or pIndex > self.N or pIndex == 0:
                    self.logger.error(f"[WLC] Invalid polymer index {pIndex}")
                    raise Exception("Invalid polymer index")
                if pIndex > 0:
                    sel.append(pIndex-1)
                if pIndex < 0:
                    sel.append(self.N+pIndex)

            return sel

        return None
