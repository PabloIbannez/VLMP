import sys, os

import logging

from . import simulationStepBase

class forceBetweenSetsMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Palacios-Alonso",
        "description": "Measures the force between two sets of particles in the simulation.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for force measurements.",
                "type": "str",
                "default": "force_between_sets.dat"
            },
            "setName_idList": {
                "description": "Dictionary mapping set names to lists of particle IDs.",
                "type": "dict",
                "default": null
            }
        },
        "example": "
        {
            \"type\": \"forceBetweenSetsMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"force_data.dat\",
                \"setName_idList\": {\"set1\": [1, 2, 3], \"set2\": [4, 5, 6]}
            }
        }
        "
    }
    """

    availableParameters = {"setName_idList",
                           "outputFilePath"}
    requiredParameters  = {"setName_idList",
                           "outputFilePath"}

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

        data = []
        setName_idList = params["setName_idList"]

        for setName in setName_idList.keys():
            data += [[setName, setName_idList[setName]]]


        simulationStep = {
            name:{
                "type":["MechanicalMeasure","ForceBetweenSetsMeasure"],
                "parameters":{**parameters},
                "labels":["name", "id_list"],
                "data":data.copy()
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



