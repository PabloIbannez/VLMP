import sys, os

import logging

from . import systemBase

class seed(systemBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "This component sets the seed for the random number generator",
     "parameters":{
        "seed":{"description":"Seed for the random number generator",
                "type":"int"}
            },

     "example":"
         {
            \"type\":\"seed\",
            \"seed\":123456
         }
        "
    }
    """

    availableParameters = {"seed"}
    requiredParameters  = {"seed"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        system = {
            name:{"type":["Simulation","Information"],
                  "parameters":{}}
        }

        system[name]["parameters"]["seed"] = params.get("seed")

        ############################################################

        self.setSystem(system)

