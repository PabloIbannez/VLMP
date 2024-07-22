import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class harmonicBondBetweenCentersOfMass(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Adds a harmonic bond between the centers of mass of two groups of particles.",
        "parameters": {
            "K": {
                "description": "Spring constant for the harmonic bond.",
                "type": "float",
                "default": null
            },
            "r0": {
                "description": "Equilibrium distance for the harmonic bond.",
                "type": "float",
                "default": null
            }
        },
        "selections": {
            "selection1": {
                "description": "Selection for the first group of particles.",
                "type": "list of ids"
            },
            "selection2": {
                "description": "Selection for the second group of particles.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"harmonicBondBetweenCentersOfMass\",
            \"parameters\": {
                \"K\": 100.0,
                \"r0\": 5.0,
                \"selection1\": \"model1 chain A\",
                \"selection2\": \"model2 chain B\"
            }
        }
        "
    }
    """

    availableParameters = {"K","r0"}
    requiredParameters  = {"K","r0"}
    availableSelections = {"selection1","selection2"}
    requiredSelections  = {"selection1","selection2"}

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



