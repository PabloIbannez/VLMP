import sys, os
import copy

import logging

from . import globalBase

class NVT(globalBase):

    """
    Component name: NVT
    Component type: globalBase

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

        parameters = {}

        parameters["box"]         = params.get("box")
        parameters["temperature"] = params.get("temperature")

        self.setGlobals({"ensemble":{"type":["Ensemble","NVT"],
                                     "labels":["box","temperature"],
                                     "data":[[copy.deepcopy(parameters["box"]),
                                              copy.deepcopy(parameters["temperature"])]]}})

