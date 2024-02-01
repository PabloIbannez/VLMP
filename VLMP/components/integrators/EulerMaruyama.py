import sys, os

import copy

import logging

from . import integratorBase

class EulerMaruyama(integratorBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Simple Euler-Maruyama integrator for Brownian dynamics. This integrator is suitable
      for simulations involving stochastic processes, particularly in fluid environments
      with defined viscosity.",

     "parameters":{
        "integrationSteps":{"description":"Number of integration steps",
                            "type":"int"},
        "timeStep":{"description":"Time step of the integrator",
                    "type":"float"},
        "viscosity":{"description":"Viscosity of the fluid",
                     "type":"float"}
        },

     "example":"
         {
            \"type\":\"EulerMaruyama\",
            \"integrationSteps\":10000,
            \"timeStep\":0.001,
            \"viscosity\":0.01
         }
        "
    }
    """

    availableParameters = {"integrationSteps", "timeStep", "viscosity"}
    requiredParameters  = {"integrationSteps", "timeStep", "viscosity"}

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
        parameters["viscosity"]        = params.get("viscosity")

        integrator = {
            "type" : ["Brownian", "EulerMaruyama"],
            "parameters" : copy.deepcopy(parameters)
        }

        ############################################################

        self.setIntegrationSteps(integrationSteps)
        self.setIntegrator(integrator)
