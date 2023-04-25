import sys, os

import logging

from . import simulationStepBase

class heightMeasurement(simulationStepBase):
    """
    Component name: heightMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 09/04/2023

    This component measures the height of the particles selected.
    The height is the average of the N particles with the highest z coordinate.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param particleNumberAverage: Number of particles to average the height
    :type particleNumberAverage: int

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath","particleNumberAverage"},
                         requiredParameters  = {"outputFilePath"},
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params.get("outputFilePath")

        if "particleNumberAverage" in params:
            parameters["particleNumberAverage"] = params.get("particleNumberAverage")

        simulationStep = {
            name:{
              "type":["GeometricalMeasure","Height"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



