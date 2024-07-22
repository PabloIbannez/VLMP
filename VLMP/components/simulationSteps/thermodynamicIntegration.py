import sys, os

import logging

from . import simulationStepBase

class thermodynamicIntegration(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Performs thermodynamic integration to calculate free energy differences.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for thermodynamic integration results.",
                "type": "str",
                "default": null
            },
            "stepLambda": {
                "description": "Step size for lambda parameter in the integration.",
                "type": "float",
                "default": null
            },
            "lambdaValues": {
                "description": "List of lambda values for the integration.",
                "type": "list of float",
                "default": null
            }
        },
        "selections": {},
        "example": "
        {
            \"type\": \"thermodynamicIntegration\",
            \"parameters\": {
                \"outputFilePath\": \"ti_results.dat\",
                \"stepLambda\": 0.1,
                \"lambdaValues\": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath",
                           "stepLambda","lambdaValues"}
    requiredParameters  = {"outputFilePath",
                           "stepLambda","lambdaValues"}
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

        parameters["stepLambda"]     = params["stepLambda"]
        parameters["lambdaValues"]   = params["lambdaValues"]

        simulationStep = {
            name:{
              "type":["ThermodynamicMeasure","ThermodynamicIntegration"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



