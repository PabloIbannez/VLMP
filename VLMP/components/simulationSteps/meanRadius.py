import sys, os

import logging

from . import simulationStepBase

class meanRadius(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Calculates the mean radius of selected particles over time.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for mean radius measurements.",
                "type": "str",
                "default": "mean_radius.dat"
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for mean radius calculation.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"meanRadius\",
            \"parameters\": {
                \"outputFilePath\": \"radius_data.dat\",
                \"selection\": \"model1 type sphere\"
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
              "type":["GeometricalMeasure","MeanRadius"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



