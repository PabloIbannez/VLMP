import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class uniformMagneticField(modelExtensionBase):
    """
    {
        "author": "P. Palacios-Alonso",
        "description": "Applies a uniform magnetic field to selected magnetic particles in the simulation.",
        "parameters": {
            "b0": {"description": "Magnitude of the magnetic field", "type": "float", "default": null},
            "direction": {"description": "Direction of the magnetic field", "type": "list of float", "default": [0, 0, 1]}
        },
        "example": "
        {
            \"type\": \"uniformMagneticField\",
            \"parameters\": {
                \"b0\": 1.0,
                \"direction\": [0, 0, 1]
            }
        }"
    }
    """

    availableParameters = {"b0"}
    requiredParameters  = {"b0"}
    availableSelections = set()
    requiredSelections  = set()

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

        frequency = params.get("frequency")
        b0        = params.get("b0")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["External","UniformMagneticField"]
        extension[name]["parameters"] = {}
        extension[name]["parameters"]["b0"] = b0
        extension[name]["parameters"]["direction"] = [0,0,1]
        ############################################################

        self.setExtension(extension)



