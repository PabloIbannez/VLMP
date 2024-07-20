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

    availableParameters = {"outputFilePath",
                           "stepLambda","lambdaValues"}
    requiredParameters  = {"outputFilePath",
                           "stepLambda","lambdaValues"}
    availableSelections = set()
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



