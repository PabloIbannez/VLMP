import sys, os

import logging

from VLMP.components.types import typesBase

class polarizable(typesBase):
    """
    {"author": "Pablo Diez-Silva",
     "description":
     "Component for defining a polarizable type of particle, with mass, radius, charge and polarizability",
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
        "polarizability":{"description":"Default polarizability for a new type",
                  "type":"float",
                  "default":0.0}
            },
     "example":"
         {
            \"type\":\"polarizable\"
         }
        "
    }
    """

    availableParameters = {"mass","radius","charge","polarizability"}
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

        self.setTypesName("Polarizable")

        self.addTypesComponent("mass", 1.0)
        self.addTypesComponent("radius", 1.0)
        self.addTypesComponent("charge", 0.0)
        self.addTypesComponent("polarizability", 0.0)
