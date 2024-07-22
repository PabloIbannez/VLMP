import sys, os

import logging

from . import simulationStepBase

class meanMagnetizationMeasurement(simulationStepBase):
    """
    {
        "author": "P. Palacios Alonso",
        "description": "Measures the mean magnetization of selected magnetic particles in the system.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for mean magnetization measurements.",
                "type": "str",
                "default": "mean_magnetization.dat"
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of magnetic particles for magnetization measurement.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"meanMagnetizationMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"magnetization_data.dat\",
                \"selection\": \"model1 type magnetic\"
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

        parameters["outputFilePath"] = params["outputFilePath"]

        simulationStep = {
            name:{
              "type":["MagneticMeasure","MeasureMeanMagnetization"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



