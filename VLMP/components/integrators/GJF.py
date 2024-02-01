import sys, os

import copy

import logging

from . import integratorBase

class GFJ(integratorBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "GJF integrator, a Langevin integrator for the NVT ensemble, as described in
      DOI: 10.1080/00268976.2012.760055. This integrator is designed for simulations
      that maintain a constant number of particles, volume, and temperature, incorporating
      stochastic thermal noise and friction in the dynamics.",

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
            \"type\":\"GFJ\",
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
            "type" : ["Langevin","GJF"],
            "parameters" : copy.deepcopy(parameters)
        }

        ############################################################

        self.setIntegrationSteps(integrationSteps)
        self.setIntegrator(integrator)
