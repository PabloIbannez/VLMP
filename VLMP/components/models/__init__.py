import os
import copy

import logging

################ MODEL INTERFACE ################

import abc
from pyUAMMD import simulation

from ...utils.utils import getLabelIndex

class modelBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,types,
                 availableParameters:set,
                 requiredParameters:set,
                 definedSelections:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units = units
        self._types = types

        self.availableParameters = availableParameters.copy()
        self.requiredParameters  = requiredParameters.copy()
        self.definedSelections    = definedSelections.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[Model] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for model {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Model] ({self._type}) Parameter {par} not available for model {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Model] ({self._type}) Required parameter {par} not given for model {self._name}")
                raise Exception(f"Required parameter not given")

        self.logger.info(f"[Model] ({self._type}) Using model {self._name}")

        ########################################################

        self._idOffset   = None

        ########################################################

        self._state      = None
        self._structure  = None
        self._forceField = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setState(self,state):
        self._state = state

    def setStructure(self,structure):
        self._structure = structure

    def setForceField(self,forceField):
        self._forceField = forceField

    def getState(self):
        if self._state is None:
            self.logger.error(f"[Model] ({self._type}) State not set")
            raise Exception(f"State not set")
        return self._state

    def getStructure(self):
        if self._structure is None:
            self.logger.error(f"[Model] ({self._type}) Structure not set")
            raise Exception(f"Structure not set")
        return self._structure

    def getForceField(self):
        if self._forceField is None:
            self.logger.error(f"[Model] ({self._type}) Force field not set")
            raise Exception(f"Force field not set")
        return self._forceField

    ########################################################

    def getUnits(self):
        return self._units

    def getTypes(self):
        return self._types

    ########################################################

    def getNumberOfParticles(self):
        if self._state is None:
            return 0
        return len(self.getState()["data"])

    def getIds(self):
        if self._state is None:
            return []
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
            raise Exception(f"Id offset not set")
        return self._idOffset

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):

        # Create simulation

        sim = {}

        if self._state is not None:
            sim["state"]  = self.getState()

        sim["topology"] = {}
        if self._structure is not None:
            sim["topology"]["structure"]  = self.getStructure()
        if self._forceField is not None:
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
        # Check if all selectors given by params are available
        for par in params:
            if par not in self.definedSelections:
                self.logger.error(f"[Model] ({self._type}) Selector {par} not available for model {self._name}")
                raise Exception(f"Selector not available")
        return self.processSelection(**params)

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
models = [ module.rsplit(".")[1] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
models = [ m.split("/")[-1].split(".")[0] for m in models]

for m in models:
    try:
        exec(f"from .{m} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[Model] Error importing model type component {m}")
