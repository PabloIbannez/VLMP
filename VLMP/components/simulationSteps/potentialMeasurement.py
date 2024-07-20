import sys, os

import logging

from . import simulationStepBase

class potentialMeasurement(simulationStepBase):
    """
    Component name: potentialMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 09/04/2023

    """

    availableParameters = {"outputFilePath"}
    requiredParameters  = {"outputFilePath"}
    availableSelections = {"selection"}
    requiredSelections  = {"selection"}

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



