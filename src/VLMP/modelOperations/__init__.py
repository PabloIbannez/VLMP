import os
import copy

################ MODEL INTERFACE ################

import abc
from UAMMD.simulation import simulation

class modelOperationBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 models,
                 availableParameters:set,
                 compulsoryParameters:set,
                 **kwargs):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.units  = units
        self.models = models
        self.logger.debug(f"[ModelOperation] ({self._type}) Operating on models: "+
                          " ".join([m.getName() for m in self.models])+
                          ". For model operation: "+self._name)

        self.availableParameters  = availableParameters.copy()
        self.compulsoryParameters = compulsoryParameters.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.error(f"[ModelOperation] ({self._type}) Parameter {key} not available for model operation {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[ModelOperation] ({self._type}) Compulsory parameter {key} not given for model operation {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[ModelOperation] ({self._type}) Using model operation {self._name}")

        ########################################################

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'apply') and
                callable(subclass.apply)   and
                NotImplemented)

    @abc.abstractmethod
    def apply(self):
        """Apply the model operation to the model"""
        raise NotImplementedError

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
operations = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
operations = [ m.split("/")[-1].split(".")[0] for m in operations ]

for o in operations:
    exec(f"from .{o} import *")
