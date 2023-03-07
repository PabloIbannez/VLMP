import os
import copy

################ UNITS INTERFACE ################

import abc
from UAMMD.simulation import simulation

class unitsBase(metaclass=abc.ABCMeta):

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
                self.logger.error(f"[Units] ({self._type}) Parameter {key} not available for units {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[Units] ({self._type}) Compulsory parameter {key} not given for units {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[Units] ({self._type}) Using units {self._name}")

        ########################################################

        self.unitsUAMMD = None

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    def getSimulation(self,DEBUG_MODE = False):
        if self.unitsUAMMD is None:
            self.logger.error(f"[Units] Units key for UAMMD not set")
            raise ValueError(f"Units key for UAMMD not set")

        return simulation({"global":{"units":self.unitsUAMMD}},DEBUG_MODE)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fromInputToInternalTime') and
                callable(subclass.fromInputToInternalTime)   and
                NotImplemented)

    @abc.abstractmethod
    def fromInputToInternalTime(self, inputTime):
        """ Performs the conversion from the input time to the internal one """
        raise NotImplementedError

############### IMPORT ALL UNITS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
units = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
units = [ u.split("/")[-1].split(".")[0] for u in units ]

for u in units:
    exec(f"from .{u} import *")
