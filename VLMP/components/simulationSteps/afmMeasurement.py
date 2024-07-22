import sys, os

import logging

from . import simulationStepBase

class afmMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Performs measurements for Atomic Force Microscopy (AFM) simulations, recording force-distance data.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for AFM measurements.",
                "type": "str",
                "default": "afm_measurement.dat"
            }
        },
        "example": "
        {
            \"type\": \"afmMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"afm_data.dat\"
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath"}
    requiredParameters  = {"outputFilePath"}
    availableSelections = set()
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
              "type":["ExperimentMeasures","AFMMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



