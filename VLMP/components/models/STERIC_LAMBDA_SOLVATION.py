import sys, os

import logging

import numpy as np

from VLMP.components.models import modelBase

class STERIC_LAMBDA_SOLVATION(modelBase):

    """
    Component name: STERIC_LAMBDA_SOLVATION
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 02/01/2024

    steric lambda solvation model.

    :param concentration: Concentration of the solute in the solvent (in N/V units)
    :type concentration: float
    :param condition: Condition for the interaction. Options: "inter", "intra" ...
    :type condition: str, default="inter"
    :param epsilon: epsilon parameter of the steric potential
    :type epsilon: float
    :param cutOffFactor: Factor to multiply the sigma parameter to obtain the cut-off distance.
    :type cutOffFactor: float
    :alpha: alpha parameter of the steric potential
    :type alpha: float, default=0.5
    :param addVerletList: If True, a Verlet list will be created for the interactions.
    :type addVerletList: bool, optional, default=True
    :param particleName: Name of the particle to be added to the system.
    :type particleName: str, optional, default="W"
    :param particleMass: Mass of the particle to be added to the system.
    :type particleMass: float, optional, default=1.0
    :param particleRadius: Radius of the particle to be added to the system.
    :type particleRadius: float, optional, default=1.0
    :param particleCharge: Charge of the particle to be added to the system.
    :type particleCharge: float, optional, default=0.0
    :param padding: Padding to be added to the box to place the particle.
    :type padding: two lists of three floats, optional, default=[[0.0,0.0,0.0],[0.0,0.0,0.0]]

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"concentration",
                                                "epsilon","cutOffFactor",
                                                "alpha",
                                                "addVerletList","condition",
                                                "particleName",
                                                "particleMass","particleRadius","particleCharge",
                                                "padding"},
                         requiredParameters  = {"concentration",},
                         definedSelections   = {"particleId"},
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

    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += [0]

        return sel




