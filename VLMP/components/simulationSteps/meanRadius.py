import sys, os

import logging

from . import simulationStepBase

class meanRadius(simulationStepBase):
    """
    Component name: meanRadius
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 24/10/2023

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
              "type":["GeometricalMeasure","MeanRadius"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



