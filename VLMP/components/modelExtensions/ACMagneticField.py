import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class ACMagneticField(modelExtensionBase):

    """
    Component name: ACMagneticField
    Component type: modelExtension

    Author: P. Palacios-Alonso
    Date: 16/10/2023

    Alternating current (AC) magnetic field applied to a selection of magnetic particles

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param force: Force applied to the particles
    :type force: list of floats

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"b0", "frequency", "direction"},
                         requiredParameters  = {"b0", "frequency"},
                         availableSelections = set(),
                         requiredSelections  = set(),
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



