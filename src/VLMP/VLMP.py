import os
import logging

from tqdm import tqdm

import json
import jsbeautifier

from collections import OrderedDict

from . import DEBUG_MODE
from .utils import getValuesAndPaths

import VLMP.components.system          as _system
import VLMP.components.units           as _units
import VLMP.components.globals         as _globals
import VLMP.components.models          as _models
import VLMP.components.modelOperations as _modelOperations
import VLMP.components.modelExtensions as _modelExtensions
import VLMP.components.integrators     as _integrators
import VLMP.components.simulationSteps as _simulationSteps

class VLMP:

    #Distribute functions

    def __distributeSimulationPoolByMaxNumberOfParticles(self,maxNumberOfParticles):

        simulationSets = []

        currentSet     = []
        currentSetSize = 0

        for simIndex,sim in enumerate(self.simulations):
            if currentSetSize + sim.getNumberOfParticles() > maxNumberOfParticles:
                if len(currentSet) > 0:
                    simulationSets.append(currentSet)
                currentSet     = []
                currentSetSize = 0

            currentSet.append(simIndex)
            currentSetSize += sim.getNumberOfParticles()

        if len(currentSet) > 0:
            simulationSets.append(currentSet)

        #Print the number of simulations and the number of particles in each set
        for i in range(len(simulationSets)):
            self.logger.debug("[VLMP] Simulation set %d has %d simulations and %d particles (max %d)",
                              i,len(simulationSets[i]),
                              sum([self.simulations[simIndex].getNumberOfParticles() for simIndex in simulationSets[i]]),
                              maxNumberOfParticles)

        return simulationSets

    def __distributeSimulationPoolByProperty(self,propertyPath):

        simulationSets = {}

        for simIndex,sim in enumerate(self.simulations):
            #Get the property value
            try:
                propertyValue = sim[propertyPath[0]]
                for i in range(1,len(propertyPath)):
                    propertyValue = propertyValue[propertyPath[i]]
            except:
                self.logger.error("[VLMP] Property \"%s\" not found in simulation",propertyPath)
                raise ValueError("Property not found in simulation")

            if propertyValue not in simulationSets.keys():
                simulationSets[propertyValue] = []

            simulationSets[propertyValue].append(simIndex)

        #Print the number of simulations and the property value in each set
        for propertyValue in simulationSets.keys():
            self.logger.debug("[VLMP] Simulation set \"%s\" has %d simulations",
                              propertyValue,len(simulationSets[propertyValue]))

        return simulationSets.values()

    ########################################

    def __checkComponent(self,component,componentClass,simulationBuffer):
        componentType = component.get("type",None)

        if componentType is None:
            self.logger.error(f"[VLMP] Error processing \"{componentClass}\" component ({component}), \"type\" property not found")
            raise ValueError("Component type not specified")
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
            raise ValueError("Component already loaded")

        return componentType,componentName,componentParameters

    ########################################

    def __init__(self):
        self.logger = logging.getLogger("VLMP")

        self.logger.info("[VLMP] Starting VLMP")

        self.simulations    = []
        self.simulationSets = []


    def loadSimulationPool(self,simulationPool:dict):

        for simulationInfo in simulationPool:

            simulationBuffer = OrderedDict()

            ############## SYSTEM ##############

            #Check if system section is present
            if "system" not in simulationInfo.keys():
                self.logger.error("[VLMP] System section not found")
                raise ValueError("System section not found")
            else:

                #Check there is one (and only one) system component of type "simulationName"
                simNameComponents = [component for component in simulationInfo["system"] if component["type"] == "simulationName"]
                if len(simNameComponents) == 0:
                    self.logger.error("[VLMP] Simulation name not specified")
                    raise ValueError("Simulation name not specified")
                elif len(simNameComponents) > 1:
                    self.logger.error("[VLMP] More than one simulation name specified")
                    raise ValueError("More than one simulation name specified")

                for system in simulationInfo["system"]:

                    typ, name, param = self.__checkComponent(system,"system",simulationBuffer)
                    self.logger.debug(f"[VLMP] Adding system \"{name}\"")

                    #Check if typ is part of "_system"
                    if typ not in dir(_system):
                        self.logger.error(f"[VLMP] System \"{typ}\" not found")
                        raise ValueError("System not found")

                    try:
                        system = eval(f"_system.{typ}")(name=name,**param)
                        simulationBuffer["system_"+name] = system
                    except:
                        self.logger.error(f"[VLMP] Error loading system \"{name}\" ({typ})")
                        raise ValueError("Error loading system")


            ############## UNITS ##############

            #Check if units section is present
            if "units" not in simulationInfo.keys():
                self.logger.error("[VLMP] Units section not found")
                raise ValueError("Units section not found")
            else:
                #Only one unit system can be specified
                if len(simulationInfo["units"]) > 1:
                    self.logger.error("[VLMP] Only one unit system can be specified")
                    raise ValueError("Only one unit system can be specified")

                typ, name, param = self.__checkComponent(simulationInfo["units"][0],"units",simulationBuffer)
                self.logger.debug(f"[VLMP] Selected units: \"{name}\" ({typ})")

                #Check if typ is part of "_units"
                if typ not in dir(_units):
                    self.logger.error(f"[VLMP] Units \"{typ}\" not found")
                    raise ValueError("Units not found")

                try:
                    units = eval(f"_units.{typ}")(name=name,**param)
                    simulationBuffer["units_"+name] = units
                except:
                    self.logger.error(f"[VLMP] Error loading units \"{name}\" ({typ})")
                    raise ValueError("Error loading units")

            ############## GLOBAL ##############

            #Check if global section is present
            if "global" not in simulationInfo.keys():
                self.logger.error("[VLMP] Global section not found")
                raise ValueError("Global section not found")
            else:

                for global_ in simulationInfo["global"]:

                    typ, name, param = self.__checkComponent(global_,"global",simulationBuffer)
                    self.logger.debug(f"[VLMP] Adding global \"{name}\"")

                    #Check if typ is part of "_globals"
                    if typ not in dir(_globals):
                        self.logger.error(f"[VLMP] Global \"{typ}\" not found")
                        raise ValueError("Global not found")

                    try:
                        simulationBuffer["global_"+name] = eval("_globals." + typ)(name=name,units=units,**(param))
                    except:
                        self.logger.error(f"[VLMP] Error loading global \"{name}\"")
                        raise ValueError("Error loading global")

            ############### MODEL ###############
            #Create a list with the added models. This is used afterwards to apply model operations
            #and add model extensions to specific models
            models = []
            #Check if model section is present
            if "model" not in simulationInfo.keys():
                self.logger.error("[VLMP] Model section not found")
                raise ValueError("Model section not found")
            else:

                for model in simulationInfo["model"]:

                    typ, name, param = self.__checkComponent(model,"model",simulationBuffer)
                    self.logger.debug(f"[VLMP] Adding model \"{name}\"")

                    #Check if typ is part of "_models"
                    if typ not in dir(_models):
                        self.logger.error(f"[VLMP] Model \"{typ}\" not found")
                        raise ValueError("Model not found")

                    try:
                        simulationBuffer["model_"+name] = eval("_models." + typ)(name=name,units=units,**(param))
                        models.append("model_"+name)
                    except:
                        self.logger.error(f"[VLMP] Error loading model \"{name}\"")
                        raise ValueError("Error loading model")

            #Set idOffset for each model
            idOffset = 0
            for mdl in models:
                simulationBuffer[mdl].setIdOffset(idOffset)
                ids = simulationBuffer[mdl].getIds()
                if len(ids) != 0:
                    idOffset += max(ids) + 1



            ############### MODEL OPERATIONS ###############

            #Check if model operations section is present
            if "modelOperations" not in simulationInfo.keys():
                self.logger.warning("[VLMP] Model operations section not found, skipping")
            else:

                appliedOperations = []
                for modelOperation in simulationInfo["modelOperations"]:

                    typ, name, param = self.__checkComponent(modelOperation,"modelOperations",simulationBuffer)
                    self.logger.debug(f"[VLMP] Adding model operation \"{name}\"")

                    if "modelOperations_"+name in appliedOperations:
                        self.logger.error(f"[VLMP] Model operation \"{name}\" already applied")
                        raise ValueError("Model operation already applied")

                    #Check if typ is part of "__modelOperation__"
                    if typ not in dir(_modelOperations):
                        self.logger.error(f"[VLMP] Model operation \"{name}\" not found")
                        raise ValueError("Model operation not found")

                    try:
                        operation = eval("_modelOperations." + typ)(name   = name,
                                                                    units  = units,
                                                                    models = [simulationBuffer[model] for model in models],
                                                                    **(param))
                        appliedOperations.append("modelOperations_"+name)

                    except:
                        self.logger.error(f"[VLMP] Error loading model operation \"{name}\"")
                        raise ValueError("Error loading model operation")

            ############### MODEL EXTENSIONS ###############

            #Check if model extensions section is present
            if "modelExtensions" not in simulationInfo.keys():
                self.logger.warning("[VLMP] Model extensions section not found, skipping")
            else:

                for modelExtension in simulationInfo["modelExtensions"]:

                    typ, name, param = self.__checkComponent(modelExtension,"modelExtensions",simulationBuffer)
                    self.logger.debug(f"[VLMP] Adding model extension \"{name}\"")

                    #Check if typ is part of "_modelExtensions"
                    if typ not in dir(_modelExtensions):
                        self.logger.error(f"[VLMP] Model extension \"{name}\" not found")
                        raise ValueError("Model extension not found")

                    try:
                        simulationBuffer["modelExtensions_"+name] = eval("_modelExtensions." + typ)(name   = name,
                                                                                                    units  = units,
                                                                                                    models = [simulationBuffer[model] for model in models],
                                                                                                    **(param))

                    except:
                        self.logger.error(f"[VLMP] Error loading model extension \"{name}\"")
                        raise ValueError("Error loading model extension")

            ############## INTEGRATOR ##############

            #Check if integrator section is present
            if "integrator" not in simulationInfo.keys():
                self.logger.error("[VLMP] Integrator section not found")
                raise ValueError("Integrator section not found")
            else:

                for integrator in simulationInfo["integrator"]:

                    typ, name, param = self.__checkComponent(integrator,"integrator",simulationBuffer)
                    self.logger.debug(f"[VLMP] Adding integrator \"{name}\"")

                    #Check if typ is part of "_integrators"
                    if typ not in dir(_integrators):
                        self.logger.error(f"[VLMP] Integrator \"{typ}\" not found")
                        raise ValueError("Integrator not found")

                    try:
                        simulationBuffer["integrator_"+name] = eval("_integrators." + typ)(name=name,units=units,**(param))
                    except:
                        self.logger.error(f"[VLMP] Error loading integrator \"{name}\"")
                        raise ValueError("Error loading integrator")

            ############### SIMULATION STEPS ###############

            #Check if simulation steps section is present
            if "simulationSteps" not in simulationInfo.keys():
                self.logger.warning("[VLMP] Simulation steps section not found, skipping")
            else:

                for simulationStep in simulationInfo["simulationSteps"]:

                    typ, name, param = self.__checkComponent(simulationStep,"simulationSteps",simulationBuffer)
                    self.logger.debug(f"[VLMP] Adding simulation step \"{name}\"")

                    #Check if typ is part of "_simulationSteps"
                    if typ not in dir(_simulationSteps):
                        self.logger.error(f"[VLMP] Simulation step \"{name}\" not found")
                        raise ValueError("Simulation step not found")

                    try:
                        simulationBuffer["simulationSteps_"+name] = eval("_simulationSteps." + typ)(name=name,
                                                                                                    units=units,
                                                                                                    **(param))
                    except:
                        self.logger.error(f"[VLMP] Error loading simulation step \"{name}\"")
                        raise ValueError("Error loading simulation step")

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

            #Check name is unique
            simulationName = sim["system"]["parameters"]["name"]

            #Check if other simulation with the same name has been already created
            if simulationName in [s["system"]["parameters"]["name"] for s in self.simulations]:
                self.logger.error(f"[VLMP] Simulation with name \"{simulationName}\" already exists")
                raise ValueError("Simulation already exists")

            ###############################################

            #Store the simulation
            self.simulations.append(sim)

    def distributeSimulationPool(self,*mode):

        availableModes = ["none","one","upperLimit","property"]

        #Check at least one simulations has been loaded
        if len(self.simulations) == 0:
            self.logger.error("[VLMP] No simulations loaded")
            raise ValueError("No simulations loaded")

        #Check mode
        if len(mode) == 0:
            self.logger.warning("[VLMP] No mode specified, using \"none\"")
            modeName = "none"
        else:
            modeName = mode[0]
            self.logger.debug(f"[VLMP] Distributing simulation pool using mode \"{modeName}\"")

        if modeName not in availableModes:
            self.logger.error("[VLMP] Distribute mode \"%s\" not available, available modes are: %s",modeName,availableModes)
            raise ValueError("Distribute mode not available")
        else:
            #Switch to the selected mode
            if  modeName == "none":
                self.simulationSets = [[i] for i in range(len(self.simulations))]
            elif modeName == "one":
                self.simulationSets = list(range(len(self.simulations)))
            elif modeName == "upperLimit":
                self.logger.debug("[VLMP] Distributing simulation pool using upper limit")
                availableScoringProperties = ["numberOfParticles"]

                if len(mode) >= 2:
                    scoringPropertyName = mode[1]
                else:
                    self.logger.error("[VLMP] No scoring property specified")
                    raise ValueError("No scoring property specified")

                if scoringPropertyName not in availableScoringProperties:
                    self.logger.error("[VLMP] Scoring property \"%s\" not available, available properties are: %s",
                                      scoringPropertyName,availableScoringProperties)
                    raise ValueError("Scoring property not available")
                else:
                    #Switch to the selected scoring property
                    if scoringPropertyName == "numberOfParticles":
                        self.logger.debug("[VLMP] Distributing simulation pool using number of particles")
                        if len(mode) >= 3:
                            maxNumberOfParticles = mode[2]
                        else:
                            self.logger.error("[VLMP] No particle limit specified")
                            raise ValueError("No upper limit specified")

                        #Distribute the simulation pool
                        self.simulationSets = self.__distributeSimulationPoolByMaxNumberOfParticles(maxNumberOfParticles)
                    #Scoring property switch finished

            elif modeName == "property":
                self.logger.debug("[VLMP] Distributing simulation pool using property")

                if len(mode) >= 2:
                    propertyPath = mode[1]
                    #Check if property path is valid is list of strings
                    if not isinstance(propertyPath,list):
                        self.logger.error("[VLMP] Property path must be a list of strings")
                        raise ValueError("Property path must be a list of strings")
                    else:
                        for property in propertyPath:
                            if not isinstance(property,str):
                                self.logger.error("[VLMP] Property path must be a list of strings")
                                raise ValueError("Property path must be a list of strings")
                else:
                    self.logger.error("[VLMP] No property path specified")
                    raise ValueError("No scoring property specified")

                #Distribute the simulation pool
                self.simulationSets = self.__distributeSimulationPoolByProperty(propertyPath)

        #Check all the simulations have been distributed.
        #simulationSets is a list of lists which contains the indexes of the simulations
        #in the simulation pool

        simulationIndexes       = list(range(len(self.simulations)))
        simulationIndexesInSets = [ i for s in self.simulationSets for i in s]

        #Both must be equal
        if simulationIndexes != simulationIndexesInSets:
            self.logger.error("[VLMP] Simulation distribution failed")
            raise ValueError("Simulation distribution failed")

    def aggregateSimulationSets(self):

        #Generate a simulation merging all simulations in each set
        for i in range(len(self.simulations)):
            self.logger.debug("[VLMP] Generating simulation set %d",i)

    def setUpSimulation(self, sessionName):
        self.logger.debug("[VLMP] Setting up simulation")

        if len(self.simulationSets) == 0:
            self.logger.error("[VLMP] Simulation pool not distributed")
            raise ValueError("Simulation pool not distributed")

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

            #For each simulation in the simulation set. Create a folder sessionName/simulationSets/simulationSetName/simulationName/
            for simIndex in simSet:
                simulationName         = self.simulations[simIndex]["system"]["parameters"]["name"]

                simulationFolder       = os.path.join(sessionName,"simulationSets",simulationSetName,simulationName)
                simulationResultFolder = os.path.join(sessionName,"results",simulationName)

                if not os.path.exists(simulationFolder):
                    os.makedirs(simulationFolder)

                if not os.path.exists(simulationResultFolder):
                    os.makedirs(simulationResultFolder)

                #Update output files for each simulation in simSet
                sim = self.simulations[simIndex]

                #Relative path to the simulation folder
                relativePath = os.path.relpath(simulationFolder,simulationSetFolder)

                VLMPsession["simulations"].append([simulationName,
                                                   os.path.join(*simulationFolder.split("/")[1:]),
                                                   os.path.join(*simulationResultFolder.split("/")[1:])])

                #Updating file path
                outputFilePaths = getValuesAndPaths(sim,"outputFilePath")
                for fName,fSimPath in outputFilePaths:
                    sim.setValue(fSimPath,os.path.join(relativePath,fName))

            ################################################
            #Aggregate simulations in simulation sets

            #We assume that simulationId is 0 (not set) for each independent simulation
            #Check it
            for simIndex in simSet:
                structureLabels = self.simulations[simIndex]["topology"]["structure"]["labels"]
                if "simulationId" in structureLabels:
                    self.logger.error("[VLMP] SimulationId already set, for a single simulation. Cannot aggregate simulations")
                    raise ValueError("SimulationId already set")

            #Update simulationsStep for each simulation in the simulation set
            #This ensures the simulation step is applied over particles for the
            #same simulationId
            for simIndex in simSet:

                #simIndex is equivalent to simulationId

                sim = self.simulations[simIndex]
                if len(simSet) > 1:
                    groupDefinitionRequired = False
                    if "simulationStep" in sim.keys():
                        keysToRename = []
                        for simStep in sim["simulationStep"].keys():
                            simStepType = sim["simulationStep"][simStep]["type"][0]
                            if "UtilsStep" not in simStepType: #Ignore UtilsStep types
                                sim["simulationStep"][simStep]["parameters"]["group"] = f"simId_{simIndex}"
                                keysToRename.append(simStep)
                                groupDefinitionRequired = True

                        for k in keysToRename:
                            sim["simulationStep"][k+f"_{simIndex}"] = sim["simulationStep"].pop(k)

                    if groupDefinitionRequired:
                        if "groups_simulationId" not in sim["simulationStep"].keys():
                            sim["simulationStep"]["groups_simulationId"] = {
                                "type": ["Groups","GroupsList"],
                                "parameters": {},
                                "labels":["name","type","selection"],
                                "data":[
                                    [f"simId_{simIndex}","SimIds",[0]],
                                ]
                            }
                        else:
                            self.logger.error("[VLMP] groups_simulationId already defined")
                            raise ValueError("groups_simulationId already defined")
                else:
                    #Only one simulation in the set, do nothing
                    pass

            #Perform aggregation
            self.logger.info("[VLMP] Aggregating simulations in simulation set %d",simSetIndex)

            #Store names of simulations in simulation set
            simInSimSetNames = [self.simulations[simIndex]["system"]["parameters"]["name"] for simIndex in simSet]

            aggregatedSimulation = None
            for simIndex in tqdm(simSet):
                if aggregatedSimulation is None:
                    aggregatedSimulation = self.simulations[simIndex]
                else:
                    aggregatedSimulation.append(self.simulations[simIndex],mode="simulationId")

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
                                                  simInSimSetNames])

        with open(os.path.join(sessionName,"VLMPsession.json"),"w") as simSetsFile:
            #Write simulation sets file using jsbeautifier
            simSetsFile.write(jsbeautifier.beautify(json.dumps(VLMPsession)))

        self.logger.debug("[VLMP] Simulation set up finished")




