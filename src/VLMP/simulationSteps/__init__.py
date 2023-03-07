import os
import copy

################ SIMULATION STEP INTERFACE ################

import abc
from UAMMD.simulation import simulation

class simulationStepBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 availableParameters:set,
                 compulsoryParameters:set,
                 **kwargs):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.units  = units

        self.availableParameters  = availableParameters.copy()
        self.compulsoryParameters = compulsoryParameters.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.error(f"[SimulationStep] ({self._type}) Parameter {key} not available for simulation step {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[SimulationStep] ({self._type}) Compulsory parameter {key} not given for simulation step {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[SimulationStep] ({self._type}) Using simulation step {self._name}")

        ########################################################

        self.simulationStep = None

    def getSimulationStep(self):
        if self.simulationStep == None:
            self.logger.error(f"[SimulationStep] ({self._type}) Simulation step not set")
            raise ValueError(f"Simulation step not set")

        return self.simulationStep

    def getSimulation(self,DEBUG_MODE = False):

        sim = {}

        sim["simulationStep"] = {}
        sim["simulationStep"] = self.getSimulationStep()

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (NotImplemented)

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
simulationSteps = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
simulationSteps = [ m.split("/")[-1].split(".")[0] for m in simulationSteps ]

for o in simulationSteps:
    exec(f"from .{o} import *")
