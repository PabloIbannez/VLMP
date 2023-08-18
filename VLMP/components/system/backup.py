import sys, os

import logging

from . import systemBase

class backup(systemBase):
    """
    Component name: backup
    Component type: system

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    Component used to add a backup system to the simulation.
    When this component is added to the simulation, the simulation will
    create a backup of the simulation every backupIntervalStep steps.
    The simulation will try to restore the simulation from the backup
    if the simulation crashes.

    :param backupIntervalStep: Interval of steps between backups
    :type backupIntervalStep: int
    :param backupFilePath: Path to the backup file, defaults to "backup"
    :type simulationName: str, optional
    :param backupStartStep: Step at which the backup starts
    :type backupStartStep: int, optional
    :param backupEndStep: Step at which the backup ends
    :type backupEndStep: int, optional
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters  = {"backupIntervalStep",
                                                 "backupStartStep","backupEndStep",
                                                 "backupFilePath"},
                         requiredParameters = {"backupIntervalStep"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        system = {
            name:{"type":["Simulation","Backup"],
                  "parameters":{}}
        }

        system[name]["parameters"]["backupIntervalStep"] = params.get("backupIntervalStep")
        system[name]["parameters"]["backupFilePath"]     = params.get("backupFilePath","backup")

        if "backupStartStep" in params:
            system[name]["parameters"]["backupStartStep"] = params.get("backupStartStep")
        if "backupEndStep" in params:
            system[name]["backupEndStep"] = params.get("backupEndStep")

        ############################################################

        self.setSystem(system)







