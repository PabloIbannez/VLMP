import sys, os

import logging

from . import modelOperationBase

import numpy as np

class setParticlePositions(modelOperationBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Sets the positions of a group of particles to specified coordinates.",
        "parameters": {
            "positions": {
                "description": "List of new positions for the selected particles.",
                "type": "list of list of float",
                "default": null
            },
            "ids": {
                "description": "List of particle IDs to move.",
                "type": "list of int",
                "default": null
            }
        },
        "example": "{
            \"type\": \"setParticlePositions\",
            \"parameters\": {
                \"positions\": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
                \"ids\": [0, 1]
            }
        }"
    }
    """

    availableParameters = {"positions","ids"}
    requiredParameters  = {"positions","ids"}
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

        positions = params["positions"]
        ids       = params["ids"]

        self.setIdsState(ids,"position",positions)
