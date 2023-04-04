import sys, os

import copy

import logging

from . import integratorBase

class EulerMaruyamaRigidBody(integratorBase):

    """
    Component name: EulerMaruyamaRigidBody
    Component type: integrator

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Euler-Maruyama for rigid bodies. https://doi.org/10.1063/1.4932062

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
            "type" : ["BrownianNVT", "EulerMaruyamaRigidBody"],
            "parameters" : copy.deepcopy(parameters)
        }

        ############################################################

        self.setIntegrationSteps(integrationSteps)
        self.setIntegrator(integrator)