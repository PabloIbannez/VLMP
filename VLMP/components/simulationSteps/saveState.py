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

    Avalible formats are:
        * .coord
        * .sp
        * .xyz
        * .pdb
        * .itpv
        * .itpd
        * .dcd
        * .lammpstrj
        * .vel

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param outputFormat: Format of the output file
    :type outputFormat: str

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath","outputFormat","pbc"},
                         requiredParameters  = {"outputFilePath","outputFormat",},
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params["outputFilePath"]
        parameters["outputFormat"]   = params["outputFormat"]

        if "pbc" in params:
            parameters["pbc"] = params["pbc"]

        simulationStep = {
            name:{
              "type":["WriteStep","WriteStep"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



