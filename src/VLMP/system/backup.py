import sys, os

import logging

from . import systemBase

class backup(systemBase):

    """
    Simulation backup
    """

    def __init__(self,name,**kwargs):
        super().__init__(_type="backup",
                         _name= name,
                         availableParameters  = ["backupIntervalStep","backupStartStep","backupEndStep"],
                         compulsoryParameters = ["backupIntervalStep"],
                         **kwargs)

        ############################################################
        ####################  Backup Parameters  ###################
        ############################################################

        self.system = {}
        self.system["saveBackup"] = True

        self.system["backupIntervalStep"] = kwargs.get("backupIntervalStep")

        if "backupStartStep" in kwargs:
            self.system["backupStartStep"] = kwargs.get("backupStartStep")
        if "backupEndStep" in kwargs:
            self.system["backupEndStep"] = kwargs.get("backupEndStep")





