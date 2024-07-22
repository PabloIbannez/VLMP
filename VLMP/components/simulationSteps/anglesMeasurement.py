import sys, os

import logging

from . import simulationStepBase

class anglesMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures angles between specified triplets of particles in the simulation.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for angle measurements.",
                "type": "str",
                "default": "angles.dat"
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particle triplets for angle measurement.",
                "type": "list of triplets"
            }
        },
        "example": "
        {
            \"type\": \"anglesMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"angle_data.dat\",
                \"selection\": \"model1 forceField ANGLES\"
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

        parameters["outputFilePath"] = params["outputFilePath"]

        selIds = self.getSelection("selection")

        #Check if selIds is a list of list of size 3
        if isinstance(selIds,list):
            for selId in selIds:
                if isinstance(selId,list):
                    if len(selId) != 3:
                        self.logger.error("[anglesMeasurement] selection must be a list of list of size 3")
                        raise Exception("Selection error")
                else:
                    self.logger.error("[anglesMeasurement] selection must be a list of list of size 3")
                    raise Exception("Selection error")
        else:
            self.logger.error("[anglesMeasurement] selection must be a list of list of size 3")
            raise Exception("Selection error")

        simulationStep = {
            name:{
              "type":["ParticlesListMeasure","AnglesMeasure"],
              "parameters":{**parameters},
              "labels":["id_i","id_j","id_k"],
              "data":selIds.copy()
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



