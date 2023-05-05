import os
import copy

import logging

################ MODEL INTERFACE ################

from pyUAMMD import simulation

from ...utils.utils import getSelections

class modelExtensionBase:

    def __init__(self,
                 _type:str,_name:str,
                 units,types,
                 models,
                 availableParameters:set,
                 requiredParameters:set,
                 availableSelections:set,
                 requiredSelections:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units  = units
        self._types  = types
        self._models = models

        self.logger.debug(f"[ModelExtension] ({self._type}) Extending models: "+
                          " ".join([m.getName() for m in self._models])+
                          ". For model extension: "+self._name)

        self.availableParameters =  availableParameters.copy()
        self.availableParameters.update({"startStep","endStep"})
        self.availableSelections  =  availableSelections.copy()

        self.requiredParameters  =  requiredParameters.copy()
        self.requiredSelections  =  requiredSelections.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[ModelExtension] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for model extension {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check all required selections are available selections
        if not self.requiredSelections.issubset(self.availableSelections):
            notAvailable = self.requiredSelections.difference(self.availableSelections)
            self.logger.error(f"[ModelExtension] ({self._type}) Some required selections ({notAvailable}) are not available selections for model extension {self._name}")
            raise Exception(f"Required selections are not available selections")

        # Check if all parameters and selectors given by params are available
        for par in params:
            if par not in self.availableParameters and par not in self.availableSelections:
                self.logger.error(f"[ModelExtension] ({self._type}) Parameter or selection {par} not available for model extension {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[ModelExtension] ({self._type}) Required parameter {par} not given for model extension {self._name}")
                raise Exception(f"Required parameter not given")

        # Check if all required selections are given
        for sel in self.requiredSelections:
            if sel not in params:
                self.logger.error(f"[ModelExtension] ({self._type}) Required selection {sel} not given for model extension {self._name}")
                raise Exception(f"Required selection not given")

        self.logger.info(f"[ModelExtension] ({self._type}) Using model extension {self._name}")

        ########################################################

        self._startStep = params.get("startStep",None)
        self._endStep   = params.get("endStep",None)

        ########################################################

        #Process selections
        selections = [sel for sel in params if sel in self.availableSelections]
        self._selection = getSelections(self._models,
                                        selections,
                                        **params)

        ########################################################

        self._extension = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def setExtension(self,extension):
        self._extension = extension

    def getExtension(self):
        if self._extension is None:
            self.logger.error(f"[ModelExtension] ({self._type}) Extension not initialized")
            raise Exception(f"Extension not initialized")

        if self._startStep is not None:
            self._extension[self.getName()]["parameters"]["startStep"] = self._startStep
        if self._endStep is not None:
            self._extension[self.getName()]["parameters"]["endStep"]   = self._endStep

        return self._extension

    ########################################################

    def getUnits(self):
        return self._units

    def getTypes(self):
        return self._types

    def getSelection(self,selectionName):
        return self._selection[selectionName]

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):

        sim = {}

        sim["topology"] = {}
        sim["topology"]["forceField"] = self.getExtension()

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

############### IMPORT ALL MODEL EXTENSIONS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
extensions = [ module.rsplit(".")[1] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
extensions = [ m.split("/")[-1].split(".")[0] for m in extensions ]

for e in extensions:
    try:
        exec(f"from .{e} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[ModelExtension] Error importing model extension type component {e}")
