import sys, os

import logging

from . import simulationStepBase

class pairwiseForces(simulationStepBase):
    """
    Component name: pairwiseForces
    Component type: simulationStep

    Author: Pablo Palacios-Alonso
    Date: 11/03/2024

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
        parameters["mode"]           = "Pairwise_force"

        simulationStep = {
            name:{
                "type":["MechanicalMeasure","PairwiseForceMeasure"],
                "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



