import sys, os

import logging

from . import simulationStepBase

class meanSquareDisplacement(simulationStepBase):
    """
    {
        "author": "Pablo Diez-Silva",
        "description": "Calculates the mean square displacement (MSD) of selected particles over time.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for MSD measurements.",
                "type": "str",
                "default": "msd.dat"
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for MSD calculation.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"meanSquareDisplacement\",
            \"parameters\": {
                \"outputFilePath\": \"msd_data.dat\",
                \"selection\": \"model1 type diffusive\"
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
              "type":["GeometricalMeasure","meanSquareDisplacement"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



