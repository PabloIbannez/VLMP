import sys, os

import logging

from . import unitsBase

class none(unitsBase):

    """
    Component name: none
    Component type: units

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    None units. All constants are set to 1.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {},
                         requiredParameters  = {},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        self.setUnits("None")

    def getConstant(self,constantName):
        return 1.0
