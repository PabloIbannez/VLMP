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

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"positions","ids"},
                         requiredParameters  = {"positions","ids"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        positions = params["positions"]
        ids       = params["ids"]

        self.setIdsState(ids,"position",positions)
