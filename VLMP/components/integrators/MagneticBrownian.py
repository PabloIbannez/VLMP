import sys, os

import copy

import logging

from . import integratorBase

class MagneticBrownian(integratorBase):

    """
    Component name: MagneticBrownian
    Component type: integrator

    Author: P. Palacios-Alonso
    Date: 17/10/2023

    Simple Euler-Maruyama integrator for brownian dynamics.

    :param integrationSteps: Number of integration steps.
    :type integrationSteps: int
    :param timeStep: Time step of the integrator.
    :type timeStep: float
    :param viscosity: Viscosity of the fluid.
    :type viscosity: float


    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"integrationSteps","timeStep","viscosity",
                                                "gyroRatio", "damping", "msat",
                                                "magneticIntegrationAlgorithm"},
                         requiredParameters  = {"integrationSteps","timeStep","viscosity",
                                                "gyroRatio", "damping", "msat",
                                                "magneticIntegrationAlgorithm"},
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
