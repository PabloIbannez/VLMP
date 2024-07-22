import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantForce(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a constant force to a selection of particles.
                        The force is applied over each individual particle.",
        "parameters": {
            "force": {
                "description": "Force vector to be applied.",
                "type": "list of float",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to which the force will be applied.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"constantForce\",
            \"parameters\": {
                \"force\": [0.0, 0.0, -9.8],
                \"selection\": \"model1 type A B\"
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

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Bond1","ConstantForce"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["id_i","force"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        for id_i in selectedIds:
            extension[name]["data"].append([id_i,force])

        ############################################################

        self.setExtension(extension)



