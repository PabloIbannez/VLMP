import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantForceBetweenCentersOfMass(modelExtensionBase):

    """
    Component name: constantForceBetweenCentersOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Constant force between centers of mass of selected particles

    :param selection1: Selection for the first particle group
    :type selection1: list of dictionaries
    :param selection2: Selection for the second particle group
    :type selection2: list of dictionaries
    :param force: Force applied to the particles
    :type force: float

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters  = {"force"},
                         requiredParameters   = {"force"},
                         availableSelections  = {"selection1","selection2"},
                         requiredSelections   = {"selection1","selection2"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        force = params.get("force")
        # Check if the force is a float
        if not isinstance(force,float):
            raise Exception("The force must be a float")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set2","ConstantForceBetweenCentersOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","idSet_j","force"]
        extension[name]["data"]   = []

        selectedIds1 = self.getSelection("selection1")
        selectedIds2 = self.getSelection("selection2")

        extension[name]["data"].append([selectedIds1,selectedIds2,force])

        ############################################################

        self.setExtension(extension)



