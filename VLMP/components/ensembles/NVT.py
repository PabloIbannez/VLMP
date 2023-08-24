import sys, os
import copy

import logging

from . import ensembleBase

class NVT(ensembleBase):

    """
    Component name: NVT
    Component type: ensembleBase

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    Set the box size and temperature.

    :param box: box size
    :type box: float
    :param temperature: temperature
    :type temperature: float

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"box","temperature"},
                         requiredParameters  = {"box","temperature"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        box         = params.get("box")
        temperature = params.get("temperature")

        self.setEnsembleName("NVT")

        self.addEnsembleComponent("box",box)
        self.addEnsembleComponent("temperature",temperature)
