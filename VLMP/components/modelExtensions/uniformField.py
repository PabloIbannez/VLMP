import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class uniformMagneticField(modelExtensionBase):

    """
    Component name: uniformMagneticField
    Component type: modelExtension

    Author: P. Palacios-Alonso
    Date: 16/10/2023

    Alternating current (Uniform) magnetic field applied to a selection of magnetic particles

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param force: Force applied to the particles
    :type force: list of floats

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"b0"},
                         requiredParameters  = {"b0"},
                         availableSelections = set(),
                         requiredSelections  = set(),
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



