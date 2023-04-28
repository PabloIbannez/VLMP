import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class constraintCenterOfMassPosition(modelExtensionBase):

    """
    Component name: constraintCenterOfMassPosition
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 14/03/2023

    Apply a constraint to the center of mass of a selection of particles

    :param selection: Selection of particles where the constraint will be applied
    :type selection: list of dictionaries
    :param K: Stiffness of the constraint
    :type K: float
    :param r0: Distance between the center of mass and the constraint position
    :type r0: float
    :param position: Position of the center of mass of the selection
    :type position: list of floats

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"K","r0","position"},
                         requiredParameters  = {"K","r0","position"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        K        = params.get("K")
        #Check if K is a float
        if not isinstance(K,float):
            raise Exception("K must be a float")

        r0       = params.get("r0")
        #Check if r0 is a float
        if not isinstance(r0,float):
            raise Exception("r0 must be a float")

        position = params.get("position")
        #Check if position is a list of floats
        if not isinstance(position,list):
            raise Exception("position must be a list of floats")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set1","FixedHarmonicCenterOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","K","r0","position"]
        extension[name]["data"]   = []

        selectedIds = self.getSelection("selection")

        extension[name]["data"].append([selectedIds,[K,K,K],[r0,r0,r0],position])

        ############################################################

        self.setExtension(extension)



