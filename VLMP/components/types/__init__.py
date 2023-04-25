import os
import copy

################ TYPES INTERFACE ################

from pyUAMMD import simulation

class typesBase:

    def __init__(self,
                 _type:str,_name:str,
                 units,
                 availableParameters:set,
                 requiredParameters:set,
                 **params):

        self.logger = logging.getLogger("VLMP")

        self._type = _type
        self._name = _name

        self._units  = units

        self.availableParameters = availableParameters.copy()
        self.requiredParameters  = requiredParameters.copy()

        # Check all required parameters are available parameters
        if not self.requiredParameters.issubset(self.availableParameters):
            notAvailable = self.requiredParameters.difference(self.availableParameters)
            self.logger.error(f"[Types] ({self._type}) Some required parameters ({notAvailable}) are not available parameters for types {self._name}")
            raise ValueError(f"Required paramaters are not available parameters")

        # Check if all parameters given by params are available
        for par in params:
            if par not in self.availableParameters:
                self.logger.error(f"[Types] ({self._type}) Parameter {par} not available for types {self._name}")
                raise ValueError(f"Parameter not available")

        # Check if all required parameters are given
        for par in self.requiredParameters:
            if par not in params:
                self.logger.error(f"[Types] ({self._type}) Required parameter {par} not given for types {self._name}")
                raise ValueError(f"Required parameter not given")

        self.logger.info(f"[Types] ({self._type}) Using types {self._name}")

        ########################################################

        self._typesUAMMD = None
        self._typesComp  = None
        self._typesDecl  = None

    ########################################################

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    ########################################################

    def getUnits(self):
        return self._units

    def getTypes(self):
        if self._typesComp is None:
            self.logger.error(f"[Types] ({self._type}) Types components not set for types {self._name}")
            raise ValueError(f"Types components not set")
        if self._typesDecl is None:
            self.logger.error(f"[Types] ({self._type}) Types not declared for types {self._name}")
            raise ValueError(f"Types not declared")

        types = {}

        components = [comp for comp in self.getTypesComponents().keys()]
        for typDecl in self._typesDecl:
            types[typDecl["name"]] = {comp:typDecl[comp] for comp in components}

        return copy.deepcopy(types)

    def setTypesName(self, typesUAMMD):
        self._typesUAMMD = typesUAMMD

    def getTypesName(self):
        if self._typesUAMMD is None:
            self.logger.error(f"[Types] ({self._type}) Types not set for types {self._name}")
            raise ValueError(f"Types not set")
        return self._typesUAMMD

    def addTypesComponent(self, typesCompName, defaultValue):
        if self._typesComp is None:
            self._typesComp = {"name":None}
        if typesCompName in self._typesComp.keys():
            self.logger.error(f"[Types] ({self._type}) Component {typesCompName} already declared for types {self._name}.")
            raise ValueError(f"Component already declared")
        self._typesComp[typesCompName] = defaultValue

    def getTypesComponents(self):
        if self._typesComp is None:
            self.logger.error(f"[Types] ({self._type}) Types components not set for types {self._name}")
            raise ValueError(f"Types components not set")
        return self._typesComp

    def addType(self, **components):
        if self._typesComp is None:
            self.logger.error(f"[Types] ({self._type}) Types components not set for types {self._name}")
            raise ValueError(f"Types components not set")
        if self._typesDecl is None:
            self._typesDecl = []
        #Check name in components
        if "name" not in components.keys():
            self.logger.error(f"[Types] ({self._type}) Name not given when declaring types {self._name}. Declaration: {components}")
            raise ValueError(f"Name not given")

        #Check if all keys of components are available
        for key in components:
            if key not in self._typesComp.keys():
                self.logger.error(f"[Types] ({self._type}) Component {key} not available for types {self._name}. Available components are {list(self._typesComp.keys())}")
                raise ValueError(f"Component not available")

        typeDecl = {}
        for key in self._typesComp.keys():
            if key in components:
                typeDecl[key] = components[key]
            else:
                typeDecl[key] = self._typesComp[key]
                self.logger.warning(f"[Types] ({self._type}) Component {key} not given for types {self._name}. Using default value {self._typesComp[key]}")

        self._typesDecl.append(copy.deepcopy(typeDecl))

    ########################################################

    def getSimulation(self,DEBUG_MODE = False):

        labels = [comp for comp in self.getTypesComponents().keys()]

        data = []

        if self._typesDecl is None:
            self.logger.error(f"[Types] ({self._type}) Types not declared for types {self._name}")
            raise ValueError(f"Types not declared")
        else:
            for types in self._typesDecl:
                data.append([types[comp] for comp in labels])

        return simulation({"global":{"parameters":copy.deepcopy({"types":self.getTypesName()}),
                                     "labels":copy.deepcopy(labels),
                                     "data":copy.deepcopy(data)}},DEBUG_MODE)

############### IMPORT ALL TYPES ###############

import glob

currentPath = os.path.dirname(os.path.abspath(__file__))
types = [ module.split(".")[0] for module in glob.glob(currentPath+"/*.py") if not "__" in module]
types = [ t.split("/")[-1].split(".")[0] for t in types ]

for t in types:
    try:
        exec(f"from .{t} import *")
    except Exception as e:
        logging.getLogger("VLMP").error(e)
        logging.getLogger("VLMP").error(f"[Types] Error importing types type component {t}")
