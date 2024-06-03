import sys, os

import logging

from VLMP.components.simulationSteps import simulationStepBase

class escapeTime(simulationStepBase):
    """
    Component name: escapeTime
    Component type: simulationStep

    Author: Pablo Diez-Silva
    Date: 20/05/2024

    This component measures the escape time of particles from the a system defined by a list of planes.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param normalVector: List of normal vectors of the planes
    :type normalVector: list of three-element list of float
    :param independentVector: List of independent vectors of the planes
    :type independentVector: list of three-element list of float
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath","normalVector","independentVector"},
                         requiredParameters  = {"outputFilePath","normalVector","independentVector"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params.get("outputFilePath")

        simulationStep = {
            name:{
              "type":["GeometricalMeasure","EscapeTime"],
              "parameters":{**parameters},
              "labels":["normalVector","independentVector"],
              "data":[]
            }
        }
        for i in range(len(params["normalVector"])):
            simulationStep[name]["data"].append([params["normalVector"][i],params["independentVector"][i]])

        ############################################################
        self.setSimulationStep(simulationStep)



