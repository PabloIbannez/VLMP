import sys, os

import copy

import logging

from . import integratorBase

class MagneticBrownian(integratorBase):
    """
    {"author": "P. Palacios-Alonso",
     "description":
     "Simple Euler-Maruyama integrator adapted for Brownian dynamics with magnetic
      properties. It is designed for simulating the behavior of magnetically responsive
      particles in a fluid, considering viscosity, gyromagnetic ratio, damping, and
      saturation magnetization.",

     "parameters":{
        "integrationSteps":{"description":"Number of integration steps",
                            "type":"int"},
        "timeStep":{"description":"Time step of the integrator",
                    "type":"float"},
        "viscosity":{"description":"Viscosity of the fluid",
                     "type":"float"},
        "gyroRatio":{"description":"Gyromagnetic ratio",
                     "type":"float"},
        "damping":{"description":"Damping factor",
                   "type":"float"},
        "msat":{"description":"Saturation magnetization",
                "type":"float"},
        "magneticIntegrationAlgorithm":{"description":"Algorithm for magnetic integration",
                                        "type":"string"}
        },

     "example":"
         {
            \"type\":\"MagneticBrownian\",
            \"integrationSteps\":10000,
            \"timeStep\":0.001,
            \"viscosity\":0.01,
            \"gyroRatio\":2.8,
            \"damping\":0.1,
            \"msat\":1.0,
            \"magneticIntegrationAlgorithm\":\"algorithmName\"
         }
        "
    }
    """

    availableParameters = {"integrationSteps", "timeStep", "viscosity", "gyroRatio", "damping", "msat", "magneticIntegrationAlgorithm"}
    requiredParameters  = {"integrationSteps", "timeStep", "viscosity", "gyroRatio", "damping", "msat", "magneticIntegrationAlgorithm"}

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

        parameters["timeStep"]  = params.get("timeStep")
        parameters["viscosity"] = params.get("viscosity")
        parameters["gyroRatio"] = params.get("gyroRatio")
        parameters["damping"]   = params.get("damping")
        parameters["msat"]      = params.get("msat")
        parameters["magneticIntegrationAlgorithm"] = params.get("magneticIntegrationAlgorithm")


        integrator = {
            "type" : ["Magnetic", "Brownian"],
            "parameters" : copy.deepcopy(parameters)
        }

        ############################################################

        self.setIntegrationSteps(integrationSteps)
        self.setIntegrator(integrator)
