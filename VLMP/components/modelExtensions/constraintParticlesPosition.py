import sys, os
import copy

import logging

import numpy as np

from . import modelExtensionBase

class constraintParticlesPosition(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Applies a positional constraint to a selection of particles.
                        The constraint is a harmonic potential with a spring constant K.",
        "parameters": {
            "K": {
                "description": "Spring constant for the constraint.",
                "type": "float or list of float",
                "default": null
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
            \"type\": \"constraintParticlesPosition\",
            \"parameters\": {
                \"K\": [100.0, 100.0, 100.0],
                \"selection\": \"model1 type A B C\"
            }
        }
        "
    }
    """

    availableParameters = {"K"}
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
        extension[name]["type"] = ["Bond1","FixedHarmonicAnisotropic"]
        extension[name]["parameters"] = {}
        extension[name]["labels"] = ["id_i","position","K","r0"]
        extension[name]["data"]   = []
        for id_,pos in zip(selectedIds,idsPositions):
            extension[name]["data"].append([id_,pos,K,r0])

        ############################################################

        self.setExtension(extension)



