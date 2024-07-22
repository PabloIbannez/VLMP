import sys, os

import logging

from . import simulationStepBase

class thermodynamicMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures various thermodynamic properties of the system, including energy, temperature, and pressure.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for thermodynamic measurements.",
                "type": "str",
                "default": null
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles for thermodynamic measurements. If not specified, all particles are included.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"thermodynamicMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"thermo.dat\",
                \"selection\": \"model1 all\"
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
              "type":["ThermodynamicMeasure","ThermodynamicQuantityMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



