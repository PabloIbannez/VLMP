import os
import copy

################ UNITS INTERFACE ################

import abc
from UAMMD.simulation import simulation

class unitsBase(metaclass=abc.ABCMeta):

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

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Units] ({self._type}) Parameter {par} not available for units {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Units] ({self._type}) Required parameter {par} not given for units {self._name}")
                raise ValueError(f"Required parameter not given")

        self.logger.info(f"[Units] ({self._type}) Using units {self._name}")

        ########################################################

        self._unitsUAMMD = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setUnits(self, unitsUAMMD):
        self._unitsUAMMD = unitsUAMMD

    def getUnits(self):
        if self._unitsUAMMD is None:
            self.logger.error(f"[Units] ({self._type}) Units not set for units {self._name}")
            raise ValueError(f"Units not set")
        return self._unitsUAMMD

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):
        return simulation({"global":{"parameters":copy.deepcopy({"units":self.getUnits()})}},DEBUG_MODE)

    ########################################################

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getConstant') and
                callable(subclass.getConstant)   and
                NotImplemented)

    @abc.abstractmethod
    def getConstant(self, constantName):
        """ Get physical constant in units of this system """
        raise NotImplementedError

############### IMPORT ALL UNITS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
units = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
units = [ u.split("/")[-1].split(".")[0] for u in units ]

for u in units:
    try:
        exec(f"from .{u} import *")
    except:
        logging.getLogger("VLMP").error(f"[Units] Error importing units type component {u}")
