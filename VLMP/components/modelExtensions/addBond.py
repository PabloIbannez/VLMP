from VLMP.components.modelExtensions import modelExtensionBase

import numpy as np

class addBond(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire and Pablo Palacios",
        "description": "Adds a harmonic bond between two particles.",
        "parameters": {
            "K": {"description": "Spring constant for the bond", "type": "float", "default": null},
            "r0": {"description": "Equilibrium distance of the bond", "type": "float", "default": null}
        },
        "selections": {
            "selection1": {"description": "First particle in the bond", "type": "list of ids"},
            "selection2": {"description": "Second particle in the bond", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"addBond\",
            \"parameters\": {
                \"K\": 100.0,
                \"r0\": 1.0,
                \"selection1\": \"model1 id 1\",
                \"selection2\": \"model1 id 2\"
            }
        }"
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
