import sys, os

import logging

from . import simulationStepBase

class thermodynamicMeasurement(simulationStepBase):
    """
    Component name: thermodynamicMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    This component performs a thermodynamic measurement of the system.
    It measures the particle number, volume,
    energy (per interaction), kinetic energy, total potential energy, total energy,
    temperature, and virial.

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
              "type":["ThermodynamicMeasure","ThermodynamicQuantityMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setGroup("selection")
        self.setSimulationStep(simulationStep)



