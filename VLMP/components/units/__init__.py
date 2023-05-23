import os
import copy

import logging

################ UNITS INTERFACE ################

from pyUAMMD import simulation

class unitsBase:

    def __init__(self,
                 _type:str,_name:str,
                 availableParameters:set,
                 requiredParameters:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.availableParameters = availableParameters.copy()
        self.requiredParameters  = requiredParameters.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[Units] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for units {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Units] ({self._type}) Parameter {par} not available for units {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Units] ({self._type}) Required parameter {par} not given for units {self._name}")
                raise Exception(f"Required parameter not given")

        self.logger.info(f"[Units] ({self._type}) Using units {self._name}")

        ########################################################

        self._unitsUAMMD = None
        self._constants  = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setUnitsName(self, unitsUAMMD):
        self._unitsUAMMD = unitsUAMMD

    def getUnitsName(self):
        if self._unitsUAMMD is None:
            self.logger.error(f"[Units] ({self._type}) Units not set for units {self._name}")
            raise Exception(f"Units not set")
        return self._unitsUAMMD

    def addConstant(self, constName, constValue):
        if self._constants is None:
            self._constants = {}
        if constName in self._constants.keys():
            self.logger.warning(f"[Units] ({self._type}) Constant {constName} already add for units {self._name}")
        self._constants[constName] = constValue

    def getConstant(self, constName):
        if self._constants is None:
            self.logger.error(f"[Units] ({self._type}) No constants added for units {self._name}")
            raise Exception(f"No constants added")
        if constName not in self._constants.keys():
            self.logger.error(f"[Units] ({self._type}) Constant {constName} not added for units {self._name}")
            raise Exception(f"Constant not added")
        return self._constants[constName]

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):
        return simulation({"global":{"units":{"type":["Units",self.getUnitsName()]}}},DEBUG_MODE)

############### IMPORT ALL UNITS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
units = [ module.rsplit(".")[1] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
units = [ u.split("/")[-1].split(".")[0] for u in units ]

for u in units:
    try:
        exec(f"from .{u} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[Units] Error importing units type component {u}")
