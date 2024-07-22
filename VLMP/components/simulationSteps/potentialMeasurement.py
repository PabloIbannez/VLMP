import sys, os

import logging

from . import simulationStepBase

class potentialMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures the potential of individual particles in the simulation.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for potential measurements.",
                "type": "str",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for potential measurement.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"potentialMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"particle_potentials.dat\",
                \"selection\": \"model1 type B\"
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath"}
    requiredParameters  = {"outputFilePath"}
    availableSelections = {"selection"}
    requiredSelections  = {"selection"}

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
              "type":["ParticlesListMeasure","PotentialMeasure"],
              "parameters":{**parameters},
              "labels":["id"],
              "data":[[i] for i in self.getSelection("selection")]
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



