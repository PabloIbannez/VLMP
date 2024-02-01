import sys, os

import logging

from . import typesBase

class none(typesBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Component representing a 'none' type in a simulation.
      Essentially, it signifies that no additional components or special characteristics are
      associated with the entity. This can be useful in simulations where certain entities need
      to be defined but do not require specific attributes or behaviors.",

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

        self.setTypesName("None")
