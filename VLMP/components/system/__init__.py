import os
import copy

import logging

################ SYSTEM INTERFACE ################

from pyUAMMD import simulation

class systemBase:

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
            self.logger.error(f"[System] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for system {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[System] ({self._type}) Parameter {par} not available for system {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[System] ({self._type}) Required parameter {par} not given for system {self._name}")
                raise Exception(f"Required parameter not given")

        self.logger.info(f"[System] ({self._type}) Using system {self._name}")

        ########################################################

        self._system = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setSystem(self,system):
        self._system = system

    def getSystem(self):
        if self._system is None:
            self.logger.error(f"[System] ({self._type}) System {self._name} not initialized")
            raise Exception(f"System not initialized")
        return self._system

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):
        return simulation({"system":copy.deepcopy(self.getSystem())},DEBUG_MODE)

############### IMPORT ALL SYSTEMS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
systems = [ module.rsplit(".")[1] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
systems = [ u.split("/")[-1].split(".")[0] for u in systems ]

for s in systems:
    try:
        exec(f"from .{s} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[System] Error importing system type component \"{s}\"")

