import sys, os

import logging

from . import simulationStepBase

class heightMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures the height of selected particles, typically used in surface-based simulations.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for height measurements.",
                "type": "str",
                "default": "height.dat"
            },
            "particleNumberAverage": {
                "description": "Number of particles to average for height calculation.",
                "type": "int",
                "default": 1
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for height measurement.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"heightMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"height_data.dat\",
                \"particleNumberAverage\": 5,
                \"selection\": \"model1 type surface\"
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath","particleNumberAverage"}
    requiredParameters  = {"outputFilePath"}
    availableSelections = {"selection"}
    requiredSelections  = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params.get("outputFilePath")

        if "particleNumberAverage" in params:
            parameters["particleNumberAverage"] = params.get("particleNumberAverage")

        simulationStep = {
            name:{
              "type":["GeometricalMeasure","Height"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



