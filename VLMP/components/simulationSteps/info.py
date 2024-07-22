import sys, os

import logging

from . import simulationStepBase

class info(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Provides basic information about the simulation progress, including current step, estimated remaining time, and mean FPS.",
        "parameters": {},
        "example": "
        {
            \"type\": \"info\",
            \"parameters\": {}
        }
        "
    }
    """

    availableParameters = set()
    requiredParameters  = set()
    availableSelections = set()
    requiredSelections  = set()

    def __init__(self,name,**params):
        super().__init__(_type= self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
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


