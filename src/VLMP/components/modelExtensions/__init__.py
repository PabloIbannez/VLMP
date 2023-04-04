import os
import copy

################ MODEL INTERFACE ################

from UAMMD.simulation import simulation

from ...utils import getSelections

class modelExtensionBase:

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 models,
                 availableParameters:set,
                 requiredParameters:set,
                 requiredSelections:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units  = units
        self._models = models

        self.logger.debug(f"[ModelExtension] ({self._type}) Extending models: "+
                          " ".join([m.getName() for m in self._models])+
                          ". For model extension: "+self._name)

        self.availableParameters =  availableParameters.copy()
        self.availableParameters.update({"startStep","endStep"})

        self.requiredParameters  =  requiredParameters.copy()
        self.requiredSelections  =  requiredSelections.copy()

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters and par not in self.requiredSelections:
                self.logger.error(f"[ModelExtension] ({self._type}) Parameter {par} not available for model extension {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params and par not in self.requiredSelections:
                self.logger.error(f"[ModelExtension] ({self._type}) Required parameter {par} not given for model extension {self._name}")
                raise ValueError(f"Required parameter not given")

        self.logger.info(f"[ModelExtension] ({self._type}) Using model extension {self._name}")

        ########################################################

        self._startStep = params.get("startStep",None)
        self._endStep   = params.get("endStep",None)

        ########################################################

        #Process selections
        self._selection = getSelections(self._models,
                                        self.requiredSelections,
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
            raise ValueError(f"Extension not initialized")

        if self._startStep is not None:
            self._extension[self.getName()]["parameters"]["startStep"] = self._startStep
        if self._endStep is not None:
            self._extension[self.getName()]["parameters"]["endStep"]   = self._endStep

        return self._extension

    ########################################################

    def getUnits(self):
        return self._units

    def getSelection(self,selectionName):
        return self._selection[selectionName]

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):

        sim = {}

        sim["topology"] = {}
        sim["topology"]["forceField"] = self.getExtension()

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
extensions = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
extensions = [ m.split("/")[-1].split(".")[0] for m in extensions ]

for e in extensions:
    try:
        exec(f"from .{e} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[ModelExtension] Error importing model extension type component {e}")
