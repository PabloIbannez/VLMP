import sys, os

import logging

from . import simulationStepBase

class saveState(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Saves the current state of the simulation, including particle positions and velocities.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for saving the state.",
                "type": "str",
                "default": null
            },
            "outputFormat": {
                "description": "Format of the output file (e.g., 'xyz', 'pdb', 'dcd').",
                "type": "str",
                "default": null
            },
            "pbc": {
                "description": "Whether to apply periodic boundary conditions when saving.",
                "type": "bool",
                "default": false
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particles to save. If not specified, all particles are saved.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"saveState\",
            \"parameters\": {
                \"outputFilePath\": \"simulation_state.pdb\",
                \"outputFormat\": \"pdb\",
                \"pbc\": true,
                \"selection\": \"model1 all\"
            }
        }
        "
    }
    """

    availableParameters = {"outputFilePath","outputFormat","pbc"}
    requiredParameters  = {"outputFilePath","outputFormat"}
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
        parameters["outputFormat"]   = params["outputFormat"]

        if "pbc" in params:
            parameters["pbc"] = params["pbc"]

        simulationStep = {
            name:{
              "type":["WriteStep","WriteStep"],
              "parameters":{**parameters}
            }
        }

        self.setGroup("selection")

        ############################################################

        self.setSimulationStep(simulationStep)



