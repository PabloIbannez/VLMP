import sys, os
import copy

import logging

import numpy as np

from . import modelExtensionBase

class constraintParticlesListPositionLambda(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a lambda-dependent positional constraint to a list of specified particles.
                        The potential applied is a harmonic potential multiplied by a lambda-dependent factor (lambda^n).",
        "parameters": {
            "K": {
                "description": "Spring constant for the constraint.",
                "type": "float or list of float",
                "default": null
            },
            "n": {
                "description": "Exponent for the lambda dependence.",
                "type": "int",
                "default": 2
            },
            "ids": {
                "description": "List of particle IDs to be constrained.",
                "type": "list of int",
                "default": null
            },
            "positions": {
                "description": "List of positions for each constrained particle.",
                "type": "list of list of float",
                "default": null
            }
        },
        "example": "
        {
            \"type\": \"constraintParticlesListPositionLambda\",
            \"parameters\": {
                \"K\": [100.0, 100.0, 100.0],
                \"n\": 2,
                \"ids\": [1, 2, 3],
                \"positions\": [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [2.0, 2.0, 2.0]]
            }
        }",
        "warning": "This potential requires an ensemble which includes the 'Lambda' variable."
    }
    """

    availableParameters = {"K","n","ids","positions"}
    requiredParameters  = {"K","ids","positions"}
    availableSelections = set()
    requiredSelections  = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
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
        extension[name]["type"] = ["Bond1","LambdaFixedHarmonicAnisotropic"]
        extension[name]["parameters"] = {"n":n}
        extension[name]["labels"] = ["id_i","position","K","r0"]
        extension[name]["data"]   = []
        for id_,pos in zip(ids,positions):
            extension[name]["data"].append([id_,pos,K,r0])

        ############################################################

        self.setExtension(extension)
