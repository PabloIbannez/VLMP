import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class harmonicBondBetweenCentersOfMass(modelExtensionBase):

    """
    Component name: harmonicBondBetweenCentersOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Harmonic bond between centers of mass

    :param selection1: Selection for the first particle group
    :type selection1: list of dictionaries
    :param selection2: Selection for the second particle group
    :type selection2: list of dictionaries
    :param K: Spring constant
    :type K: float
    :param r0: Equilibrium distance
    :type r0: float

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"K","r0"},
                         requiredParameters  = {"K","r0"},
                         availableSelections = {"selection1","selection2"},
                         requiredSelections  = {"selection1","selection2"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        K  = params.get("K")
        #Check if K is a float
        if not isinstance(K,float):
            raise Exception("K must be a float")

        r0 = params.get("r0")
        #Check if r0 is a float
        if not isinstance(r0,float):
            raise Exception("r0 must be a float")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Set2","HarmonicBondBetweenCentersOfMass"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["idSet_i","idSet_j","K","r0"]
        extension[name]["data"]   = []

        selectedIds1 = self.getSelection("selection1")
        selectedIds2 = self.getSelection("selection2")

        extension[name]["data"].append([selectedIds1,selectedIds2,K,r0])

        ############################################################

        self.setExtension(extension)



