import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantTorqueBetweenCentersOfMass(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a constant torque between the centers of mass of two groups of particles.
                        The torque is applied in such a way that the two groups of particles
                        rotate in opposite directions around the axis defined by the vector",
        "parameters": {
            "torque": {"description": "Magnitude of the torque to be applied", "type": "float", "default": null}
        },
        "selections": {
            "selection1": {"description": "First group of particles", "type": "list of ids"},
            "selection2": {"description": "Second group of particles", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"constantTorqueBetweenCentersOfMass\",
            \"parameters\": {
                \"torque\": 1.0,
                \"selection1\": \"model1 chain A\",
                \"selection2\": \"model1 chain B\"
            }
        }"
    }
    """

    availableParameters = {"torque"}
    requiredParameters  = {"torque"}
    availableSelections = {"selection1","selection2"}
    requiredSelections  = {"selection1","selection2"}

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
        #Check it torque is a float
        if not isinstance(torque,float):
            raise Exception("torque must be a float")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set2","ConstantTorqueBetweenCentersOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","idSet_j","torque"]
        extension[name]["data"]   = []

        selectedIds1 = self.getSelection("selection1")
        selectedIds2 = self.getSelection("selection2")

        extension[name]["data"].append([selectedIds1,selectedIds2,torque])

        ############################################################

        self.setExtension(extension)



