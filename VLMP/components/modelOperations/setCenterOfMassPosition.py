import sys, os

import logging

from . import modelOperationBase

import numpy as np

class setCenterOfMassPosition(modelOperationBase):

    """
    Component name: setCenterOfMassPosition
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Set the center of mass of a selection of particles to a given position.

    :param position: Position to set the center of mass to.
    :type position: list of floats

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"position"},
                         requiredParameters  = {"position"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
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

