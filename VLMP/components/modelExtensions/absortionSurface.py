import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class absortionSurface(modelExtensionBase):

    """
    Component name: absortionSurface
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 30/08/2023

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"heightThreshold","K"},
                         requiredParameters  = {"heightThreshold","K"},
                         availableSelections = set(),
                         requiredSelections  = set(),
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



