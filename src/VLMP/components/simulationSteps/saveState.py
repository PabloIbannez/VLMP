import sys, os

import logging

from . import simulationStepBase

class saveState(simulationStepBase):
    """
    Component name: saveState
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    This component is used to save the state of the simulation.
    Availble formats are:
        - .coord
        - .sp
        - .xyz
        - .pdb
        - .itpv
        - .itpd
        - .dcd
        - .lammpstrj
        - .vel

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param outputFormat: Format of the output file
    :type outputFormat: str
    :param intervalStep: Interval of steps to save the state
    :type intervalStep: int
    :param startStep: Step to start saving the state
    :type startStep: int, optional
    :param endStep: Step to end saving the state
    :type endStep: int, optional

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath","outputFormat","intervalStep","startStep","endStep"},
                         requiredParameters  = {"outputFilePath","outputFormat","intervalStep"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params.get("outputFilePath")
        parameters["outputFormat"]   = params.get("outputFormat")
        parameters["intervalStep"]   = params.get("intervalStep")

        if "startStep" in params:
            parameters["startStep"] = params.get("startStep")
        if "endStep" in params:
            parameters["endStep"]   = params.get("endStep")

        simulationStep = {
            name:{
              "type":["WriteStep","WriteStep"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



