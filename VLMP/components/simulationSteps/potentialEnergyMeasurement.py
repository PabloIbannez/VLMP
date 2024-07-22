import sys, os

import logging

from . import simulationStepBase

class potentialEnergyMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures the potential energy of selected particles or the entire system.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for potential energy measurements.",
                "type": "str",
                "default": null
            },
            "potentials": {
                "description": "List of potential types to measure. If not specified, all potentials are measured.",
                "type": "list of str",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for potential energy measurement.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"potentialEnergyMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"potential_energy.dat\",
                \"potentials\": [\"LennardJones\", \"Coulomb\"],
                \"selection\": \"model1 type A\"
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath","potentials"}
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

        parameters["outputFilePath"]  = params["outputFilePath"]

        if "potentials" in params:
            parameters["interactorsList"] = params["potentials"]

        simulationStep = {
            name:{
              "type":["ThermodynamicMeasure","InteractorsListEnergyMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



