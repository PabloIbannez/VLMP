import sys, os

import logging

from . import modelOperationBase

import numpy as np

class setParticlePositions(modelOperationBase):

    """
    Component name: setParticlePositions
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 31/10/2023

    Set the position of a set of particles to a given a list of ids and a position.

    :param positions: Position to set the particles to.
    :type position: list of floats

    """

    availableParameters = {"positions","ids"}
    requiredParameters  = {"positions","ids"}
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

        positions = params["positions"]
        ids       = params["ids"]

        self.setIdsState(ids,"position",positions)
