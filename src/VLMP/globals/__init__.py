import os
import copy

################ GLOBALS INTERFACE ################

import abc
from UAMMD.simulation import simulation

class globalBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 availableParameters:set,
                 compulsoryParameters:set,
                 **kwargs):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.units = units

        self.availableParameters  = availableParameters.copy()
        self.compulsoryParameters = compulsoryParameters.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.error(f"[Global] ({self._type}) Parameter {key} not available for global {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[Global] ({self._type}) Compulsory parameter {key} not given for global {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[Global] ({self._type}) Using global {self._name}")

        ########################################################

        self.globals = None

    def getSimulation(self,DEBUG_MODE = False):
        if self.globals is None:
            self.logger.error(f"[Global] ({self._type}) Global {self._name} not initialized")
            raise ValueError(f"Global not initialized")
        return simulation({"global":{"parameters":copy.deepcopy(self.globals)}},DEBUG_MODE)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (NotImplemented)

############### IMPORT ALL GLOBALS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
globals_ = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
globals_ = [ m.split("/")[-1].split(".")[0] for m in globals_]

for g in globals_:
    exec(f"from .{g} import *")
