import sys, os

import copy

import logging

from . import integratorBase

class NVE(integratorBase):

    """
    Component name: NVE
    Component type: integrator

    Author: Pablo Ibáñez-Freire
    Date: 04/01/2024

    NVE integrator.

    :param integrationSteps: Number of integration steps.
    :type integrationSteps: int
    :param timeStep: Time step of the integrator.
    :type timeStep: float

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"integrationSteps","timeStep"},
                         requiredParameters  = {"integrationSteps","timeStep"},
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
