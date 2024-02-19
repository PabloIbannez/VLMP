import sys, os

import logging

from . import simulationStepBase

class forceBetweenSetsMeasurement(simulationStepBase):
    """
    Component name: forceBetweenSetsMeasurement
    Component type: simulationStep

    Author: Pablo Palacios-Alonso
    Date: 12/02/2024

    """


    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"setName_idList",
                                                "outputFilePath"},
                         requiredParameters  = {"setName_idList",
                                                "outputFilePath"},
                         availableSelections = set(),
                         requiredSelections  = set(),
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



