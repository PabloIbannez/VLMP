import os
import logging

import copy

from tqdm import tqdm

import json
import jsbeautifier

from collections import OrderedDict

from . import DEBUG_MODE

import VLMP.components.systems         as _systems
import VLMP.components.units           as _units
import VLMP.components.types           as _types
import VLMP.components.ensembles       as _ensembles
import VLMP.components.models          as _models
import VLMP.components.modelOperations as _modelOperations
import VLMP.components.modelExtensions as _modelExtensions
import VLMP.components.integrators     as _integrators
import VLMP.components.simulationSteps as _simulationSteps

from pyUAMMD.utils.merging.merging import mergeSimulationsSet

import importlib
import inspect

class VLMP:

    def __setUpAdditionalComponents(self,additionalComponets = None):

        for component in self.availableComponents:
            compName = "additional" + component[0].upper() + component[1:]
            setattr(self,compName,None)

        if additionalComponets is not None:

            if os.path.isdir(additionalComponets):
                self.logger.info("[VLMP] Loading additional components from \"%s\"",additionalComponets)
            else:
                #Create additional components folder
                self.logger.info("[VLMP] Creating additional components folder \"%s\"",additionalComponets)
                os.mkdir(additionalComponets)

            #Check a folder for each available component exists, else create it
            for component in self.availableComponents:
                componentPath = os.path.join(additionalComponets,component)
                if not os.path.isdir(componentPath):
                    self.logger.info("[VLMP] Creating additional components folder \"%s\"",componentPath)
                    os.mkdir(componentPath)

            #Check a file named "__init__.py" exists in each folder, else create it
            for component in self.availableComponents:
                componentPath = os.path.join(additionalComponets,component,"__init__.py")
                if not os.path.isfile(componentPath):
                    self.logger.info("[VLMP] Creating __init__.py for additional components folder \"%s\"",componentPath)
                    open(componentPath,"w").close()

            for component in self.availableComponents:
                compName = "additional" + component[0].upper() + component[1:]
                setattr(self,compName,importlib.import_module(".".join([additionalComponets,component])))

            #List all additional components imported
            for component in self.availableComponents:
                compName = "additional" + component[0].upper() + component[1:]
                comp = [name for name, obj in vars(eval(f"self.{compName}")).items() if not name.startswith('_') and name != f"{component}Base" and inspect.isclass(obj)]
                self.logger.info("[VLMP] Additional components \"%s\": %s",component,comp)

        self.componentsModules["system"]         ["additional"] = self.additionalSystem
        self.componentsModules["units"]          ["additional"] = self.additionalUnits
        self.componentsModules["types"]          ["additional"] = self.additionalTypes
        self.componentsModules["ensemble"]       ["additional"] = self.additionalEnsemble
        self.componentsModules["models"]         ["additional"] = self.additionalModels
        self.componentsModules["modelOperations"]["additional"] = self.additionalModelOperations
        self.componentsModules["modelExtensions"]["additional"] = self.additionalModelExtensions
        self.componentsModules["integrators"]    ["additional"] = self.additionalIntegrators
        self.componentsModules["simulationSteps"]["additional"] = self.additionalSimulationSteps

    ########################################

    #Distribute functions

    def __distributeSimulationPoolByMaxNumberOfParticles(self,maxNumberOfParticles):

        simulationSets = []

        for simSet in self.simulationSets:

            currentSet     = []
            currentSetSize = 0

            for simName in simSet:
                sim = self.simulations[simName]
                if currentSetSize + sim.getNumberOfParticles() > maxNumberOfParticles:
                    if len(currentSet) > 0:
                        simulationSets.append(currentSet)
                    currentSet     = []
                    currentSetSize = 0

                currentSet.append(simName)
                currentSetSize += sim.getNumberOfParticles()

            if len(currentSet) > 0:
                simulationSets.append(currentSet)

        #Print the number of simulations and the number of particles in each set
        for i in range(len(simulationSets)):
            self.logger.debug("[VLMP] Simulation set %d has %d simulations and %d particles (max %d)",
                              i,len(simulationSets[i]),
                              sum([self.simulations[simName].getNumberOfParticles() for simName in simulationSets[i]]),
                              maxNumberOfParticles)

        return simulationSets.copy()

    def __distributeSimulationPoolBySize(self,size):
        simulationSets = []

        for simSet in self.simulationSets:

            currentSet     = []
            currentSetSize = 0

            for simName in simSet:
                sim = self.simulations[simName]
                if currentSetSize + 1 > size:
                    if len(currentSet) > 0:
                        simulationSets.append(currentSet)
                    currentSet     = []
                    currentSetSize = 0

                currentSet.append(simName)
                currentSetSize += 1

            if len(currentSet) > 0:
                simulationSets.append(currentSet)

        #Print the number of simulations and the number of particles in each set
        for i in range(len(simulationSets)):
            self.logger.debug("[VLMP] Simulation set %d has %d simulations",
                              i,len(simulationSets[i]))

        return simulationSets.copy()

    def __distributeSimulationPoolByProperty(self,propertyPath):

        simulationSets = []

        for simSet in self.simulationSets:

            simulationSetsProp = {}

            for simName in simSet:
                sim = self.simulations[simName]
                #Get the property value
                try:
                    propertyValue = sim[propertyPath[0]]
                    for i in range(1,len(propertyPath)):
                        propertyValue = propertyValue[propertyPath[i]]
                except:
                    self.logger.error("[VLMP] Property \"%s\" not found in simulation",propertyPath)
                    raise Exception("Property not found in simulation")

                if propertyValue not in simulationSetsProp.keys():
                    simulationSetsProp[propertyValue] = []

                simulationSetsProp[propertyValue].append(simName)

            simulationSets += simulationSetsProp.values()

        #Print the number of simulations and the number of particles in each set
        for i in range(len(simulationSets)):
            self.logger.debug("[VLMP] Simulation set %d has %d simulations",
                              i,len(simulationSets[i]))

        return simulationSets.copy()

    ########################################

    def __checkComponent(self,component,componentClass,simulationBuffer):

        # Check if all component.keys() are in self.availableComponentEntries
        for key in component.keys():
            if key not in self.availableComponentEntries:
                self.logger.error("[VLMP] Component \"%s\" has an invalid entry \"%s\"",componentClass,key)
                raise Exception("Invalid component entry")

        componentType = component.get("type",None)

        if componentType is None:
            self.logger.error(f"[VLMP] Error processing \"{componentClass}\" component ({component}), \"type\" property not found")
            raise Exception("Component type not specified")
        self.logger.debug(f"[VLMP] Processing \"{componentClass}\" component ({component}), type \"{componentType}\"")

        componentName = component.get("name",None)
        if componentName is None:
            componentName = componentType
            self.logger.warning(f"[VLMP] ({componentClass}) Component name not specified, using \"{componentName}\".")
        self.logger.debug(f"[VLMP] ({componentClass}) Component name \"{componentName}\".")

        #Check if parameters are specified
        componentParameters = component.get("parameters",None)
        if componentParameters is None:
            componentParameters = {}
            self.logger.warning(f"[VLMP] ({componentClass}) Component parameters not specified, creating empty dictionary")
        self.logger.debug(f"[VLMP] ({componentClass}) Component parameters \"{componentParameters}\"")

        #Check if component is already loaded
        if "_".join([componentClass,componentName]) in simulationBuffer.keys():
            self.logger.error(f"[VLMP] ({componentClass}) Component \"{componentName}\" already loaded")
            raise Exception("Component already loaded")

        return componentType,componentName,componentParameters

    def __processSimulationPoolSection(self,
                                       simulationBuffer,
                                       simulationInfo,
                                       sectionName,
                                       addToSimulationBuffer,
                                       required,
                                       unique,
                                       units,types,ensemble,models):

        sectionNameUpper  = sectionName[0].upper()+sectionName[1:]

        if sectionName[-1] != "s":
            sectionNamePlural = sectionName+"s"
        else:
            sectionNamePlural = sectionName

        loadedComponents = []

        #Check if "sectionName" section is present
        if sectionName not in simulationInfo.keys():
            if not required:
                self.logger.warning(f"[VLMP] ({sectionName}) Section not found, skipping")
                return loadedComponents
            self.logger.error(f"[VLMP] {sectionNameUpper} section not found")
            raise Exception(f"{sectionNameUpper} section not found")
        else:

            if unique:
                #Only one unit system can be specified
                if len(simulationInfo[sectionName]) > 1:
                    self.logger.error(f"[VLMP] Only one {sectionName} entry can be specified")
                    raise Exception("Only one entry can be specified")

            for comp in simulationInfo[sectionName]:

                typ, name, param = self.__checkComponent(comp,sectionName,simulationBuffer)
                self.logger.debug(f"[VLMP] Adding {sectionName} \"{name}\"")

                isComp           = typ in dir(self.componentsModules[sectionName]["base"])
                isAdditionalComp = typ in dir(self.componentsModules[sectionName]["additional"])

                if not isComp and not isAdditionalComp:
                    self.logger.error(f"[VLMP] {sectionNameUpper} \"{typ}\" not found")
                    raise Exception(f"{sectionNameUpper} not found")

                if isComp and isAdditionalComp:
                    self.logger.error(f"[VLMP] {sectionNameUpper} \"{typ}\" found in both VLMP base and additional components")
                    raise Exception(f"{sectionNameUpper} found in both VLMP base and additional components")

                allArgs = {
                    'name'    : name,
                    'units'   : units,
                    'types'   : types,
                    'ensemble': ensemble,
                    'models'  : models
                }

                args = {k: v for k, v in allArgs.items() if v is not None}

                if isComp:

                    try:

                        initComp = eval(f"_{sectionNamePlural}.{typ}")(**args, **param)

                        if addToSimulationBuffer:
                            simulationBuffer[f"{sectionNamePlural}_{name}"] = initComp

                        loadedComponents.append(f"{sectionNamePlural}_{name}")
                    except:
                        self.logger.error(f"[VLMP] Error loading {sectionName} \"{name}\" ({typ})")
                        raise Exception(f"Error loading {sectionName}")

                if isAdditionalComp:
                    try:

                        initComp = eval(f"self.additional{sectionNameUpper}.{typ}")(**args,**param)

                        if addToSimulationBuffer:
                            simulationBuffer[f"{sectionName}_{name}"] = initComp

                        loadedComponents.append(f"{sectionName}_{name}")
                    except:
                        self.logger.error(f"[VLMP] Error loading {sectionName} \"{name}\" ({typ})")
                        raise Exception(f"Error loading {sectionName}")

        return loadedComponents

    ########################################

    def __init__(self,additionalComponets = None):
        self.logger = logging.getLogger("VLMP")

        self.logger.info("[VLMP] Starting VLMP")

        self.simulations    = OrderedDict()
        self.simulationSets = []

        self.availableComponents = ["system","units","types","ensemble",
                                    "models","modelOperations","modelExtensions",
                                    "integrators",
                                    "simulationSteps"]

        self.availableComponentEntries = ["type","name","parameters"]

        self.componentsModules = {"system"          : {"base":_systems        },
                                  "units"           : {"base":_units          },
                                  "types"           : {"base":_types          },
                                  "ensemble"        : {"base":_ensembles      },
                                  "models"          : {"base":_models         },
                                  "modelOperations" : {"base":_modelOperations},
                                  "modelExtensions" : {"base":_modelExtensions},
                                  "integrators"     : {"base":_integrators    },
                                  "simulationSteps" : {"base":_simulationSteps}}

        self.__setUpAdditionalComponents(additionalComponets)

    def loadSimulationPool(self,simulationPool:list):

        self.simulationsInfo = {}

        for simulationInfo in simulationPool:

            #Check all keys are available components
            for key in simulationInfo.keys():
                if key not in self.availableComponents:
                    self.logger.error("[VLMP] Unknown component \"%s\"",key)
                    self.logger.error("[VLMP] Available components are: %s",self.availableComponents)
                    raise Exception("Unknown component")

            simulationBuffer = OrderedDict()

            ############## SYSTEM ##############

            #### Get simulation name ####

            # Check there is one (and only one) system component of type "simulationName"
            simNameComponents = [component for component in simulationInfo["system"] if component["type"] == "simulationName"]
            if len(simNameComponents) == 0:
                self.logger.error("[VLMP] Simulation name not specified")
                raise Exception("Simulation name not specified")
            elif len(simNameComponents) > 1:
                self.logger.error("[VLMP] More than one simulation name specified")
                raise Exception("More than one simulation name specified")

            for comp in simulationInfo["system"]:

                typ, name, param = self.__checkComponent(comp,"system",simulationBuffer)

                #Read simulationName
                if typ == "simulationName":
                    simulationName = param["simulationName"]

                    #Check if other simulation with the same name has been already created
                    if simulationName in self.simulations.keys():
                        self.logger.error(f"[VLMP] Simulation with name \"{simulationName}\" already exists")
                        raise Exception("Simulation already exists")

            #############################

            _ = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                    simulationInfo   = simulationInfo,
                                                    sectionName      = "system",
                                                    addToSimulationBuffer = True,
                                                    required = True,
                                                    unique   = False,
                                                    units    = None,
                                                    types    = None,
                                                    ensemble = None,
                                                    models   = None)

            ############## UNITS ##############

            units = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                        simulationInfo = simulationInfo,
                                                        sectionName    = "units",
                                                        addToSimulationBuffer = True,
                                                        required = True,
                                                        unique   = False,
                                                        units    = None,
                                                        types    = None,
                                                        ensemble = None,
                                                        models   = None)

            units = simulationBuffer[units[0]]

            ############## TYPES ##############

            types = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                        simulationInfo = simulationInfo,
                                                        sectionName    = "types",
                                                        addToSimulationBuffer = True,
                                                        required = True,
                                                        unique   = False,
                                                        units    = units,
                                                        types    = None,
                                                        ensemble = None,
                                                        models   = None)

            types = simulationBuffer[types[0]]

            ############## ENSEMBLE ##############

            ensemble = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                           simulationInfo = simulationInfo,
                                                           sectionName    = "ensemble",
                                                           addToSimulationBuffer = True,
                                                           required = True,
                                                           unique   = False,
                                                           units    = units,
                                                           types    = types,
                                                           ensemble = None,
                                                           models   = None)

            ensemble = simulationBuffer[ensemble[0]]

            ############### MODEL ###############

            models = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                         simulationInfo = simulationInfo,
                                                         sectionName    = "models",
                                                         addToSimulationBuffer = True,
                                                         required = True,
                                                         unique   = False,
                                                         units    = units,
                                                         types    = types,
                                                         ensemble = ensemble,
                                                         models   = None)

            #Set idOffset for each model
            idOffset = 0
            for mdl in models:
                simulationBuffer[mdl].setIdOffset(idOffset)
                ids = simulationBuffer[mdl].getLocalIds()
                if len(ids) != 0:
                    idOffset += max(ids) + 1

            models = [simulationBuffer[model] for model in models]

            ############### MODEL OPERATIONS ###############

            _ = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                    simulationInfo = simulationInfo,
                                                    sectionName    = "modelOperations",
                                                    addToSimulationBuffer = False,
                                                    required = False,
                                                    unique   = False,
                                                    units    = units,
                                                    types    = types,
                                                    ensemble = ensemble,
                                                    models   = models)

            ############### MODEL EXTENSIONS ###############

            _ = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                    simulationInfo = simulationInfo,
                                                    sectionName    = "modelExtensions",
                                                    addToSimulationBuffer = True,
                                                    required = False,
                                                    unique   = False,
                                                    units    = units,
                                                    types    = types,
                                                    ensemble = ensemble,
                                                    models   = models)

            ############## INTEGRATOR ##############

            _ = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                    simulationInfo = simulationInfo,
                                                    sectionName    = "integrators",
                                                    addToSimulationBuffer = True,
                                                    required = True,
                                                    unique   = False,
                                                    units    = units,
                                                    types    = types,
                                                    ensemble = ensemble,
                                                    models   = models)

            ############### SIMULATION STEPS ###############

            _ = self.__processSimulationPoolSection(simulationBuffer = simulationBuffer,
                                                    simulationInfo = simulationInfo,
                                                    sectionName    = "simulationSteps",
                                                    addToSimulationBuffer = True,
                                                    required = False,
                                                    unique   = False,
                                                    units    = units,
                                                    types    = types,
                                                    ensemble = ensemble,
                                                    models   = models)

            ###############################################

            #Merge all components into a single simulation
            self.logger.debug("[VLMP] Merging components into a single simulation")

            sim = None
            for componentName,component in simulationBuffer.items():
                self.logger.debug(f"[VLMP] Merging component \"{componentName}\"")
                if sim is None:
                    sim = component.getSimulation(DEBUG_MODE)
                else:
                    sim.append(component.getSimulation(DEBUG_MODE),mode="modelId")
                self.logger.debug(f"[VLMP] Component \"{componentName}\" merged")
            #Simulation creation finished

            ###############################################

            #Store the simulation
            self.simulationsInfo[simulationName] = copy.deepcopy(simulationInfo)
            self.simulations[simulationName]     = sim

        ###############################################

        #At this point simulation pool is processed

        #Create default simulation set, all simulations in one set
        self.simulationSets = [list(self.simulations.keys())]

    def distributeSimulationPool(self,*mode):

        availableModes = ["none","one","upperLimit","size","property"]

        #Check at least one simulations has been loaded
        if len(self.simulations) == 0:
            self.logger.error("[VLMP] No simulations loaded")
            raise Exception("No simulations loaded")

        #Check mode
        if len(mode) == 0:
            self.logger.warning("[VLMP] No mode specified, using \"none\"")
            modeName = "none"
        else:
            modeName = mode[0]
            self.logger.debug(f"[VLMP] Distributing simulation pool using mode \"{modeName}\"")

        if modeName not in availableModes:
            self.logger.error("[VLMP] Distribute mode \"%s\" not available, available modes are: %s",modeName,availableModes)
            raise Exception("Distribute mode not available")
        else:
            #Switch to the selected mode
            if modeName == "none":
                pass
            elif  modeName == "one":
                self.simulationSets = [[i] for i in self.simulations.keys()]
            elif modeName == "upperLimit":
                self.logger.debug("[VLMP] Distributing simulation pool using upper limit")
                availableScoringProperties = ["numberOfParticles"]

                if len(mode) >= 2:
                    scoringPropertyName = mode[1]
                else:
                    self.logger.error("[VLMP] No scoring property specified")
                    raise Exception("No scoring property specified")

                if scoringPropertyName not in availableScoringProperties:
                    self.logger.error("[VLMP] Scoring property \"%s\" not available, available properties are: %s",
                                      scoringPropertyName,availableScoringProperties)
                    raise Exception("Scoring property not available")
                else:
                    #Switch to the selected scoring property
                    if scoringPropertyName == "numberOfParticles":
                        self.logger.debug("[VLMP] Distributing simulation pool using number of particles")
                        if len(mode) >= 3:
                            maxNumberOfParticles = mode[2]
                        else:
                            self.logger.error("[VLMP] No particle limit specified")
                            raise Exception("No upper limit specified")

                        #Distribute the simulation pool
                        self.simulationSets = self.__distributeSimulationPoolByMaxNumberOfParticles(maxNumberOfParticles)
                    #Scoring property switch finished
            elif modeName == "size":
                self.logger.debug("[VLMP] Distributing simulation pool using size")

                if len(mode) >= 2:
                    size = mode[1]
                else:
                    self.logger.error("[VLMP] No size specified")
                    raise Exception("No size specified")

                #Distribute the simulation pool
                self.simulationSets = self.__distributeSimulationPoolBySize(size)

            elif modeName == "property":
                self.logger.debug("[VLMP] Distributing simulation pool using property")

                if len(mode) >= 2:
                    propertyPath = mode[1]
                    #Check if property path is valid is list of strings
                    if not isinstance(propertyPath,list):
                        self.logger.error("[VLMP] Property path must be a list of strings")
                        raise Exception("Property path must be a list of strings")
                    else:
                        for property in propertyPath:
                            if not isinstance(property,str):
                                self.logger.error("[VLMP] Property path must be a list of strings")
                                raise Exception("Property path must be a list of strings")
                else:
                    self.logger.error("[VLMP] No property path specified")
                    raise Exception("No scoring property specified")

                #Distribute the simulation pool
                self.simulationSets = self.__distributeSimulationPoolByProperty(propertyPath)


        #Check all the simulations have been distributed.
        #simulationSets is a list of lists which contains the names of the simulations
        #in the simulation pool

        simulationNames       = list(self.simulations.keys())
        simulationNamesInSets = [s for st in self.simulationSets for s in st]

        #Both must be equal
        if sorted(simulationNames) != sorted(simulationNamesInSets):
            self.logger.error("[VLMP] Simulation distribution failed")
            raise Exception("Simulation distribution failed")

    def setUpSimulation(self, sessionName):
        self.logger.debug("[VLMP] Setting up simulation")

        if len(self.simulationSets) == 0:
            self.logger.error("[VLMP] Simulation pool not distributed")
            raise Exception("Simulation pool not distributed")

        ################################################

        #Create folder named sessionName
        if not os.path.exists(sessionName):
            os.makedirs(sessionName)

        ################################################

        #Create folder sessionName/simulationSets
        if not os.path.exists(os.path.join(sessionName,"simulationSets")):
            os.makedirs(os.path.join(sessionName,"simulationSets"))

        #Create folder sessionName/results
        if not os.path.exists(os.path.join(sessionName,"results")):
            os.makedirs(os.path.join(sessionName,"results"))

        VLMPsession = {"name":sessionName}
        VLMPsession["simulations"] = []
        VLMPsession["simulationSets"] = []
        for simSetIndex,simSet in enumerate(self.simulationSets):
            #Create folder sessionName/simulationSets/simulationSet_i
            simulationSetName   = f"simulationSet_{simSetIndex}"
            simulationSetFolder = os.path.join(sessionName,"simulationSets",simulationSetName)

            if not os.path.exists(simulationSetFolder):
                os.makedirs(simulationSetFolder)

            #For each simulation in the simulation set.
            #Create a folder sessionName/simulationSets/simulationSetName/simulationName/
            for simName in simSet:

                simulationFolder       = os.path.join(sessionName,"simulationSets",simulationSetName,simName)
                simulationResultFolder = os.path.join(sessionName,"results",simName)

                if not os.path.exists(simulationFolder):
                    os.makedirs(simulationFolder)

                if not os.path.islink(simulationResultFolder):
                    os.symlink(os.path.relpath(simulationFolder,
                                               "/".join(simulationResultFolder.split("/")[:-1])),
                               simulationResultFolder)

                #Update output files for each simulation in simSet
                sim = self.simulations[simName]

                #Write simulation file into results folder
                sim.write(os.path.join(simulationFolder,"simulation.json"))

                #Relative path to the simulation folder
                relativePath = os.path.relpath(simulationFolder,simulationSetFolder)

                VLMPsession["simulations"].append([simName,
                                                   os.path.join(*simulationFolder.split("/")[1:]),
                                                   os.path.join(*simulationResultFolder.split("/")[1:]),
                                                   self.simulationsInfo[simName]])

                #Updating file path
                def getValuesAndPaths(d, key, path=None):
                    """
                    Recursively search a nested dictionary
                    for all values associated with a given key,
                    along with the path to each value.
                    """
                    if path is None:
                        path = ()

                    values = []
                    for k, v in d.items():
                        new_path = path + (k,)
                        if k == key:
                            values.append((v, new_path))
                        elif isinstance(v, dict):
                            values.extend(getValuesAndPaths(v, key, new_path))

                    return values

                outputFilePaths = getValuesAndPaths(sim,"outputFilePath")
                for fName,fSimPath in outputFilePaths:
                    sim.setValue(fSimPath,os.path.join(relativePath,fName))

            ################################################
            #Aggregate simulations in simulation sets

            self.logger.debug(f"[VLMP] Aggregating simulations in simulation set {simSetIndex}")
            aggregatedSimulation = mergeSimulationsSet([self.simulations[simName] for simName in simSet])

            #Aggregated simulation is ready
            ################################################

            ################################################
            #Write aggregated simulation to file

            aggregatedSimulation.write(os.path.join(simulationSetFolder,f"simulationSet_{simSetIndex}.json"))

            #Relative path to the simulation folder
            relativePath = os.path.relpath(simulationSetFolder,sessionName)
            VLMPsession["simulationSets"].append([simulationSetName,
                                                  f"{relativePath}",
                                                  f"simulationSet_{simSetIndex}.json",
                                                  simSet.copy()])

        with open(os.path.join(sessionName,"VLMPsession.json"),"w") as simSetsFile:
            #Write simulation sets file using jsbeautifier
            simSetsFile.write(jsbeautifier.beautify(json.dumps(VLMPsession)))

        self.logger.debug("[VLMP] Simulation set up finished")
