import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantForceOverCenterOfMass(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a constant force to the center of mass of a selection of particles. The applied
                       force is distributed among the particles in the selection according to their mass.",
        "parameters": {
            "force": {
                "description": "Force vector to be applied to the center of mass.",
                "type": "list of float",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles whose center of mass will be affected.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"constantForceOverCenterOfMass\",
            \"parameters\": {
                \"force\": [0.0, 0.0, -9.8],
                \"selection\": \"model1 chain A\"
            }
        }
        "
    }
    """

    availableParameters = {"force"}
    requiredParameters  = {"force"}
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

        force = params.get("force")
        #Check if the force is a list of floats
        if not isinstance(force,list):
            raise Exception("The force must be a list of floats")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set1","ConstantForceOverCenterOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","force"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        extension[name]["data"].append([selectedIds,force])

        ############################################################

        self.setExtension(extension)



