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

        self.setUnitsName("KcalMol_A")

        self.addConstant("kT",0.593)
        self.addConstant("KBOLTZ",1.987191E-03)
        self.addConstant("ELECOEF",332.0716)
