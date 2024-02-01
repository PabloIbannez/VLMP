import sys, os

import copy

import logging

from . import integratorBase

class BBK(integratorBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "BBK integrator for the NVT ensemble. This Langevin integrator is designed for
      simulations that maintain a constant number of particles, volume, and temperature.
      It is particularly useful for molecular dynamics simulations requiring stochastic
      thermal noise and friction.",

     "parameters":{
        "integrationSteps":{"description":"Number of integration steps",
                            "type":"int"},
        "timeStep":{"description":"Time step of the integrator",
                    "type":"float"},
        "frictionConstant":{"description":"Friction constant of the integrator",
                            "type":"float"}
        },

     "example":"
         {
            \"type\":\"BBK\",
            \"integrationSteps\":10000,
            \"timeStep\":0.001,
            \"frictionConstant\":0.1
         }
        "
    }
    """

    availableParameters = {"integrationSteps", "timeStep", "frictionConstant"}
    requiredParameters  = {"integrationSteps", "timeStep", "frictionConstant"}

    def __init__(self, name, **params):
        super().__init__(_type=self.__class__.__name__, _name=name,
                         availableParameters=self.availableParameters,
                         requiredParameters=self.requiredParameters,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        integrationSteps = params.get("integrationSteps")

        parameters = {}

        parameters["timeStep"]         = params.get("timeStep")
        parameters["frictionConstant"] = params.get("frictionConstant")

        integrator = {
            "type" : ["Langevin","BBK"],
            "parameters" : copy.deepcopy(parameters)
        }

        ############################################################

        self.setIntegrationSteps(integrationSteps)
        self.setIntegrator(integrator)
