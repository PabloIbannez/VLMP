#Template for the MODEL_EXTENSION component.
#This template is used to create the MODEL_EXTENSION component.
#Comments begin with a hash (#) and they can be removed.

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

    :param applyOnModel: List of models where the component is applied
    :type applyOnModel: list of strings
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
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        force = params.get("force")

        extension = {}

        extension["constantForce"] = {}
        extension["constantForce"]["type"] = ["Bond1","ConstantForce"]
        extension["constantForce"]["parameters"] = {}
        extension["constantForce"]["labels"] = ["id_i","force"]
        extension["constantForce"]["data"]   = []

        selectedIds = self.getSelection("selection")

        for id_i in selectedIds:
            extension["constantForce"]["data"].append([id_i,force])

        ############################################################

        self.setExtension(extension)



