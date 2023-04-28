import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantForceOverCenterOfMass(modelExtensionBase):

    """
    Component name: constantForceOverCenterOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Applies a constant force over the center of mass of a selection of particles.

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param force: Force applied to the particles
    :type force: list of floats

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"force"},
                         requiredParameters  = {"force"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        force = params.get("force")
        #Check if the force is a list of floats
        if not isinstance(force,list):
            raise Exception("The force must be a list of floats")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set1","ConstantForceOverCenterOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","force"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        extension[name]["data"].append([selectedIds,force])

        ############################################################

        self.setExtension(extension)



