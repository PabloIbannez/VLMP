import sys, os

import logging

from . import simulationStepBase

class nativeContactsMeasurement(simulationStepBase):
    """
    Component name: nativeContactsMeasurement
    Component type: simulationStep

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath"},
                         requiredParameters  = {"outputFilePath"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
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



