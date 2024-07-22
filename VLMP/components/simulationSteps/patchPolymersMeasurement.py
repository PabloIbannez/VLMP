import sys, os

import logging

from . import simulationStepBase

class patchPolymersMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures properties of polymers created by dynamic bonded patchy particles, including size and surface bonding.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for polymer measurements.",
                "type": "str",
                "default": null
            },
            "bufferSize": {
                "description": "Size of the buffer for measurements.",
                "type": "int",
                "default": null
            },
            "surfaceEnergyThreshold": {
                "description": "Energy threshold for determining surface bonding.",
                "type": "float",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of patchy particles to measure.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"patchPolymersMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"patch_polymers.dat\",
                \"bufferSize\": 1000,
                \"surfaceEnergyThreshold\": -1.0,
                \"selection\": \"model1 type patchy\"
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath","bufferSize","surfaceEnergyThreshold"}
    requiredParameters  = {"outputFilePath","bufferSize","surfaceEnergyThreshold"}
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

        #Check if intervalStep is different from 1. If so, raise an error
        if params.get("intervalStep") != 1:
            self.logger.error("[PatchPolymersMeasurement] intervalStep must be 1")
            raise Exception("Not valid intervalStep")

        parameters = {}

        parameters["outputFilePath"]         = params["outputFilePath"]
        parameters["bufferSize"]             = params["bufferSize"]
        parameters["surfaceEnergyThreshold"] = params["surfaceEnergyThreshold"]

        simulationStep = {
            name:{
              "type":["TopologicalMeasures","PatchPolymers"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



