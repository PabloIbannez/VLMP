import sys, os

import logging

from . import simulationStepBase

class centerOfMassMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures the center of mass of a selected group of particles throughout the simulation.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for center of mass measurements.",
                "type": "str",
                "default": "com.dat"
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for center of mass calculation.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"centerOfMassMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"com_data.dat\",
                \"selection\": \"model1 type A B C\"
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
              "type":["GeometricalMeasure","CenterOfMassPosition"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



