import sys, os

import copy

import logging

from . import integratorBase

class EulerMaruyamaRigidBodyPatchesState(integratorBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "Euler-Maruyama integrator designed for rigid bodies with patches state. This
      integrator extends the standard Euler-Maruyama approach to accommodate simulations
      involving rigid bodies with specific patches states, adding complexity and realism to
      the simulated dynamics. The update of the patches state is performed using the
      a Monte Carlo approach, after the Euler-Maruyama update of the rigid body state.
      Random numbers are generated and used to decide whether a patch is going to be
      update its state or not.",
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
            \"type\":\"EulerMaruyamaRigidBodyPatchesState\",
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
            "type" : ["Brownian", "EulerMaruyamaRigidBodyPatchesState"],
            "parameters" : copy.deepcopy(parameters)
        }

        ############################################################

        self.setIntegrationSteps(integrationSteps)
        self.setIntegrator(integrator)
