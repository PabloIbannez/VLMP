import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constantTorqueOverCenterOfMass(modelExtensionBase):

    """
    Component name: constantTorqueOverCenterOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Constant torque over center of mass

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param torque: Torque applied to the center of mass
    :type torque: list of floats

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"torque"},
                         requiredParameters  = {"torque"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        torque = params.get("torque")
        # Check if the torque is a list of floats
        if not isinstance(torque,list):
            raise Exception("Torque must be a list of floats")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set1","ConstantTorqueOverCenterOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","torque"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        extension[name]["data"].append([selectedIds,torque])

        ############################################################

        self.setExtension(extension)



