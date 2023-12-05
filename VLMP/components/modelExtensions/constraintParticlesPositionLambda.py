import sys, os
import copy

import logging

import numpy as np

from . import modelExtensionBase

class constraintParticlesPositionLambda(modelExtensionBase):

    """
    Component name: constraintParticlesPositionLambda
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 5/12/2023

    Apply a lambda constraint to the position of a set of particles.

    :param selection: Selection of particles where the constraint will be applied
    :type selection: list of dictionaries
    :param K: Stiffness of the constraint
    :type K: float
    :param n: Exponent of the constraint
    :type n: float

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"K","n"},
                         requiredParameters  = {"K"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        K        = params.get("K")
        n        = params.get("n",2)

        #Check if K is a float
        if not isinstance(K,float) and not isinstance(K,list):
            raise Exception("K must be a float or a list of floats")
        if isinstance(K,float):
            K = [K,K,K]

        r0 = [0.0,0.0,0.0]

        selectedIds  = self.getSelection("selection")
        idsPositions = self.getIdsState(selectedIds,"position")

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Bond1","LambdaFixedHarmonic"]
        extension[name]["parameters"] = {"n":n}
        extension[name]["labels"] = ["id_i","position","K","r0"]
        extension[name]["data"]   = []
        for id_,pos in zip(selectedIds,idsPositions):
            extension[name]["data"].append([id_,pos,K,r0])

        ############################################################

        self.setExtension(extension)
