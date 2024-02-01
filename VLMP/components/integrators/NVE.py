import sys, os

import copy

import logging

from . import integratorBase

class NVE(integratorBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "NVE integrator for simulations maintaining a constant number of particles,
      volume, and energy. This integrator is suitable for closed-system simulations
      where energy exchange with the environment is not considered.",

     "parameters":{
        "integrationSteps":{"description":"Number of integration steps",
                            "type":"int"},
        "timeStep":{"description":"Time step of the integrator",
                    "type":"float"}
        },

     "example":"
         {
            \"type\":\"NVE\",
            \"integrationSteps\":10000,
            \"timeStep\":0.001
         }
        "
    }
    """

    availableParameters = {"integrationSteps", "timeStep"}
    requiredParameters  = {"integrationSteps", "timeStep"}

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

        parameters["timeStep"] = params.get("timeStep")

        integrator = {
            "type" : ["Verlet","VelocityVerlet"],
            "parameters" : copy.deepcopy(parameters)
        }

        ############################################################

        self.setIntegrationSteps(integrationSteps)
        self.setIntegrator(integrator)
