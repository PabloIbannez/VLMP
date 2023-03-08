import sys, os

import logging

from . import integratorBase

class BBK(integratorBase):

    """
    BBK integrator. This is an Langevin integrator with a stochastic force.
    :class:`BBK` is a subclass of :class:`integratorBase`.

    :param timeStep: The time step of the integrator.
    :type timeStep: float
    :param frictionConstant: The friction constant of the integrator.
    :type frictionConstant: float

    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="BBK",
                         _name= name,
                         availableParameters  = ["timeStep","frictionConstant","totalIntegrationTime"],
                         compulsoryParameters = ["timeStep","frictionConstant","totalIntegrationTime"],
                         **kwargs)

        self.integratorClass    = "LangevinNVT"
        self.integratorSubClass = "BBK"

        ############################################################
        ####################  BBK Parameters   #####################
        ############################################################

        self.timeStep         = kwargs["timeStep"]
        self.frictionConstant = kwargs["frictionConstant"]

        self.integratorParameters = {"timeStep":self.timeStep,
                                     "frictionConstant":self.frictionConstant}

        self.totalIntegrationTime = kwargs["totalIntegrationTime"]

        ###################  Units Conversion  ####################

        self.timeStep         = self.units.fromInputToInternalTime(self.timeStep)
        self.frictionConstant = 1.0/self.units.fromInputToInternalTime(1.0/self.frictionConstant)

        self.totalIntegrationTime = self.units.fromInputToInternalTime(self.totalIntegrationTime)

        self.integrationSteps = int(self.totalIntegrationTime/self.timeStep)
