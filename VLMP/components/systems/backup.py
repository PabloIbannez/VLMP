import sys, os

import logging

from . import systemBase

class backup(systemBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     " Component used to add a backup system to the simulation.
       When this component is added to the simulation, the simulation will
       create a backup of the simulation every backupIntervalStep steps.
       The simulation will try to restore the simulation from the backup
       if the simulation crashes.",
     "parameters":{
        "backupIntervalStep":{"description":"Interval of steps between backups",
                              "type":"ullint"},
        "backupFilePath":{"description":"Path to the backup file",
                          "type":"str",
                          "default":"backup"},
        "backupStartStep":{"description":"Step at which the backup starts",
                           "type":"ullint",
                           "default":0},
        "backupEndStep":{"description":"Step at which the backup ends",
                          "type":"ullint",
                          "default":"MAX_ULLINT"}
            },
     "example":"
         {
            "type":"backup",
            "backupIntervalStep":1000,
            "backupFilePath":"backup"
         }
        "
    }
    """

    availableParameters  = {"backupIntervalStep",
                            "backupStartStep","backupEndStep",
                            "backupFilePath"}

    requiredParameters = {"backupIntervalStep"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
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







