import sys, os

import logging

from . import simulationStepBase

class AFMMaxForce(simulationStepBase):
    """
    Component name: AFMMaxForce
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 31/08/2023

    """

    def __init__(self,name,**params):
        super().__init__(_type= self.__class__.__name__,
                         _name= name,
                         availableParameters = {"maxForce"},
                         requiredParameters  = {"maxForce"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        maxForce = params["maxForce"]

        simulationStep = {
            name:{
                  "type":["FlowControl","AFMMaxForce"],
                  "parameters":{"maxForce":maxForce}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)


