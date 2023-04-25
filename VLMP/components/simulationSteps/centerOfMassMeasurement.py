import sys, os

import logging

from . import simulationStepBase

class centerOfMassMeasurement(simulationStepBase):
    """
    Component name: centerOfMassMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 09/04/2023

    This component measures the center of mass of the particles in the simulation.

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
              "type":["GeometricalMeasure","CenterOfMassPosition"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



