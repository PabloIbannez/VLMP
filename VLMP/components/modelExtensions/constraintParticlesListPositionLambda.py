import sys, os
import copy

import logging

import numpy as np

from . import modelExtensionBase

class constraintParticlesListPositionLambda(modelExtensionBase):

    """
    Component name: constraintParticlesListPositionLambda
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 5/12/2023

    Apply a lambda constraint to the position of a set of particles.
    Particles are given by two lists, one with the ids and the other one with the positions

    :param K: Stiffness of the constraint
    :type K: float
    :param n: Exponent of the constraint
    :type n: int
    :param ids: List of particle ids
    :type ids: list of int
    :param positions: List of particle positions
    :type positions: list of list of float

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"K","n","ids","positions"},
                         requiredParameters  = {"K","ids","positions"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        K        = params["K"]
        n        = params.get("n",2)

        ids      = params["ids"]
        positions= params["positions"]

        #Check if K is a float
        if not isinstance(K,float) and not isinstance(K,list):
            raise Exception("K must be a float or a list of floats")
        if isinstance(K,float):
            K = [K,K,K]

        #Check if ids and positions are a list
        if not isinstance(ids,list):
            raise Exception("ids must be a list of ints")

        if not isinstance(positions,list):
            raise Exception("positions must be list of floats")

        if len(ids) != len(positions):
            raise Exception("ids and positions must have the same len")

        #Check if ids and positions have the same size
        #if len(ids) != len(positions)

        r0 = [0.0,0.0,0.0]

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Bond1","LambdaFixedHarmonic"]
        extension[name]["parameters"] = {"n":n}
        extension[name]["labels"] = ["id_i","position","K","r0"]
        extension[name]["data"]   = []
        for id_,pos in zip(ids,positions):
            extension[name]["data"].append([id_,pos,K,r0])

        ############################################################

        self.setExtension(extension)
