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

    :param startStep: first step to show the info
    :type startStep: int, optional
    :param endStep: last step to show the info
    :type endStep: int, optional

    """

    def __init__(self,name,**params):
        super().__init__(_type= self.__class__.__name__,
                         _name= name,
                         availableParameters = set(),
                         requiredParameters  = set(),
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        simulationStep = {
            name:{
                  "type":["UtilsStep","InfoStep"],
                  "parameters":{}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)


