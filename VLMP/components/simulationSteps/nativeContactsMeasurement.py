import sys, os

import logging

from . import simulationStepBase

class nativeContactsMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Measures the native contacts between selected pairs of particles, typically used in protein folding simulations.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for native contacts measurements.",
                "type": "str",
                "default": "native_contacts.dat"
            }
        },
        "selections": {
            "selection": {
                "description": "Selection of particle pairs for native contacts measurement.",
                "type": "list of pairs"
            }
        },
        "example": "
        {
            \"type\": \"nativeContactsMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"contacts_data.dat\",
                \"selection\": \"model1 contacts 1:5 6:10 11:15\"
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
        data = []
        for i,j in selIds:
            data.append([i,j])

        simulationStep = {
            name:{
              "type":["ParticlesListMeasure","ContactsMeasure"],
              "parameters":{**parameters},
              "labels":["id_i","id_j"],
              "data":data.copy()
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



