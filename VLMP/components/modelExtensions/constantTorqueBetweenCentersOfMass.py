import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantTorqueBetweenCentersOfMass(modelExtensionBase):

    """
    Component name: constantTorqueBetweenCentersOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Constant torque between centers of mass of selected particles

    :param selection1: Selection for the first particle group
    :type selection1: list of dictionaries
    :param selection2: Selection for the second particle group
    :type selection2: list of dictionaries
    :param torque: torque applied to the particles
    :type torque: float

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"torque"},
                         requiredParameters  = {"torque"},
                         availableSelections = {"selection1","selection2"},
                         requiredSelections  = {"selection1","selection2"},
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



