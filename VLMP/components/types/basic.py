import sys, os

import logging

from . import typesBase

class basic(typesBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Component for defining basic types in a simulation.
      It includes components for mass, radius, and charge, which are essential attributes
      for many simulation scenarios. These properties define the physical characteristics
      of the particles used in the simulation. When a new type is created, if no value is
      given for any of these properties, the default value is used.",
     "parameters":{
        "mass":{"description":"Default mass for a new type",
                "type":"float",
                "default":1.0},
        "radius":{"description":"Default radius for a new type",
                  "type":"float",
                  "default":1.0},
        "charge":{"description":"Default charge for a new type",
                  "type":"float",
                  "default":0.0}
            },
     "example":"
         {
            \"type\":\"basic\"
         }
        "
    }
    """

    availableParameters = {"mass","radius","charge"}
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

        self.setTypesName("Basic")

        self.addTypesComponent("mass", 1.0)
        self.addTypesComponent("radius", 1.0)
        self.addTypesComponent("charge", 0.0)
