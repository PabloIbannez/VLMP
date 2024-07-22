import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class absortionSurface(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Implements an absorption surface that attracts particles within a certain distance.
                        Once the interaction starts this potential add an harmonic contraint to the particles
                        that are below the heightThreshold",
        "parameters": {
            "heightThreshold": {"description": "Height above the surface where absorption starts", "type": "float", "default": null},
            "K": {"description": "Spring constant for the absorption force", "type": "float", "default": null}
        },
        "example": "
        {
            \"type\": \"absortionSurface\",
            \"parameters\": {
                \"heightThreshold\": 5.0,
                \"K\": 10.0
            }
        }"
    }
    """

    availableParameters = {"heightThreshold","K"}
    requiredParameters  = {"heightThreshold","K"}
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

        heightThreshold = params["heightThreshold"]
        K               = params["K"]

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Surface","Absorbed"]
        extension[name]["parameters"] = {"heightThreshold":heightThreshold,"K":K}

        ############################################################

        self.setExtension(extension)



