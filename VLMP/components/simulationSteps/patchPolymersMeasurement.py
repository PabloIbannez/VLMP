import sys, os

import logging

from . import simulationStepBase

class patchPolymersMeasurement(simulationStepBase):
    """
    Component name: patchPolymers
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 7/05/2023

    This step is used to measure properties of the
    polymers created by dynamic bonded patchy particles.
    It computes size of the polymers and if they are
    bonded to the surface or not.

    :param startStep: First step to apply the simulationStep
    :type startStep: int, optional
    :param endStep: Last step to apply the simulationStep
    :type endStep: int, optional

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath","bufferSize","surfaceEnergyThreshold"},
                         requiredParameters  = {"outputFilePath","bufferSize","surfaceEnergyThreshold"},
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        #Check if intervalStep is different from 1. If so, raise an error
        if params.get("intervalStep") != 1:
            self.logger.error("[PatchPolymersMeasurement] intervalStep must be 1")
            raise Exception("Not valid intervalStep")

        parameters = {}

        parameters["outputFilePath"]         = params["outputFilePath"]
        parameters["bufferSize"]             = params["bufferSize"]
        parameters["surfaceEnergyThreshold"] = params["surfaceEnergyThreshold"]

        simulationStep = {
            name:{
              "type":["TopologicalMeasures","PatchPolymers"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



