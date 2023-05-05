import os
import copy

import logging

################ GLOBALS INTERFACE ################

from pyUAMMD import simulation

class globalBase:

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 types,
                 availableParameters:set,
                 requiredParameters:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units = units
        self._types = types

        self.availableParameters = availableParameters.copy()
        self.requiredParameters  = requiredParameters.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[Global] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for global {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Global] ({self._type}) Parameter {par} not available for global {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Global] ({self._type}) Required parameter {par} not given for global {self._name}")
                raise Exception(f"Required parameter not given")

        self.logger.info(f"[Global] ({self._type}) Using global {self._name}")

        ########################################################

        self._globals = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setGlobals(self, _globals):
        self._globals = _globals

    def getGlobals(self):
        if self._globals is None:
            self.logger.error(f"[Global] ({self._type}) Global {self._name} not initialized")
            raise Exception(f"Global not initialized")
        return self._globals

    ########################################################

    def getUnits(self):
        return self._units

    def getTypes(self):
        return self._types

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):
        return simulation({"global":copy.deepcopy(self.getGlobals())},DEBUG_MODE)

############### IMPORT ALL GLOBALS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
globals_ = [ module.rsplit(".")[1] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
globals_ = [ m.split("/")[-1].split(".")[0] for m in globals_]

for g in globals_:
    try:
        exec(f"from .{g} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[Global] Error importing global type component \"{g}\"")
