import os
import copy

import logging

################ INTEGRATORS INTERFACE ################

from pyUAMMD import simulation

class integratorBase:

    def __init__(self,
                 _type:str,_name:str,
                 units,types,ensemble,models,
                 availableParameters:set,
                 requiredParameters:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units    = units
        self._types    = types
        self._ensemble = ensemble
        self._models   = models

        self.availableParameters  = availableParameters.copy()
        self.requiredParameters = requiredParameters.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[Integrator] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for integrator {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Integrator] ({self._type}) Parameter {par} not available for integrator {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Integrator] ({self._type}) Required parameter {par} not given for integrator {self._name}")
                raise Exception(f"Required parameter not given")

        self.logger.info(f"[Integrator] ({self._type}) Using integrator {self._name}")

        ########################################################

        self._integrator       = None
        self._integrationSteps = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def getUnits(self):
        return self._units

    def getTypes(self):
        return self._types

    def getEnsemble(self):
        return self._ensemble

    ########################################################

    def setIntegrator(self, integrator):
        self._integrator = integrator

    def setIntegrationSteps(self, integrationSteps):
        self._integrationSteps = integrationSteps

    def getIntegrator(self):
        if self._integrator is None:
            self.logger.error(f"[Integrator] ({self._type}) Integrator not initialized")
            raise Exception(f"Integrator not initialized")
        return self._integrator

    def getIntegrationSteps(self):
        if self._integrationSteps is None:
            self.logger.error(f"[Integrator] ({self._type}) Integration steps not initialized")
            raise Exception(f"Integration steps not initialized")
        return self._integrationSteps

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):
        sim = {}

        sim["integrator"] = {self._name:copy.deepcopy(self.getIntegrator())}

        sim["integrator"]["schedule"] = {
            "type":["Schedule","Integrator"],
            "labels":["order","integrator","steps"],
            "data":[[1,self._name,self.getIntegrationSteps()]]
        }

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

############### IMPORT ALL INTEGRATORS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
integrators = [os.path.basename(x) for x in glob.glob(currentPath+"/*.py")]
integrators = [x.split(".")[0] for x in integrators if "__" not in x]

for i in integrators:
    try:
        exec(f"from .{i} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[Integrator] Error importing integrator type component {i}")
