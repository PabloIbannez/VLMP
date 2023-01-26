import os

################ MODEL INTERFACE ################

import abc

class modelBase(metaclass=abc.ABCMeta):

    def __init__(self,name:str,availableParameters:list,availableSelectors:list,**kwargs):
        self.logger = logging.getLogger("VLMP")

        self.name = name
        self.logger.info(f"[{self.name}] Using model \"{self.name}\"")

        self.availableParameters = availableParameters.copy()
        self.availableSelectors  = availableSelectors.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.warning(f"[{name}] Parameter \"{key}\" not available for model \"{name}\"")

    def getCoordinates(self):
        return self.coordinates

    def getTopology(self):
        return self.topology

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'write') and
                callable(subclass.write)   and
                hasattr(subclass, 'selection') and
                callable(subclass.selection)   and
                NotImplemented)

    @abc.abstractmethod
    def selection(self, **kwargs):
        """ Return a index of the particles that are selected """
        raise NotImplementedError

    def selection_safe(self,**kwargs):
        # Check if all selectors given by kwargs are available
        for key in kwargs:
            if key not in self.availableSelectors:
                self.logger.warning(f"[{self.name}] Selector \"{key}\" not available")
        return self.selection(**kwargs)

    @abc.abstractmethod
    def write(self, filePath: str):
        """Write model to file using json format"""
        raise NotImplementedError

############### IMPORT ALL MODELS ###############

import glob
models = [ module.split(".")[0] for module in glob.glob("*.py") if not "__" in module]

for model in models:
    import_str = f"from .{model} import *"
    exec(import_str)

print("MODELS")
