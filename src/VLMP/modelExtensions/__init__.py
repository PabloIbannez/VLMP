import os
import copy

################ MODEL INTERFACE ################

import abc
from UAMMD.simulation import simulation

class modelExtensionBase(metaclass=abc.ABCMeta):

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
        self.logger.debug(f"[ModelExtension] ({self._type}) Extending models: "+
                          " ".join([m.getName() for m in self.models])+
                          ". For model extension: "+self._name)

        self.availableParameters  = availableParameters.copy()
        self.compulsoryParameters = compulsoryParameters.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.error(f"[ModelExtension] ({self._type}) Parameter {key} not available for model extension {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[ModelExtension] ({self._type}) Compulsory parameter {key} not given for model extension {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[ModelExtension] ({self._type}) Using model extension {self._name}")

        ########################################################

        self.extension = None

    def getExtension(self):
        if self.extension is None:
            self.logger.error(f"[ModelExtension] ({self._type}) Extension not set")
            raise ValueError(f"Extension not set")
        return self.extension

    def getSimulation(self,DEBUG_MODE = False):

        sim = {}

        sim["topology"] = {}
        sim["topology"]["forceField"] = self.getExtension()

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (NotImplemented)

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
extensions = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
extensions = [ m.split("/")[-1].split(".")[0] for m in extensions ]

for o in extensions:
    exec(f"from .{o} import *")
