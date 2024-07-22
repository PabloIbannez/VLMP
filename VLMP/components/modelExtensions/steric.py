import sys, os

import logging

import numpy as np

from . import modelExtensionBase
from ...utils.input import getLabelIndex

class steric(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Adds steric interactions between particles. If molecules are bonded, the interaction is not considered.",
        "parameters": {
            "condition": {
                "description": "Condition for the interaction.",
                "type": "str",
                "default": "inter"
            },
            "epsilon": {
                "description": "Energy parameter for the interaction.",
                "type": "float",
                "default": null
            },
            "cutOffFactor": {
                "description": "Factor to multiply the sigma parameter to obtain the cut-off distance.",
                "type": "float",
                "default": null
            },
            "addVerletList": {
                "description": "If True, a Verlet list will be created for the interactions.",
                "type": "bool",
                "default": true
            },
            "excludedBonds": {
                "description": "Number of bonds to exclude from the steric interactions.
                                This option is only available if addVerletList is True.
                                If excludedBonds > 0, the Verlet list will be created
                                with the non-bonded interactions and the excluded bonds.",
                "type": "int",
                "default": 0
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for steric interactions.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"steric\",
            \"parameters\": {
                \"condition\": \"inter\",
                \"epsilon\": 1.0,
                \"cutOffFactor\": 2.5,
                \"addVerletList\": true,
                \"selection\": \"model1 type A B C\"
            }
        }
        "
    }
    """

    availableParameters = {"epsilon","cutOffFactor","excludedBonds","addVerletList","condition"}
    requiredParameters  = {"epsilon","cutOffFactor"}
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

        epsilon            = params.get("epsilon")
        cutOffFactor       = params.get("cutOffFactor",1.0)

        excludedBonds      = params.get("excludedBonds",0)
        addVerletList      = params.get("addVerletList",True)
        condition          = params.get("condition","inter")

        if excludedBonds > 0 and addVerletList == False:
            self.logger.error("[steric] excludedBonds > 0 and addVerletList == False. This is not allowed. Exiting...")
            raise Exception("Not compatible parameters.")

        ############################################################

        # Build the interaction matrix
        interactionMatrix = []

        types = self.getTypes().getTypes()
        for t1 in types:
            for t2 in types:
                interaction = [t1,t2,epsilon,types[t1]["radius"] + types[t2]["radius"]]
                interactionMatrix.append(interaction)

        extension = {}

        if addVerletList:
            extension["nl"]={}
            extension["nl"]["type"]       =  ["VerletConditionalListSet", "nonExclIntra_nonExclInter"]
            extension["nl"]["parameters"] =  {}

            exclusions = {}

            if excludedBonds > 0:
                #Add bond2
                for mdl in self.getModels():
                    for bondName,info in mdl.getForceField().items():
                        type_ = info["type"][0]
                        if type_ == "Bond2":
                            index_i = getLabelIndex("id_i",info["labels"])
                            index_j = getLabelIndex("id_j",info["labels"])

                            for d in info["data"]:
                                i = d[index_i]+mdl.getIdOffset()
                                j = d[index_j]+mdl.getIdOffset()

                                if i not in exclusions:
                                    exclusions[i] = set()
                                if j not in exclusions:
                                    exclusions[j] = set()

                                exclusions[i].add(j)
                                exclusions[j].add(i)

            if excludedBonds > 1:
                #Add bond3
                for mdl in self.getModels():
                    for bondName,info in mdl.getForceField().items():
                        type_ = info["type"][0]
                        if type_ == "Bond3":
                            index_i = getLabelIndex("id_i",info["labels"])
                            index_j = getLabelIndex("id_j",info["labels"])
                            index_k = getLabelIndex("id_k",info["labels"])

                            for d in info["data"]:
                                i = d[index_i]+mdl.getIdOffset()
                                j = d[index_j]+mdl.getIdOffset()
                                k = d[index_k]+mdl.getIdOffset()

                                if i not in exclusions:
                                    exclusions[i] = set()
                                if j not in exclusions:
                                    exclusions[j] = set()
                                if k not in exclusions:
                                    exclusions[k] = set()

                                exclusions[i].add(j)
                                exclusions[i].add(k)
                                exclusions[j].add(i)
                                exclusions[j].add(k)
                                exclusions[k].add(i)
                                exclusions[k].add(j)

            if excludedBonds > 2:
                #Add bond4
                for mdl in self.getModels():
                    for bondName,info in mdl.getForceField().items():
                        type_ = info["type"][0]
                        if type_ == "Bond4":
                            index_i = getLabelIndex("id_i",info["labels"])
                            index_j = getLabelIndex("id_j",info["labels"])
                            index_k = getLabelIndex("id_k",info["labels"])
                            index_l = getLabelIndex("id_l",info["labels"])

                            for d in info["data"]:
                                i = d[index_i]+mdl.getIdOffset()
                                j = d[index_j]+mdl.getIdOffset()
                                k = d[index_k]+mdl.getIdOffset()
                                l = d[index_l]+mdl.getIdOffset()

                                if i not in exclusions:
                                    exclusions[i] = set()
                                if j not in exclusions:
                                    exclusions[j] = set()
                                if k not in exclusions:
                                    exclusions[k] = set()
                                if l not in exclusions:
                                    exclusions[l] = set()

                                exclusions[i].add(j)
                                exclusions[i].add(k)
                                exclusions[i].add(l)
                                exclusions[j].add(i)
                                exclusions[j].add(k)
                                exclusions[j].add(l)
                                exclusions[k].add(i)
                                exclusions[k].add(j)
                                exclusions[k].add(l)
                                exclusions[l].add(i)
                                exclusions[l].add(j)
                                exclusions[l].add(k)

            extension["nl"]["labels"]      = ["id","id_list"]
            extension["nl"]["data"]        = []
            for i in exclusions:
                extension["nl"]["data"].append([i,list(exclusions[i])])

        extension[name] = {}
        extension[name]["type"] = ["NonBonded","WCAType2"]
        extension[name]["parameters"] = {"cutOffFactor":cutOffFactor,"condition":condition}
        extension[name]["labels"] = ["name_i","name_j","epsilon","sigma"]
        extension[name]["data"]   = interactionMatrix.copy()

        ############################################################

        self.setExtension(extension)



