import os

################ MODEL INTERFACE ################

import abc
from UAMMD.simulation import simulation

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

        self.ids        = None
        self.positions  = None
        self.velocities = None
        self.directions = None

    def getIds(self):
        return self.ids

    def getPositions(self):
        return self.positions

    def getVelocities(self):
        return self.velocities

    def getDirections(self):
        return self.directions

    def getTopology(self):
        return self.topology

    def getSimulation(self):
        if self.ids is None and \
           self.positions is None and \
           self.velocities is None and \
           self.directions is None:
            return simulation({"topology":self.topology})
        else:
            coordinates = {}
            coordinates["labels"] = []
            coordinates["data"]   = []

            coordinates["labels"].append("id")
            if self.ids is not None:
                for id_ in self.ids:
                    coordinates["data"].append([int(id_)])
            else:
                #If no ids are given, use the index of the particle as id

                if self.positions is not None:
                    for i in range(len(self.positions)):
                        coordinates["data"].append([i])
                elif self.velocities is not None:
                    for i in range(len(self.velocities)):
                        coordinates["data"].append([i])
                elif self.directions is not None:
                    for i in range(len(self.directions)):
                        coordinates["data"].append([i])

            if self.positions is not None:
                coordinates["labels"].append("position")
                for i,pos in enumerate(self.positions):
                    x,y,z = pos
                    coordinates["data"][i].append([float(x),float(y),float(z)])

            if self.velocities is not None:
                coordinates["labels"].append("velocity")
                for i,vel in enumerate(self.velocities):
                    x,y,z = vel
                    coordinates["data"][i].append([float(x),float(y),float(z)])

            if self.directions is not None:
                coordinates["labels"].append("direction")
                for i,dir_ in enumerate(self.directions):
                    x,y,z,w = dir_
                    coordinates["data"][i].append([float(x),float(y),float(z),float(w)])

            return simulation({"coordinates":coordinates,"topology":self.topology})

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
