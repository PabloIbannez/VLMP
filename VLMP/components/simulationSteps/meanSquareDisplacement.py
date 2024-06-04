import sys, os

import logging

from . import simulationStepBase

class meanSquareDisplacement(simulationStepBase):
    """
    Component name: meanSquareDisplacement
    Component type: simulationStep

    Author: Pablo Diez-Silva
    Date: 04/06/2024

    This component measures the mean square displacement of the particles in the simulation.
    The mean square displacement is calculated as the average of the square of the distance between the particles and their initial position.

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
              "type":["GeometricalMeasure","meanSquareDisplacement"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



