import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantTorqueOverCenterOfMass(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a constant torque to the center of mass of selected particles.",
        "parameters": {
            "torque": {"description": "Torque vector to be applied", "type": "list of float", "default": null}
        },
        "selections": {
            "selection": {"description": "Particles to apply the torque to", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"constantTorqueOverCenterOfMass\",
            \"parameters\": {
                \"torque\": [0.0, 0.0, 1.0],
                \"selection\": \"model1 type ROTOR\"
            }
        }"
    }
    """

    availableParameters = {"torque"}
    requiredParameters  = {"torque"}
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

        torque = params.get("torque")
        # Check if the torque is a list of floats
        if not isinstance(torque,list):
            raise Exception("Torque must be a list of floats")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set1","ConstantTorqueOverCenterOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","torque"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        extension[name]["data"].append([selectedIds,torque])

        ############################################################

        self.setExtension(extension)



