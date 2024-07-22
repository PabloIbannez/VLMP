import sys, os

import logging

from . import simulationStepBase

class pairwiseForces(simulationStepBase):
    """
    {
        "author": "Pablo Palacios-Alonso",
        "description": "Measures pairwise forces between particles in the simulation.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file where pairwise forces will be written.",
                "type": "str",
                "default": null
            }
        },
        "selections": {},
        "example": "
        {
            \"type\": \"pairwiseForces\",
            \"parameters\": {
                \"outputFilePath\": \"pairwise_forces.dat\"
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
        parameters["mode"]           = "Pairwise_force"

        simulationStep = {
            name:{
                "type":["MechanicalMeasure","PairwiseForceMeasure"],
                "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



