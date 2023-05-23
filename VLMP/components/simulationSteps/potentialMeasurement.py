import sys, os

import logging

from . import simulationStepBase

class potentialMeasurement(simulationStepBase):
    """
    Component name: potentialMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 09/04/2023

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param particleNumberAverage: Number of particles to average the height
    :type particleNumberAverage: int

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath"},
                         requiredParameters  = {"outputFilePath"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params.get("outputFilePath")

        simulationStep = {
            name:{
              "type":["ParticlesListMeasure","PotentialMeasure"],
              "parameters":{**parameters},
              "labels":["id"],
              "data":[[i] for i in self.getSelection("selection")]
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



