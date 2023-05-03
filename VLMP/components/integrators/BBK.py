import sys, os

import copy

import logging

from . import integratorBase

class BBK(integratorBase):

    """
    Component name: BBK
    Component type: integrator

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    BBK integrator. It is a Langevin integrator for the NVT ensemble.

    :param integrationSteps: Number of integration steps.
    :type integrationSteps: int
    :param timeStep: Time step of the integrator.
    :type timeStep: float
    :param frictionConstant: Friction constant of the integrator.
    :type frictionConstant: float


    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"integrationSteps","timeStep","frictionConstant"},
                         requiredParameters  = {"integrationSteps","timeStep","frictionConstant"},
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
