import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class LennardJones(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Implements Lennard-Jones potential between particles for non-bonded interactions.",
        "parameters": {
            "interactionMatrix": {"description": "Matrix of interaction parameters between different types of particles", "type": "list of lists", "default": null},
            "cutOffFactor": {"description": "Factor to multiply sigma to obtain the cut-off distance", "type": "float", "default": null},
            "addVerletList": {"description": "Whether to add a Verlet list for the interactions", "type": "bool", "default": true},
            "condition": {"description": "Condition for the interaction (e.g., 'inter', 'intra')", "type": "str", "default": "inter"}
        },
        "example": "
        {
            \"type\": \"LennardJones\",
            \"parameters\": {
                \"interactionMatrix\": [[\"A\", \"B\", 1.0, 1.0], [\"B\", \"B\", 0.5, 1.2]],
                \"cutOffFactor\": 2.5,
                \"condition\": \"inter\"
            }
        }"
    }
    """

    availableParameters = {"interactionMatrix","cutOffFactor","addVerletList","condition"}
    requiredParameters  = {"interactionMatrix","cutOffFactor"}
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

        cutOffFactor       = params.get("cutOffFactor")
        interactionMatrix  = params.get("interactionMatrix")

        addVerletList      = params.get("addVerletList",True)

        condition          = params.get("condition","inter")

        extension = {}

        if addVerletList:
            extension["nl"]={}
            extension["nl"]["type"]       =  ["VerletConditionalListSet",  "nonExclIntra_nonExclInter"]
            extension["nl"]["parameters"] =  {}
            extension["nl"]["labels"]      = ["id","id_list"]
            extension["nl"]["data"]        = []

        extension[name] = {}
        extension[name]["type"] = ["NonBonded","GeneralLennardJonesType2"]
        extension[name]["parameters"] = {"cutOffFactor":cutOffFactor,"condition":condition}
        extension[name]["labels"] = ["name_i","name_j","epsilon","sigma"]
        extension[name]["data"]   = interactionMatrix.copy()

        ############################################################

        self.setExtension(extension)



