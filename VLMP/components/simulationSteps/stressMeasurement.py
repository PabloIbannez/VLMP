import sys, os

import logging

from . import simulationStepBase

class stressMeasurement(simulationStepBase):
    """
    Component name: stressMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 29/09/2020

    This component writes the stress tensor of the system to a file.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param radiusCutOff: Radius cutoff for the calculation of atom volumes
    :type radiusCutOff: float

    """

    availableParameters = {"outputFilePath","radiusCutOff"}
    requiredParameters  = {"outputFilePath","radiusCutOff"}
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
        parameters["radiusCutOff"]   = params["radiusCutOff"]

        simulationStep = {
            name:{
              "type":["MechanicalMeasure","StressMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



