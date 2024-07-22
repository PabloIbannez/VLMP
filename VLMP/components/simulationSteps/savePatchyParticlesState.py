import sys, os

import logging

from . import simulationStepBase

class savePatchyParticlesState(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Saves the state of patchy particles, including their positions and patch orientations.",
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
                "description": "Selection of patchy particles to save.",
                "type": "list of ids"
            }
        },
        "example": "
        {
            \"type\": \"savePatchyParticlesState\",
            \"parameters\": {
                \"outputFilePath\": \"patchy_state.xyz\",
                \"outputFormat\": \"xyz\",
                \"pbc\": true,
                \"selection\": \"model1 type patchy\"
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

        parameters["outputFilePath"] = params.get("outputFilePath")
        parameters["outputFormat"]   = params.get("outputFormat")

        if "pbc" in params:
            parameters["pbc"] = params["pbc"]

        simulationStep = {
            name:{
              "type":["WriteStep","WritePatchyParticlesStep"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



