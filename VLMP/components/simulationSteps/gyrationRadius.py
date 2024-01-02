import sys, os

import logging

from . import simulationStepBase

class gyrationRadius(simulationStepBase):
    """
    Component name: gyrationRadius
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 30/11/2023

    :param outputFilePath: Path to the output file
    :type outputFilePath: str

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath"},
                         requiredParameters  = {"outputFilePath"},
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params.get("outputFilePath")

        simulationStep = {
            name:{
              "type":["GeometricalMeasure","GyrationRadius"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



