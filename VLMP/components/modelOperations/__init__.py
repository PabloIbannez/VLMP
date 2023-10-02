import os
import copy

import logging

################ MODEL INTERFACE ################

from pyUAMMD import simulation

from .. import idsHandler

from ...utils.selections import getSelections

class modelOperationBase(idsHandler):

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

        self._units = units
        self._types = types
        self._ensemble = ensemble

        self._models = models

        self.logger.debug(f"[ModelOperation] ({self._type}) Operating on models: "+
                          " ".join([m.getName() for m in self._models])+
                          ". For model operation: "+self._name)

        self.availableParameters  = availableParameters.copy()
        self.requiredParameters   = requiredParameters.copy()
        self.availableSelections  = availableSelections.copy()
        self.requiredSelections   = requiredSelections.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[ModelOperation] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for model operation {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check all required selections are available selections
        if not self.requiredSelections.issubset(self.availableSelections):
            notAvailable = self.requiredSelections.difference(self.availableSelections)
            self.logger.error(f"[ModelOperation] ({self._type}) Some required selections ({notAvailable}) are not available selections for model operation {self._name}")
            raise Exception(f"Required selections are not available selections")

        # Check if all parameters and selectors given by params are available
        for par in params:
            if par not in self.availableParameters and par not in self.availableSelections:
                self.logger.error(f"[ModelOperation] ({self._type}) Parameter or selection {par} not available for model operation {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[ModelOperation] ({self._type}) Required parameter {par} not given for model operation {self._name}")
                raise Exception(f"Required parameter not given")

        # Check if all required selections are given
        for sel in self.requiredSelections:
            if sel not in params:
                self.logger.error(f"[ModelOperation] ({self._type}) Required selection {sel} not given for model operation {self._name}")
                raise Exception(f"Required selection not given")

        self.logger.info(f"[ModelOperation] ({self._type}) Using model operation {self._name}")

        ########################################################

        #Process selections
        selections = [sel for sel in params if sel in self.availableSelections]
        self._selection = getSelections(self._models,
                                        selections,
                                        **params)

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

    def getSelection(self,selectionName):
        return self._selection[selectionName]

    ########################################################

    def getIdsProperty(self,ids,propertyName):
        return self._getIdsProperty(ids,propertyName)

    def getIdsState(self,ids,stateName):
        return self._getIdsState(ids,stateName)

    def getIdsStructure(self,ids,structName):
        return self._getIdsStructure(ids,structName)

    def setIdsState(self,ids,stateName,states):
        self._setIdsState(ids,stateName,states)


############### IMPORT ALL MODEL OPERATIONS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
operations = [os.path.basename(x) for x in glob.glob(currentPath+"/*.py")]
operations = [x.split(".")[0] for x in operations if "__" not in x]

for o in operations:
    try:
        exec(f"from .{o} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[ModelOperation] Error importing model operation type component {o}")
