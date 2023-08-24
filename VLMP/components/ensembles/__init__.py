import os
import copy

import logging

################ ENSEMBLE INTERFACE ################

from pyUAMMD import simulation

from ...utils.input import getLabelIndex

class ensembleBase:

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 types,
                 availableParameters:set,
                 requiredParameters:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units = units
        self._types = types

        self.availableParameters = availableParameters.copy()
        self.requiredParameters  = requiredParameters.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[Ensemble] ({self._type}) Some required parameters ({notAvailable}) \
                              are not available parameters for ensemble {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Ensemble] ({self._type}) Parameter {par} \
                                    not available for ensemble {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Ensemble] ({self._type}) Required parameter \
                                    {par} not given for ensemble {self._name}")
                raise Exception(f"Required parameter not given")

        self.logger.info(f"[Ensemble] ({self._type}) Using ensemble {self._name}")

        ########################################################

        self._ensembleUAMMD = None
        self._ensembleComp  = None
        self._ensembleVal   = None

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

    ########################################################

    def setEnsembleName(self, ensembleUAMMD):
        self._ensembleUAMMD = ensembleUAMMD

    def getEnsembleName(self):
        if self._ensembleUAMMD is None:
            self.logger.error(f"[Ensemble] ({self._type}) Ensemble {self._name} has not been set")
            raise Exception(f"Ensemble not set")

        return self._ensembleUAMMD

    def addEnsembleComponent(self,componentName,componentValue):
        if self._ensembleComp is None:
            self._ensembleComp = {}
        if componentName in self._ensembleComp:
            self.logger.error(f"[Ensemble] ({self._type}) Component {componentName} \
                                already added to ensemble {self._name}")
            raise Exception(f"Component already added")

        self._ensembleComp[componentName] = componentValue

    def getEnsembleComponents(self):
        if self._ensembleComp is None:
            self.logger.error(f"[Ensemble] ({self._type}) No components added to ensemble {self._name}")
            raise Exception(f"No components added")

        return self._ensembleComp

    def getEnsembleComponent(self,componentName):
        if self._ensembleComp is None:
            self.logger.error(f"[Ensemble] ({self._type}) No components added to ensemble {self._name}")
            raise Exception(f"No components added")
        if componentName not in self._ensembleComp:
            self.logger.error(f"[Ensemble] ({self._type}) Component {componentName} \
                                not added to ensemble {self._name}")
            raise Exception(f"Component not added")

        return self._ensembleComp[componentName]

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):
        labels = []
        data   = []

        for l in self.getEnsembleComponents():
            labels.append(l)
            data.append(self.getEnsembleComponent(l))

        return simulation({"global":{"ensemble":{
                                        "type":["Ensemble",self.getEnsembleName()],
                                        "labels":copy.deepcopy(labels),
                                        "data":[copy.deepcopy(data)]
                                                }
                                    }
                           },DEBUG_MODE)

############### IMPORT ALL ENSEMBLES ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
ensembles_ = [os.path.basename(x) for x in glob.glob(currentPath+"/*.py")]
ensembles_ = [x.split(".")[0] for x in ensembles_ if "__" not in x]

for e in ensembles_:
    try:
        exec(f"from .{e} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[Ensemble] Error importing ensemble type component \"{e}\"")
