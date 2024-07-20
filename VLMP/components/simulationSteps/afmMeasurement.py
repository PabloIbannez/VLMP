import sys, os

import logging

from . import simulationStepBase

class afmMeasurement(simulationStepBase):
    """
    Component name: afmMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    """

    availableParameters = {"outputFilePath"}
    requiredParameters  = {"outputFilePath"}
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

        simulationStep = {
            name:{
              "type":["ExperimentMeasures","AFMMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



