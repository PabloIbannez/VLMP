import os
import copy

################ SYSTEM INTERFACE ################

import abc
from UAMMD.simulation import simulation

class systemBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 availableParameters:set,
                 compulsoryParameters:set,
                 **kwargs):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.availableParameters  = availableParameters.copy()
        self.compulsoryParameters = compulsoryParameters.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.error(f"[System] ({self._type}) Parameter {key} not available for system {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[System] ({self._type}) Compulsory parameter {key} not given for system {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[System] ({self._type}) Using system {self._name}")

        ########################################################

        self.system = None

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    def getSimulation(self,DEBUG_MODE = False):
        if self.system is None:
            self.logger.error(f"[System] ({self._type}) System {self._name} not initialized")
            raise ValueError(f"System not initialized")

        return simulation({"system":{"parameters":copy.deepcopy(self.system)}},DEBUG_MODE)

############### IMPORT ALL SYSTEMS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
systems = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
systems = [ u.split("/")[-1].split(".")[0] for u in systems ]

for s in systems:
    exec(f"from .{s} import *")
