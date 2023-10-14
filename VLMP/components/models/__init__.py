import os
import copy

import logging

################ MODEL INTERFACE ################

import abc
from pyUAMMD import simulation

from ...utils.input import getLabelIndex

class modelBase(metaclass=abc.ABCMeta):

    def __init__(self,
                 _type:str,_name:str,
                 units,types,ensemble,
                 availableParameters:set,
                 requiredParameters:set,
                 definedSelections:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units    = units
        self._types    = types
        self._ensemble = ensemble

        self.availableParameters = availableParameters.copy()
        self.requiredParameters  = requiredParameters.copy()
        self.definedSelections   = definedSelections.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[Model] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for model {self._name}")
            raise Exception(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Model] ({self._type}) Parameter {par} not available for model {self._name}")
                raise Exception(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Model] ({self._type}) Required parameter {par} not given for model {self._name}")
                raise Exception(f"Required parameter not given")

        self.logger.info(f"[Model] ({self._type}) Using model {self._name}")

        ########################################################

        self._idOffset   = None

        ########################################################

        self._state      = None
        self._structure  = None
        self._forceField = None

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

    def setState(self,state):
        self._state = state

    def setStructure(self,structure):
        self._structure = structure

    def setForceField(self,forceField):
        self._forceField = forceField

    def getState(self):
        if self._state is None:
            self.logger.error(f"[Model] ({self._type}) State not set")
            raise Exception(f"State not set")
        return self._state

    def getStructure(self):
        if self._structure is None:
            self.logger.error(f"[Model] ({self._type}) Structure not set")
            raise Exception(f"Structure not set")
        return self._structure

    def getForceField(self):
        if self._forceField is None:
            self.logger.error(f"[Model] ({self._type}) Force field not set")
            raise Exception(f"Force field not set")
        return self._forceField

    ########################################################

    def getNumberOfParticles(self):
        if self._state is None:
            return 0
        return len(self.getState()["data"])

    def getLocalIds(self):
        if self._state is None:
            return []
        ids = []
        idIndex = getLabelIndex("id",self.getState()["labels"])
        for entry in self.getState()["data"]:
            ids.append(entry[idIndex])
        return ids

    def setIdOffset(self,offset):
        self._idOffset = offset

    def getIdOffset(self):
        if self._idOffset is None:
            self.logger.error(f"[Model] ({self._type}) Id offset not set")
            raise Exception(f"Id offset not set")
        return self._idOffset

    def getGlobalIds(self):
        globalIds = []
        for localId in self.getLocalIds():
            globalIds.append(localId + self.getIdOffset())
        return globalIds

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):

        # Create simulation

        sim = {}

        if self._state is not None:
            sim["state"]  = self.getState()

        sim["topology"] = {}
        if self._structure is not None:
            sim["topology"]["structure"]  = self.getStructure()
        if self._forceField is not None:
            sim["topology"]["forceField"] = self.getForceField()

        return simulation(copy.deepcopy(sim),DEBUG_MODE)

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'processSelection') and
                callable(subclass.processSelection)   and
                NotImplemented)

    @abc.abstractmethod
    def processSelection(self,**params):
        """ Return a index of the particles that are selected """
        raise NotImplementedError

    def getSelection(self,**params):
        # If no selection is given, select all particles
        if len(params) == 0:
            return self.getLocalIds()
        # Check if all selectors given by params are available
        for par in params:
            if par not in self.definedSelections:
                self.logger.error(f"[Model] ({self._type}) Selector {par} not available for model {self._name}")
                raise Exception(f"Selector not available")
        return self.processSelection(**params)

    ########################################################
    #Common selections functions

    def getParticleIdSelection(self,particleId):
        #Check if particleId is a list
        if not isinstance(particleId,list):
            particleId = [particleId]

        localIds = self.getLocalIds()
        # Check if particleId is in localIds
        for pid in particleId:
            if pid not in localIds:
                self.logger.error(f"[Model] ({self._type}) Particle id {pid} not in local ids")
                raise Exception(f"Particle id not in local ids")

        return particleId.copy()

    def getForceFieldSelection(self,forceFieldEntriesName):
        #Check if forceFieldEntriesName is a list
        if not isinstance(forceFieldEntriesName,list):
            forceFieldEntriesName = [forceFieldEntriesName]

        sel = []

        forceField = self.getForceField()
        # Check if forceFieldEntriesName is in forceField
        for ff in forceFieldEntriesName:
            if ff not in forceField:
                self.logger.error(f"[Model] ({self._type}) Force field entry {ff} not in force field")
                raise Exception(f"Force field entry not in force field")
            else:
                entryType = forceField[ff]["type"][0]

                entryLabels = forceField[ff]["labels"]
                entryData   = forceField[ff]["data"]

                if entryType == "Bond1":
                    id1Index = getLabelIndex("id_i",entryLabels)
                    for i in range(len(entryData)):
                        id1 = int(entryData[i][id1Index])
                        sel.append(id1)

                elif entryType == "Bond2":
                    id1Index = getLabelIndex("id_i",entryLabels)
                    id2Index = getLabelIndex("id_j",entryLabels)
                    for i in range(len(entryData)):
                        id1 = int(entryData[i][id1Index])
                        id2 = int(entryData[i][id2Index])
                        sel.append([id1,id2])

                elif entryType == "Bond3":
                    id1Index = getLabelIndex("id_i",entryLabels)
                    id2Index = getLabelIndex("id_j",entryLabels)
                    id3Index = getLabelIndex("id_k",entryLabels)
                    for i in range(len(entryData)):
                        id1 = int(entryData[i][id1Index])
                        id2 = int(entryData[i][id2Index])
                        id3 = int(entryData[i][id3Index])
                        sel.append([id1,id2,id3])

                elif entryType == "Bond4":
                    id1Index = getLabelIndex("id_i",entryLabels)
                    id2Index = getLabelIndex("id_j",entryLabels)
                    id3Index = getLabelIndex("id_k",entryLabels)
                    id4Index = getLabelIndex("id_l",entryLabels)
                    for i in range(len(entryData)):
                        id1 = int(entryData[i][id1Index])
                        id2 = int(entryData[i][id2Index])
                        id3 = int(entryData[i][id3Index])
                        id4 = int(entryData[i][id4Index])
                        sel.append([id1,id2,id3,id4])

                else:
                    self.logger.error(f"[Model] ({self._type}) Force field entry {ff} has not an available type."
                                       "Available types are: Bond1, Bond2, Bond3, Bond4")
                    raise Exception(f"Force field entry has not an available type")

        return sel.copy()


############### IMPORT ALL MODELS ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
models = [os.path.basename(x) for x in glob.glob(currentPath+"/*.py")]
models = [x.split(".")[0] for x in models if "__" not in x]

for m in models:
    try:
        exec(f"from .{m} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[Model] Error importing model type component {m}")
