import sys, os

import logging

from . import unitsBase

class KcalMol_A(unitsBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Component for defining the unit system of (Kcal/mol)/A in a simulation. This unit
      component, part of the 'units' category, specifies the system's energy and distance
      units as kilocalories per mole and Angstroms, respectively. It includes fundamental
      constants relevant to this unit system, such as the Boltzmann constant (KBOLTZ) and
      the electrostatics coefficient (ELECOEF).",
     "parameters": {},
     "example":"
         {
            \"type\":\"KcalMol_A\"
         }
        "
    }
    """

    availableParameters = set()
    requiredParameters  = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        self.setUnitsName("KcalMol_A")

        self.addConstant("KBOLTZ",1.987191E-03)
        self.addConstant("ELECOEF",332.0716)
