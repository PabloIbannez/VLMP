import os
import copy

################ MODEL INTERFACE ################

from UAMMD.simulation import simulation

from ...utils import getLabelIndex
from ...utils import getSelections

class modelOperationBase:

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

        self._units = units
        self._models = models

        self.logger.debug(f"[ModelOperation] ({self._type}) Operating on models: "+
                          " ".join([m.getName() for m in self._models])+
                          ". For model operation: "+self._name)

        self.availableParameters  = availableParameters.copy()
        self.requiredParameters = requiredParameters.copy()
        self.requiredSelections   = requiredSelections.copy()

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters and par not in self.requiredSelections:
                self.logger.error(f"[ModelOperation] ({self._type}) Parameter {par} not available for model operation {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params and par not in self.requiredSelections:
                self.logger.error(f"[ModelOperation] ({self._type}) Required parameter {par} not given for model operation {self._name}")
                raise ValueError(f"Required parameter not given")

        self.logger.info(f"[ModelOperation] ({self._type}) Using model operation {self._name}")

        ########################################################

        #Process selections
        self._selection = getSelections(self._models,
                                        self.requiredSelections,
                                        **params)

        ########################################################

        self.id2mdl   = list(range(sum([mdl.getNumberOfParticles() for mdl in self._models])))
        self.id2mdlId = copy.deepcopy(self.id2mdl)

        offset=0
        for mdlIndex,mdl in enumerate(self._models):
            for i in range(mdl.getNumberOfParticles()):
                self.id2mdl[i+offset] = mdlIndex
                self.id2mdlId[i+offset] = i
            offset+=mdl.getNumberOfParticles()

        ########################################################

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def getUnits(self):
        return self._units

    def getSelection(self,selectionName):
        return self._selection[selectionName]

    def getIdsProperty(self,ids,propertyName):
         idProp = []

         for i in ids:
             mdl   = self.id2mdl[i]

             typeIndex = getLabelIndex("type",self._models[mdl].getStructure()["labels"])
             itype     = self._models[mdl].getStructure()["data"][self.id2mdlId[i]][typeIndex]

             nameIndex = getLabelIndex("name",self._models[mdl].getTypes()["labels"])
             propIndex = getLabelIndex(propertyName,self._models[mdl].getTypes()["labels"])
             for t in self._models[mdl].getTypes()["data"]:
                 if itype == t[nameIndex]:
                     idProp.append(t[propIndex])
                     break

         return idProp


    def getIdPositions(self,ids):
        idPos = []

        for i in ids:
            mdl   = self.id2mdl[i]

            posIndex = getLabelIndex("position",self._models[mdl].getState()["labels"])
            idPos.append(self._models[mdl].getState()["data"][self.id2mdlId[i]][posIndex])

        return idPos

    def setIdPositions(self,ids,pos):
        if len(ids) != len(pos):
            self.logger.error(f"[ModelOperation] ({self._type}) Number of ids and positions do not match")
            raise ValueError(f"Number of ids and positions do not match")

        for i,p in zip(ids,pos):
            mdl   = self.id2mdl[i]

            posIndex = getLabelIndex("position",self._models[mdl].getState()["labels"])
            self._models[mdl].getState()["data"][self.id2mdlId[i]][posIndex] = p


############### IMPORT ALL MODEL OPERATIONS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
operations = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
operations = [ m.split("/")[-1].split(".")[0] for m in operations ]

for o in operations:
    try:
        exec(f"from .{o} import *")
    except:
        logging.getLogger("VLMP").error(f"[ModelOperation] Error importing model operation type component {o}")
