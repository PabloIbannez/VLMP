import sys, os
import copy

import logging

import numpy as np

from . import modelExtensionBase

class constraintCenterOfMassPosition(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a constraint to the center of mass of a selection of particles.
                        The potential energy of the constraint is given by a harmonic potential.",
        "parameters": {
            "K": {"description": "Spring constant for the constraint", "type": "float or list of float", "default": null},
            "r0": {"description": "Equilibrium distance from the constraint position", "type": "float", "default": null},
            "position": {"description": "Position to constrain the center of mass to", "type": "list of float", "default": null}
        },
        "selections": {
            "selection": {"description": "Particles to apply the constraint to", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"constraintCenterOfMassPosition\",
            \"parameters\": {
                \"K\": [100.0, 100.0, 0.0],
                \"r0\": 0.0,
                \"position\": [0.0, 0.0, 0.0],
                \"selection\": \"model1\"
            }
        }"
    }
    """

    availableParameters = {"K","r0","position"}
    requiredParameters  = {"K","r0","position"}
    availableSelections = {"selection"}
    requiredSelections  = {"selection"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        K        = params.get("K")
        #Check if K is a float
        if not isinstance(K,float) and not isinstance(K,list):
            raise Exception("K must be a float or a list of floats")
        if isinstance(K,float):
            K = [K,K,K]

        r0       = params.get("r0")
        #Check if r0 is a float
        if not isinstance(r0,float):
            raise Exception("r0 must be a float")

        position = params.get("position")
        #Check if position is a list of floats
        if not isinstance(position,list):
            raise Exception("position must be a list of floats")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set1","FixedHarmonicAnisotropicCenterOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","K","r0","position"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        extension[name]["data"].append([selectedIds,copy.deepcopy(K),[r0,r0,r0],position])

        ############################################################

        self.setExtension(extension)



