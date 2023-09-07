import sys, os

import logging

from . import simulationStepBase

class savePatchyParticlesState(simulationStepBase):
    """
    Component name: savePatchyParticlesState
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 25/04/2023

    This component is used to save the state of the simulation incliding the
    patchy particles.

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
                         requiredParameters  = {"outputFilePath","outputFormat"},
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params.get("outputFilePath")
        parameters["outputFormat"]   = params.get("outputFormat")

        if "pbc" in params:
            parameters["pbc"] = params["pbc"]

        simulationStep = {
            name:{
              "type":["WriteStep","WritePatchyParticlesStep"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



