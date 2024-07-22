import sys, os
import copy

import logging

import numpy as np

from . import modelExtensionBase

class constraintParticlesPositionLambda(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a lambda-dependent positional constraint to a selection of particles.
                        The applied potential is an harmonic potential with a lambda-dependent spring constant.
                        (lambda^(n))",
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
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to be constrained.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"constraintParticlesPositionLambda\",
            \"parameters\": {
                \"K\": [100.0, 100.0, 100.0],
                \"n\": 2,
                \"selection\": \"model1 type A B C\"
            }
        }
        ",
        "warning": "This potential requires an ensemble which includes the 'Lambda' variable."
    }
    """

    availableParameters = {"K","n"}
    requiredParameters  = {"K"}
    availableSelections = {"selection"}
    requiredSelections  = {"selection"}

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
        extension[name]["type"] = ["Bond1","LambdaFixedHarmonicAnisotropic"]
        extension[name]["parameters"] = {"n":n}
        extension[name]["labels"] = ["id_i","position","K","r0"]
        extension[name]["data"]   = []
        for id_,pos in zip(selectedIds,idsPositions):
            extension[name]["data"].append([id_,pos,K,r0])

        ############################################################

        self.setExtension(extension)
