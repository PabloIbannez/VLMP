import sys, os

import logging

from . import simulationStepBase

class info(simulationStepBase):
    """
    Component name: saveState
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    Simple info step, it shows the current step,
    an estimation of the remaining time and the mean FPS.

    :param intervalStep: interval of steps to show the info
    :type intervalStep: int
    :param startStep: first step to show the info
    :type startStep: int, optional
    :param endStep: last step to show the info
    :type endStep: int, optional

    """

    def __init__(self,name,**params):
        super().__init__(_type= self.__class__.__name__,
                         _name= name,
                         availableParameters = {"intervalStep","startStep","endStep"},
                         requiredParameters  = {"intervalStep"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["intervalStep"] = params.get("intervalStep")

        if "startStep" in params:
            parameters["startStep"] = params.get("startStep")
        if "endStep" in params:
            parameters["endStep"]   = params.get("endStep")

        simulationStep = {
            name:{
                  "type":["UtilsStep","InfoStep"],
                  "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)


