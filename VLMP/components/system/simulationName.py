import sys, os

import logging

from . import systemBase

class simulationName(systemBase):
    """
    Component name: simulationName
    Component type: system

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    Simple component to add a name to the simulation.

    :param simulationName: Name of the simulation
    :type simulationName: str
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"simulationName"},
                         requiredParameters  = {"simulationName"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        system = {
            name:{"type":["Simulation","Information"],
                  "parameters":{}}
        }

        system[name]["parameters"]["name"] = params.get("simulationName")

        ############################################################

        self.setSystem(system)

