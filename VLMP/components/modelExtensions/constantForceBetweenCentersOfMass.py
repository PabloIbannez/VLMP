import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantForceBetweenCentersOfMass(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a constant force between the centers of mass of two groups of particles.",
        "parameters": {
            "force": {
                "description": "Magnitude of the force to be applied.",
                "type": "float",
                "default": null
            }
        },
        "selections": {
            "selection1": {
                "description": "Selection for the first group of particles.",
                "type": "list of ids"
            },
            "selection2": {
                "description": "Selection for the second group of particles.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"constantForceBetweenCentersOfMass\",
            \"parameters\": {
                \"force\": 10.0,
                \"selection1\": \"model1 chain A\",
                \"selection2\": \"model2 chain B\"
            }
        }
        "
    }
    """

    availableParameters  = {"force"}
    requiredParameters   = {"force"}
    availableSelections  = {"selection1","selection2"}
    requiredSelections   = {"selection1","selection2"}

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
        # Check if the force is a float
        if not isinstance(force,float):
            raise Exception("The force must be a float")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set2","ConstantForceBetweenCentersOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","idSet_j","force"]
        extension[name]["data"]   = []

        selectedIds1 = self.getSelection("selection1")
        selectedIds2 = self.getSelection("selection2")

        extension[name]["data"].append([selectedIds1,selectedIds2,force])

        ############################################################

        self.setExtension(extension)



