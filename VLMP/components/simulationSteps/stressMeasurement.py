import sys, os

import logging

from . import simulationStepBase

class stressMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures the stress tensor of the system.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for stress tensor measurements.",
                "type": "str",
                "default": null
            },
            "radiusCutOff": {
                "description": "Radius cutoff for the calculation of atom volumes.",
                "type": "float",
                "default": null
            }
        },
        "selections": {},
        "example": "
        {
            \"type\": \"stressMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"stress_tensor.dat\",
                \"radiusCutOff\": 2.5
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath","radiusCutOff"}
    requiredParameters  = {"outputFilePath","radiusCutOff"}
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
        parameters["radiusCutOff"]   = params["radiusCutOff"]

        simulationStep = {
            name:{
              "type":["MechanicalMeasure","StressMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



