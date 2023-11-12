import sys, os

import logging

from . import simulationStepBase

class thermodynamicIntegration(simulationStepBase):
    """
    Component name: thermodynamicIntegration
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 06/11/2023

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath",
                                                "stepLambda","lambdaIntervalLength",
                                                "initLambda","finalLambda"},
                         requiredParameters  = {"outputFilePath",
                                                "stepLambda","lambdaIntervalLength"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params["outputFilePath"]

        parameters["stepLambda"]           = params["stepLambda"]
        parameters["lambdaIntervalLength"] = params["lambdaIntervalLength"]

        parameters["initLambda"]  = params.get("initLambda",1.0)
        parameters["finalLambda"] = params.get("finalLambda",0.0)

        simulationStep = {
            name:{
              "type":["ThermodynamicMeasure","ThermodynamicIntegration"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



