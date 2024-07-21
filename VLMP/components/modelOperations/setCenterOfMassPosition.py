import sys, os

import logging

from . import modelOperationBase

import numpy as np

class setCenterOfMassPosition(modelOperationBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Sets the center of mass of a selection of particles to a specified position.",
        "parameters": {
            "position": {
                "description": "Target position for the center of mass.",
                "type": "list of float",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to move.",
                "type": "list of ids"
            }
        },
        "example": "{
            \"type\": \"setCenterOfMassPosition\",
            \"parameters\": {
                \"position\": [0.0, 0.0, 0.0],
                \"selection\": \"model1 type A B C\"
            }
        }"
    }
    """

    availableParameters = {"position"}
    requiredParameters  = {"position"}
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

        selectedIds = self.getSelection("selection")

        masses = np.asarray(self.getIdsProperty(selectedIds,"mass"))
        pos    = np.asarray(self.getIdsState(selectedIds,"position"))

        totalMass = np.sum(masses)
        com       = np.sum(masses[:,np.newaxis]*pos,axis=0)/totalMass

        translation = np.asarray(params.get("position")) - com

        pos += translation
        pos = pos.tolist()

        self.setIdsState(selectedIds,"position",pos)

