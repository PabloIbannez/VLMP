import sys, os

import logging

import numpy as np

from VLMP.components.models import modelBase

class STERIC_LAMBDA_SOLVATION(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "STERIC_LAMBDA_SOLVATION model for simulating solvation effects with steric interactions
      and lambda coupling. This model implements a coarse-grained representation of solvent
      particles interacting with solute molecules, incorporating both steric repulsion and
      a lambda parameter for coupling strength.
      <p>
      The model uses a soft-core potential to represent steric interactions, which allows
      for smooth transitions in free energy calculations. The lambda parameter can be used
      to gradually turn on or off the interactions, making this model particularly useful
      for free energy perturbation and thermodynamic integration studies.
      <p>
      Key features of the model include:
      <p>
      - Customizable concentration of solvent particles
      <p>
      - Adjustable steric interaction parameters (epsilon, cutoff)
      <p>
      - Lambda coupling for smooth free energy calculations
      <p>
      - Option to add a Verlet list for efficient neighbor searching
      <p>
      - Flexible boundary conditions with customizable box padding
      <p>
      The lambda coupling can be also used to create the inital conditions,
      starting from lambda=0 and gradually increasing the value to 1.
     ",
     "parameters":{
        "concentration":{"description":"Concentration of the solute in the solvent (in N/V units).",
                         "type":"float"},
        "condition":{"description":"Condition for the interaction. Options: 'inter', 'intra', etc.",
                     "type":"str",
                     "default":"inter"},
        "epsilon":{"description":"Epsilon parameter of the steric potential.",
                   "type":"float",
                   "default":1.0},
        "cutOffFactor":{"description":"Factor to multiply the sigma parameter to obtain the cut-off distance.",
                        "type":"float",
                        "default":1.5},
        "alpha":{"description":"Alpha parameter of the steric potential for soft-core behavior.",
                 "type":"float",
                 "default":0.5},
        "addVerletList":{"description":"If True, a Verlet list will be created for the interactions.",
                         "type":"bool",
                         "default":true},
        "particleName":{"description":"Name of the particle to be added to the system.",
                        "type":"str",
                        "default":"W"},
        "particleMass":{"description":"Mass of the particle to be added to the system.",
                        "type":"float",
                        "default":1.0},
        "particleRadius":{"description":"Radius of the particle to be added to the system.",
                          "type":"float",
                          "default":1.0},
        "particleCharge":{"description":"Charge of the particle to be added to the system.",
                          "type":"float",
                          "default":0.0},
        "padding":{"description":"Padding to be added to the box to place the particle.",
                   "type":"list of two lists of three floats",
                   "default":[[0.0,0.0,0.0],[0.0,0.0,0.0]]}
     },
     "example":"
         {
            \"type\":\"STERIC_LAMBDA_SOLVATION\",
            \"parameters\":{
                \"concentration\":0.1,
                \"epsilon\":1.0,
                \"cutOffFactor\":2.0,
                \"alpha\":0.5,
                \"particleRadius\":0.5,
                \"padding\":[[1.0,1.0,1.0],[1.0,1.0,1.0]]
            }
         }
        ",
     "note": "The model requires a ensemble with a lambda parameter. Otherwise, the simulation will fail."
    }
    """

    availableParameters = {"concentration",
                           "epsilon","cutOffFactor",
                           "alpha",
                           "addVerletList","condition",
                           "particleName",
                           "particleMass","particleRadius","particleCharge",
                           "padding"}
    requiredParameters  = {"concentration"}
    definedSelections   = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        concentration = params["concentration"]

        cutOffFactor  = params.get("cutOffFactor",1.5)
        epsilon       = params.get("epsilon",1.0)
        alpha         = params.get("alpha",0.5)

        addVerletList = params.get("addVerletList",True)
        condition     = params.get("condition","inter")

        particleName  = params.get("particleName","W")

        particleMass   = params.get("particleMass",1.0)
        particleRadius = params.get("particleRadius",1.0)
        particleCharge = params.get("particleCharge",0.0)

        padding = params.get("padding",[[0.0,0.0,0.0],[0.0,0.0,0.0]])

        if(not self.getEnsemble().isEnsembleComponent("box")):
            self.logger.error("[STERIC_LAMBDA_SOLVATION] The ensemble does not have a box component.")
            return
        if(not self.getEnsemble().isEnsembleComponent("lambda")):
            self.logger.error("[STERIC_LAMBDA_SOLVATION] The ensemble does not have a lambda component.")
            return

        ############################################################
        # Adding particles

        box = self.getEnsemble().getEnsembleComponent("box")

        # Applying padding
        xMax = +box[0]/2.0 + padding[0][0]
        xMin = -box[0]/2.0 - padding[1][0]

        yMax = +box[1]/2.0 + padding[0][1]
        yMin = -box[1]/2.0 - padding[1][1]

        zMax = +box[2]/2.0 + padding[0][2]
        zMin = -box[2]/2.0 - padding[1][2]

        V   = (xMax-xMin)*(yMax-yMin)*(zMax-zMin)
        N   = int(concentration*V)

        self.logger.info(f"Adding {N} particles of type {particleName} to the system.")
        # Note that the number of paricles is computed after the padding is applied

        # Add type
        types = self.getTypes()
        types.addType(name = particleName,
                      mass = particleMass,
                      radius = particleRadius,
                      charge = particleCharge)

        state = {}
        state["labels"] = ["id","position"]
        state["data"]   = []
        for i in range(N):
            self.logger.debug(f"Adding particle {i+1}/{N} ...")
            x = np.random.uniform(xMin,xMax)
            y = np.random.uniform(yMin,yMax)
            z = np.random.uniform(zMin,zMax)
            state["data"].append([i,[x,y,z]])

        structure = {}
        structure["labels"] = ["id","type"]
        structure["data"]   = []
        for i in range(N):
            structure["data"].append([i,particleName])

        ############################################################

        forceField = {}

        forcefield = {}

        if addVerletList:
            forcefield["nl"]={}
            forcefield["nl"]["type"]       =  ["VerletConditionalListSet",  "nonExclIntra_nonExclInter"]
            forcefield["nl"]["parameters"] =  {}
            forcefield["nl"]["labels"]      = ["id","id_list"]
            forcefield["nl"]["data"]        = []

        forcefield[name] = {}
        forcefield[name]["type"] = ["NonBonded","Steric12SoftCore"]
        forcefield[name]["parameters"] = {"cutOffFactor":cutOffFactor,
                                          "condition":condition,
                                          "alpha":alpha}
        forcefield[name]["labels"] = ["name_i","name_j","epsilon","sigma"]
        forcefield[name]["data"]   = []

        types = self.getTypes().getTypes()
        for t1 in types:
            for t2 in types:
                r1 = types[t1]["radius"]
                r2 = types[t2]["radius"]
                sigma = r1+r2
                forcefield[name]["data"].append([t1,t2,epsilon,sigma])

        ############################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forcefield)

    def processSelection(self,selectionType,selectionOptions):
        return None




