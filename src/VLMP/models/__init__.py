import os
import copy

################ MODEL INTERFACE ################

import abc
from UAMMD.simulation import simulation

from ..utils import getLabelIndex

class modelBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 availableParameters:set,
                 compulsoryParameters:set,
                 availableSelectors:set,
                 **kwargs):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.units = units

        self.availableParameters  = availableParameters.copy()
        self.compulsoryParameters = compulsoryParameters.copy()
        self.availableSelectors   = availableSelectors.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.error(f"[Model] ({self._type}) Parameter {key} not available for model {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[Model] ({self._type}) Compulsory parameter {key} not given for model {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[Model] ({self._type}) Using model {self._name}")

        ########################################################

        self.types      = None
        self.state      = None
        self.structure  = None
        self.forceField = None

    def getName(self):
        return self._name

    def getTypes(self):
        if self.types is None:
            self.logger.error(f"[Model] ({self._type}) Types not set")
            raise ValueError(f"Types not set")
        return self.types

    def getState(self):
        if self.state is None:
            self.logger.error(f"[Model] ({self._type}) State not set")
            raise ValueError(f"State not set")
        return self.state

    def getStructure(self):
        if self.structure is None:
            self.logger.error(f"[Model] ({self._type}) Structure not set")
            raise ValueError(f"Structure not set")
        return self.structure

    def getForceField(self):
        if self.forceField is None:
            self.logger.error(f"[Model] ({self._type}) Force field not set")
            raise ValueError(f"Force field not set")
        return self.forceField

    def getIds(self):
        ids = []
        idIndex = getLabelIndex("id",self.getState()["labels"])
        for entry in self.getState()["data"]:
            ids.append(entry[idIndex])
        return ids

    def getSimulation(self,DEBUG_MODE = False):

        # Create simulation

        sim = {}

        sim["global"] = self.getTypes()
        sim["state"]  = self.getState()

        sim["topology"] = {}
        sim["topology"]["structure"]  = self.getStructure()
        sim["topology"]["forceField"] = self.getForceField()

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'processSelection') and
                callable(subclass.processSelection)   and
                NotImplemented)

    @abc.abstractmethod
    def processSelection(self,**kwargs):
        """ Return a index of the particles that are selected """
        raise NotImplementedError

    def getSelection(self,**kwargs):
        # If no selection is given, select all particles
        if len(kwargs) == 0:
            return self.getIds()
        # Check if all selectors given by kwargs are available
        for key in kwargs:
            if key not in self.availableSelectors:
                self.logger.error(f"[Model] ({self._type}) Selector {key} not available for model {self._name}")
                raise ValueError(f"Selector not available")
        return self.selection(**kwargs)

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
models = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
models = [ m.split("/")[-1].split(".")[0] for m in models]

for m in models:
    exec(f"from .{m} import *")
