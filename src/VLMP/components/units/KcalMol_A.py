import sys, os

import logging

from . import unitsBase

class KcalMol_A(unitsBase):

    """
    Component name: KcalMol_A
    Component type: units

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    (Kcal/mol)/A

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

        self.availableConstants = {
            "kT": 0.593,
            "KBOLTZ":1.987191E-03,
            "ELECOEF":332.0716
        }

        self.setUnits("KcalMol_A")

    def getConstant(self,constantName):
        if constantName not in self.availableConstants:
            self.logger.error("[KcalMol_A] Constant {} not available".format(constantName))
            raise "Constant not available"

        return self.availableConstants[constantName]




