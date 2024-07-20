import sys, os

import logging

from . import simulationStepBase

class meanMagnetizationMeasurement(simulationStepBase):
    """
    Component name: meanMagnetizationMeasurement
    Component type: simulationStep

    Author: P. Palacios Alonso
    Date: 18/10/2023

    This component writes the mean magnetization of the system to a file.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str

    """

    availableParameters = {"outputFilePath"}
    requiredParameters  = {"outputFilePath"}
    availableSelections = {"selection"}
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
              "type":["MagneticMeasure","MeasureMeanMagnetization"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



