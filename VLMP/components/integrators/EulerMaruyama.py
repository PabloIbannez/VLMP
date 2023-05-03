import sys, os

import copy

import logging

from . import integratorBase

class EulerMaruyama(integratorBase):

    """
    Component name: EulerMaruyama
    Component type: integrator

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

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
                         availableParameters = {"integrationSteps","timeStep","viscosity"},
                         requiredParameters  = {"integrationSteps","timeStep","viscosity"},
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
