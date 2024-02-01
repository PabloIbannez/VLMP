import sys, os
import copy

import logging

from . import ensembleBase

class NVT(ensembleBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Component for setting up an NVT (constant Number of particles, Volume, and Temperature)
      ensemble in a simulation. This component is used to define the simulation environment
      with a fixed box size and temperature.
      It is essential for simulations that require a controlled temperature and volume,
      commonly used in molecular dynamics and other statistical mechanics simulations.",

     "parameters":{
        "box":{"description":"Size of the simulation box",
               "type":"float"},
        "temperature":{"description":"Temperature of the simulation environment",
                       "type":"float"}
        },

     "example":"
         {
            \"type\":\"NVT\",
            \"box\":10.0,
            \"temperature\":300.0
         }
        "
    }
    """

    availableParameters = {"box", "temperature"}
    requiredParameters  = {"box", "temperature"}

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

        self.setEnsembleName("NVT")

        self.addEnsembleComponent("box",box)
        self.addEnsembleComponent("temperature",temperature)
