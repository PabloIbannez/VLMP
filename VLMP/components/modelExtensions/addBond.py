from VLMP.components.modelExtensions import modelExtensionBase

import numpy as np

class addBond(modelExtensionBase):

    """
    Component name: addBond
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire and Pablo Palacios
    Date: 19/06/2023

    Elastic Network Model (ENM).

    :param K: Spring constant.
    :type K: float
    :param r0: Equilibrium distance.
    :type r0: float

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"K","r0"},
                         requiredParameters  = {"K","r0"},
                         availableSelections = {"selection1","selection2"},
                         requiredSelections  = {"selection1","selection2"},
                         **params)

        K   = params["K"]
        r0  = params["r0"]

        ############################################################

        sel1Ids = self.getSelection("selection1")
        sel2Ids = self.getSelection("selection2")

        #Check that the selections have the same number of atoms, 1
        if len(sel1Ids) != 1 or len(sel2Ids) != 1:
            self.logger.error("Selections must have only one atom each.")
            raise ValueError("Selections must have only one atom each.")

        extension = {}

        extension[name] = {}
        extension[name]["type"]       = ["Bond2","Harmonic"]
        extension[name]["parameters"] = {}

        extension[name]["labels"] = ["id_i","id_j","K","r0"]
        extension[name]["data"]   = [[sel1Ids[0],sel2Ids[0],K,r0]]

        ############################################################

        self.setExtension(extension)
