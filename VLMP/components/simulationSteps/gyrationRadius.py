import sys, os

import logging

from . import simulationStepBase

class gyrationRadius(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Calculates the radius of gyration for a selected group of particles over time.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for gyration radius measurements.",
                "type": "str",
                "default": "gyration_radius.dat"
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for gyration radius calculation.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"gyrationRadius\",
            \"parameters\": {
                \"outputFilePath\": \"gyration_data.dat\",
                \"selection\": \"model1 type protein\"
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath"}
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

        simulationStep = {
            name:{
              "type":["GeometricalMeasure","GyrationRadius"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



