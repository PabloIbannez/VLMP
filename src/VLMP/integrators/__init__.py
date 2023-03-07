import os
import copy

################ INTEGRATORS INTERFACE ################

import abc
from UAMMD.simulation import simulation

class integratorBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 availableParameters:set,
                 compulsoryParameters:set,
                 **kwargs):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self.units = units

        self.availableParameters  = availableParameters.copy()
        self.compulsoryParameters = compulsoryParameters.copy()

        # Check if all parameters given by kwargs are available
        for key in kwargs:
            if key not in self.availableParameters:
                self.logger.error(f"[Integrator] ({self._type}) Parameter {key} not available for integrator {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all compulsory parameters are given
        for key in self.compulsoryParameters:
            if key not in kwargs:
                self.logger.error(f"[Integrator] ({self._type}) Compulsory parameter {key} not given for integrator {self._name}")
                raise ValueError(f"Compulsory parameter not given")

        self.logger.info(f"[Integrator] ({self._type}) Using integrator {self._name}")

        ########################################################

        self.integratorClass    = None
        self.integratorSubClass = None

        self.integratorParameters = None

        self.integrationSteps = None

    def getIntegrationSteps(self):
        if self.integrationSteps is None:
            self.logger.error(f"[Integrator] ({self._type}) Integration steps not set for integrator {self._name}")
            raise ValueError(f"Integration steps not set")
        return self.integrationSteps

    def getSimulation(self,DEBUG_MODE = False):
        if self.integratorClass is None:
            self.logger.error(f"[Integrator] ({self._type}) Integrator class not set for integrator {self._name}")
            raise ValueError(f"Integrator class not set")
        if self.integratorSubClass is None:
            self.logger.error(f"[Integrator] ({self._type}) Integrator subclass not set for integrator {self._name}")
            raise ValueError(f"Integrator subclass not set")
        if self.integratorParameters is None:
            self.logger.error(f"[Integrator] ({self._type}) Integrator parameters not set for integrator {self._name}")
            raise ValueError(f"Integrator parameters not set")
        if self.integrationSteps is None:
            self.logger.error(f"[Integrator] ({self._type}) Integration steps not set for integrator {self._name}")
            raise ValueError(f"Integration steps not set")

        sim = {}

        sim["integrator"] = {
        name:{
            "type":[self.integratorClass,self.integratorSubClass],
            "parameters":copy.deepcopy(self.integratorParameters)
        }}

        sim["integrator"]["schedule"] = {
            "type":["Schedule","Integrator"],
            "labels":["order","integrator","steps"],
            "data":[[1,name,self.getIntegrationSteps()]]}

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (NotImplemented)

############### IMPORT ALL INTEGRATORS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
integrators = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
integrators = [ m.split("/")[-1].split(".")[0] for m in integrators]

for i in integrators:
    exec(f"from .{i} import *")
