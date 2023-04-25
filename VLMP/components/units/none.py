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
                         availableParameters = set(),
                         requiredParameters  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        self.setUnitsName("None")

        self.addConstant("kT",1.0)
        self.addConstant("KBOLTZ",1.0)
        self.addConstant("ELECOEF",1.0)
