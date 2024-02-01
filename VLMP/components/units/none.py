import sys, os

import logging

from . import unitsBase

class none(unitsBase):

    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Component for defining a 'none' unit system in a simulation. This units
      component is used when no specific unit conversions are required.
      It sets all constants, such as the Boltzmann constant
      (KBOLTZ) and the electrostatic coefficient (ELECOEF), to a value of 1. This can
      be particularly useful in simulations where unitless or normalized values are
      preferred, or where specific unit conversions are handled externally.",
     "parameters": {},
     "example":"
         {
            \"type\":\"none\"
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

        self.setUnitsName("None")

        self.addConstant("KBOLTZ",1.0)
        self.addConstant("ELECOEF",1.0)
