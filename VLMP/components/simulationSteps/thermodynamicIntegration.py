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
                                                "stepLambda","lambdaValues"},
                         requiredParameters  = {"outputFilePath",
                                                "stepLambda","lambdaValues"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params["outputFilePath"]

        parameters["stepLambda"]     = params["stepLambda"]
        parameters["lambdaValues"]   = params["lambdaValues"]

        simulationStep = {
            name:{
              "type":["ThermodynamicMeasure","ThermodynamicIntegration"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



