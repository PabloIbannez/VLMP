import sys, os
import copy

import logging

from . import ensembleBase

class NVTlambda(ensembleBase):

    """
    Component name: NVTlambda
    Component type: ensemble

    Author: Pablo Ibáñez-Freire
    Date: 6/11/2023

    Set the box size, temperature and lambda. Lambda is the parameter for thermodynamic integration.

    :param box: box size
    :type box: float
    :param temperature: temperature
    :type temperature: float
    :param lambda: lambda
    :type lambda: float

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"box","temperature","lambda"},
                         requiredParameters  = {"box","temperature","lambda"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        box         = params.get("box")
        temperature = params.get("temperature")
        lambda_     = params.get("lambda")

        self.setEnsembleName("NVTlambda")

        self.addEnsembleComponent("box",box)
        self.addEnsembleComponent("temperature",temperature)
        self.addEnsembleComponent("lambda",lambda_)
