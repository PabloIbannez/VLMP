import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class WCA(modelExtensionBase):

    """
    Component name: WCA
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 02/01/2024

    WCA potential between particles.

    :param condition: Condition for the interaction. Options: "inter", "intra" ...
    :type condition: str, default="inter"
    :param epsilon: epsilon parameter of the WCA potential
    :type epsilon: float
    :param cutOffFactor: Factor to multiply the sigma parameter to obtain the cut-off distance.
    :type cutOffFactor: float
    :param addVerletList: If True, a Verlet list will be created for the interactions.
    :type addVerletList: bool, optional, default=True

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"cutOffFactor","epsilon","cutOffFactor","addVerletList","condition"},
                         requiredParameters  = set(),
                         availableSelections = set(),
                         requiredSelections  = set(),
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



