import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantForce(modelExtensionBase):

    """
    Component name: constantForce
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 14/03/2023

    Constant force applied to a set of particles

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

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Bond1","ConstantForce"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["id_i","force"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        for id_i in selectedIds:
            extension[name]["data"].append([id_i,force])

        ############################################################

        self.setExtension(extension)



