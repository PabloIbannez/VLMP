import os
import copy

import logging

################ MODEL INTERFACE ################

import abc
from UAMMD.simulation import simulation

from ...utils import getLabelIndex

class modelBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 availableParameters:set,
                 requiredParameters:set,
                 availableSelectors:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.units = units

        self.availableParameters = availableParameters.copy()
        self.requiredParameters  = requiredParameters.copy()
        self.availableSelectors  = availableSelectors.copy()

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Model] ({self._type}) Parameter {par} not available for model {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Model] ({self._type}) Required parameter {par} not given for model {self._name}")
                raise ValueError(f"Required parameter not given")

        self.logger.info(f"[Model] ({self._type}) Using model {self._name}")

        ########################################################

        self._idOffset   = None

        ########################################################

        self._types      = None
        self._state      = None
        self._structure  = None
        self._forceField = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setTypes(self,types):
        self._types = types

    def setState(self,state):
        self._state = state

    def setStructure(self,structure):
        self._structure = structure

    def setForceField(self,forceField):
        self._forceField = forceField

    def getTypes(self):
        if self._types is None:
            self.logger.error(f"[Model] ({self._type}) Types not set")
            raise ValueError(f"Types not set")
        return self._types

    def getState(self):
        if self._state is None:
            self.logger.error(f"[Model] ({self._type}) State not set")
            raise ValueError(f"State not set")
        return self._state

    def getStructure(self):
        if self._structure is None:
            self.logger.error(f"[Model] ({self._type}) Structure not set")
            raise ValueError(f"Structure not set")
        return self._structure

    def getForceField(self):
        if self._forceField is None:
            self.logger.error(f"[Model] ({self._type}) Force field not set")
            raise ValueError(f"Force field not set")
        return self._forceField

    ########################################################

    def getUnits(self):
        return self._units

    ########################################################

    def getNumberOfParticles(self):
        if self._state is None:
            return 0
        return len(self.getState()["data"])

    def getIds(self):
        ids = []
        idIndex = getLabelIndex("id",self.getState()["labels"])
        for entry in self.getState()["data"]:
            ids.append(entry[idIndex])
        return ids

    def setIdOffset(self,offset):
        self._idOffset = offset

    def getIdOffset(self):
        if self._idOffset is None:
            self.logger.error(f"[Model] ({self._type}) Id offset not set")
            raise ValueError(f"Id offset not set")
        return self._idOffset

    ########################################################

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
    def processSelection(self,**params):
        """ Return a index of the particles that are selected """
        raise NotImplementedError

    def getSelection(self,**params):
        # If no selection is given, select all particles
        if len(params) == 0:
            return self.getIds()
        if len(params) == 1:
            if params.pars()[0] == "all":
                return self.getIds()
        # Check if all selectors given by params are available
        for par in params:
            if par not in self.availableSelectors:
                self.logger.error(f"[Model] ({self._type}) Selector {par} not available for model {self._name}")
                raise ValueError(f"Selector not available")
        return self.processSelection(**params)

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
models = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
models = [ m.split("/")[-1].split(".")[0] for m in models]

for m in models:
    try:
        exec(f"from .{m} import *")
    except:
        logging.getLogger("VLMP").error(f"[Model] Error importing model type component {m}")
        raise ImportError(f"Error importing model type component")

