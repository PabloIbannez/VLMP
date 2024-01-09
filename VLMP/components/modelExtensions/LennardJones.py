import sys, os

import logging

import numpy as np

from . import modelExtensionBase

class LennardJones(modelExtensionBase):

    """
    Component name: LennardJones
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 21/09/2023

    Lennard Jones potential between particles.

    :param condition: Condition for the interaction. Options: "inter", "intra" ...
    :type condition: str, default="inter"
    :param interactionMatrix: Matrix of interaction parameters between different types of particles.
    :type interactionMatrix: list of lists. Each list is a row of the matrix. Format type1,type2,epsilon,sigma
    :param cutOffFactor: Factor to multiply the sigma parameter to obtain the cut-off distance.
    :type cutOffFactor: float
    :param addVerletList: If True, a Verlet list will be created for the interactions.
    :type addVerletList: bool, optional, default=True

    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"interactionMatrix","cutOffFactor","addVerletList","condition"},
                         requiredParameters  = {"interactionMatrix","cutOffFactor"},
                         availableSelections = set(),
                         requiredSelections  = set(),
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



