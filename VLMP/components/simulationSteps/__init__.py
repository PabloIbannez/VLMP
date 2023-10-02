import os
import copy

import logging

################ SIMULATION STEP INTERFACE ################

from pyUAMMD import simulation

from .. import idsHandler

from ...utils.selections import getSelections

class simulationStepBase(idsHandler):

    def __init__(self,
                 _type:str,_name:str,
                 units,types,ensemble,
                 models,
                 availableParameters:set,
                 requiredParameters:set,
                 availableSelections:set,
                 requiredSelections:set,
                 **params):
        super().__init__(models)

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units  = units
        self._types  = types
        self._ensemble = ensemble

        self._models = models

        self.availableParameters = availableParameters.copy()
        self.availableParameters.update({"startStep","endStep","intervalStep"})
        self.availableSelections = availableSelections.copy()

        self.requiredParameters  = requiredParameters.copy()
        self.requiredParameters.update({"intervalStep"})
        self.requiredSelections  = requiredSelections.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[SimulationStep] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for model extension {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check all required selections are available selections
        if not self.requiredSelections.issubset(self.availableSelections):
            notAvailable = self.requiredSelections.difference(self.availableSelections)
            self.logger.error(f"[SimulationStep] ({self._type}) Some required selections ({notAvailable}) are not available selections for model extension {self._name}")
            raise Exception(f"Required selections are not available selections")

        # Check if all parameters and selectors given by params are available
        for par in params:
            if par not in self.availableParameters and par not in self.availableSelections:
                self.logger.error(f"[SimulationStep] ({self._type}) Parameter or selection {par} not available for model extension {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[SimulationStep] ({self._type}) Required parameter {par} not given for model extension {self._name}")
                raise Exception(f"Required parameter not given")

        # Check if all required selections are given
        for sel in self.requiredSelections:
            if sel not in params:
                self.logger.error(f"[SimulationStep] ({self._type}) Required selection {sel} not given for model extension {self._name}")
                raise Exception(f"Required selection not given")

        self.logger.info(f"[SimulationStep] ({self._type}) Using simulation step {self._name}")

        ########################################################

        self._intervalStep = params["intervalStep"]

        self._startStep = params.get("startStep",None)
        self._endStep   = params.get("endStep",None)

        ########################################################

        #Process selections
        selections = [sel for sel in params if sel in self.availableSelections]
        self._selection = getSelections(self._models,
                                        selections,
                                        **params)

        ########################################################

        self._simulationStep = None
        self._group = None

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

    def getModels(self):
        return self._models

    ########################################################

    def setSimulationStep(self, simulationStep):
        self._simulationStep = simulationStep

    def getSimulationStep(self):
        if self._simulationStep is None:
            self.logger.error(f"[SimulationStep] ({self._type}) Simulation step {self._name} not initialized")
            raise Exception(f"Simulation step not initialized")

        self._simulationStep[self.getName()]["parameters"]["intervalStep"] = self._intervalStep

        if self._startStep is not None:
            self._simulationStep[self.getName()]["parameters"]["startStep"] = self._startStep
        if self._endStep is not None:
            self._simulationStep[self.getName()]["parameters"]["endStep"]   = self._endStep

        return self._simulationStep

    def setGroup(self,selSelections):

        #If selSelections is not a list, make it a list
        if not isinstance(selSelections,list):
            selSelections = [selSelections]

        #Check if all sel in selSelections are available selections
        if not set(selSelections).issubset(self.availableSelections):
            notAvailable = set(selSelections).difference(self.availableSelections)
            self.logger.error(f"[SimulationStep] ({self._type}) Some selections ({notAvailable}),"
                              f" requested to set a group, are not available selections for simulation step {self._name}")
            raise Exception(f"Selections not available")

        selections = [sel for sel in self._selection.keys() if sel in selSelections]

        ids = []
        for sel in selections:
            ids.extend(self.getSelection(sel))

        #If ids is empty, then no particles were selected. Do nothing
        if len(ids) == 0:
            return

        self._group = {"type":["Groups","GroupsList"],
                       "parameters":{},
                       "labels":["name","type","selection"],
                       "data":[[self.getName(),"Ids",list(set(ids)).copy()]]}

    ########################################################

    def getSelection(self,selectionName):
        return self._selection[selectionName]

    ########################################################

    def getIdsProperty(self,ids,propertyName):
        return self._getIdsProperty(ids,propertyName)

    def getIdsState(self,ids,stateName):
        return self._getIdsState(ids,stateName)

    def getIdsStructure(self,ids,structName):
        return self._getIdsStructure(ids,structName)

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):

        simulationStep = {"simulationStep":self.getSimulationStep()}

        if self._group is not None:
            for sim in simulationStep["simulationStep"]:
                simulationStep["simulationStep"][sim]["parameters"]["group"] = self.getName()
            simulationStep["simulationStep"]["group"+self.getName()] = self._group

        return simulation(copy.deepcopy(simulationStep),DEBUG_MODE)

############### IMPORT ALL SIMULATION STEPS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
simulationSteps = [os.path.basename(x) for x in glob.glob(currentPath+"/*.py")]
simulationSteps = [x.split(".")[0] for x in simulationSteps if "__" not in x]

for s in simulationSteps:
    try:
        exec(f"from .{s} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[SimulationStep] Error importing simulationStep type {s}")
