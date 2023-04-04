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
                 requiredParameters:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units = units

        self.availableParameters = availableParameters.copy()
        self.availableParameters.update({"startStep","endStep"})

        self.requiredParameters  = requiredParameters.copy()

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[SimulationStep] ({self._type}) Parameter {par} not available for simulation step {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[SimulationStep] ({self._type}) Required parameter {par} not given for simulation step {self._name}")
                raise ValueError(f"Required parameter not given")

        self.logger.info(f"[SimulationStep] ({self._type}) Using simulation step {self._name}")

        ########################################################

        self._startStep = params.get("startStep",None)
        self._endStep   = params.get("endStep",None)

        ########################################################

        self._simulationStep = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setSimulationStep(self, simulationStep):
        self._simulationStep = simulationStep

    def getSimulationStep(self):
        if self._simulationStep is None:
            self.logger.error(f"[SimulationStep] ({self._type}) Simulation step {self._name} not initialized")
            raise ValueError(f"Simulation step not initialized")

        if self._startStep is not None:
            self._simulationStep[self.getName()]["parameters"]["startStep"] = self._startStep
        if self._endStep is not None:
            self._simulationStep[self.getName()]["parameters"]["endStep"]   = self._endStep

        return self._simulationStep

    ########################################################

    def getUnits(self):
        return self._units

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):
        return simulation({"simulationStep":copy.deepcopy(self.getSimulationStep())},DEBUG_MODE)

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
simulationSteps = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
simulationSteps = [ m.split("/")[-1].split(".")[0] for m in simulationSteps ]

for s in simulationSteps:
    try:
        exec(f"from .{s} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[SimulationStep] Error importing simulationStep type {s}")
