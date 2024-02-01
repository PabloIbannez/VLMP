import sys, os
import copy

import logging

from . import ensembleBase

class NVTlambda(ensembleBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Component for setting up an NVTlambda ensemble in a simulation. This ensemble type
      extends the standard NVT (constant Number of particles, Volume, and Temperature)
      by introducing an additional lambda parameter, which is essential for thermodynamic
      integration. The component is used to define the simulation environment with a
      fixed box size, temperature, and the lambda value, enabling more complex
      thermodynamic calculations.",

     "parameters":{
        "box":{"description":"Size of the simulation box",
               "type":"float"},
        "temperature":{"description":"Temperature of the simulation environment",
                       "type":"float"},
        "lambda":{"description":"Lambda parameter for thermodynamic integration",
                  "type":"float"}
        },

     "example":"
         {
            \"type\":\"NVTlambda\",
            \"box\":10.0,
            \"temperature\":300.0,
            \"lambda\":0.5
         }
        "
    }
    """

    availableParameters = {"box", "temperature", "lambda"}
    requiredParameters  = {"box", "temperature", "lambda"}

    def __init__(self, name, **params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        box         = params.get("box")
        temperature = params.get("temperature")
        lambda_     = params.get("lambda")

        self.setEnsembleName("NVTlambda")

        self.addEnsembleComponent("box",box)
        self.addEnsembleComponent("temperature",temperature)
        self.addEnsembleComponent("lambda",lambda_)
