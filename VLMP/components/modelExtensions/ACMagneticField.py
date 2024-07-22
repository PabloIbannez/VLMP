import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class ACMagneticField(modelExtensionBase):
    """
    {
        "author": "P. Palacios-Alonso",
        "description": "Applies an alternating current (AC) magnetic field to selected magnetic particles.",
        "parameters": {
            "b0": {"description": "Amplitude of the magnetic field", "type": "float", "default": null},
            "frequency": {"description": "Frequency of the AC field", "type": "float", "default": null},
            "direction": {"description": "Direction of the magnetic field", "type": "list of float", "default": [0, 0, 1]}
        },
        "example": "
        {
            \"type\": \"ACMagneticField\",
            \"parameters\": {
                \"b0\": 1.0,
                \"frequency\": 100.0,
                \"direction\": [0, 0, 1]
            }
        }"
    }
    """

    availableParameters = {"b0", "frequency", "direction"}
    requiredParameters  = {"b0", "frequency"}
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

        frequency = params["frequency"]
        b0        = params["b0"]
        direction = params.get("direction", [0,0,1])

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["External","ACMagneticField"]
        extension[name]["parameters"] = {}
        extension[name]["parameters"]["b0"] = b0
        extension[name]["parameters"]["frequency"] = frequency
        extension[name]["parameters"]["direction"] = direction.copy()
        ############################################################

        self.setExtension(extension)



