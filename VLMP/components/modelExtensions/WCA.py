import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class WCA(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Adds Weeks-Chandler-Andersen (WCA) potential interactions between particles.",
        "parameters": {
            "condition": {
                "description": "Condition for the interaction.",
                "type": "str",
                "default": "inter"
            },
            "epsilon": {
                "description": "Energy parameter for the WCA potential.",
                "type": "float",
                "default": 1.0
            },
            "cutOffFactor": {
                "description": "Factor to multiply the sigma parameter to obtain the cut-off distance.",
                "type": "float",
                "default": 2.5
            },
            "addVerletList": {
                "description": "If True, a Verlet list will be created for the interactions.",
                "type": "bool",
                "default": true
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for WCA interactions.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"WCA\",
            \"parameters\": {
                \"condition\": \"inter\",
                \"epsilon\": 1.0,
                \"cutOffFactor\": 2.5,
                \"addVerletList\": true,
                \"selection\": \"model1 all\"
            }
        }
        "
    }
    """

    availableParameters = {"cutOffFactor","epsilon","cutOffFactor","addVerletList","condition"}
    requiredParameters  = set()
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

        cutOffFactor  = params.get("cutOffFactor",2.5)
        epsilon       = params.get("epsilon",1.0)

        addVerletList = params.get("addVerletList",True)
        condition     = params.get("condition","inter")

        extension = {}

        if addVerletList:
            extension["nl"]={}
            extension["nl"]["type"]       =  ["VerletConditionalListSet",  "nonExclIntra_nonExclInter"]
            extension["nl"]["parameters"] =  {}
            extension["nl"]["labels"]      = ["id","id_list"]
            extension["nl"]["data"]        = []

        extension[name] = {}
        extension[name]["type"] = ["NonBonded","WCAType2"]
        extension[name]["parameters"] = {"cutOffFactor":cutOffFactor,"condition":condition}
        extension[name]["labels"] = ["name_i","name_j","epsilon","sigma"]
        extension[name]["data"]   = []

        types = self.getTypes().getTypes()
        for t1 in types:
            for t2 in types:
                r1 = types[t1]["radius"]
                r2 = types[t2]["radius"]
                sigma = r1+r2
                extension[name]["data"].append([t1,t2,epsilon,sigma])

        ############################################################

        self.setExtension(extension)



