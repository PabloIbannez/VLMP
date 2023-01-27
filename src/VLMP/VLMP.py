import logging

import VLMP.models as mdls

class VLMP:

    def __init__(self):
        self.logger = logging.getLogger("VLMP")

        self.logger.info("[VLMP] Starting VLMP")

    def loadSimulationPool(self,simulationPool:dict):

        self.simulations = []
        for simulationInfo in simulationPool:
            #Process each simulation info to create a simulation object
            models = {}
            for modelInfo in simulationInfo["modelCreation"]:
                modelType = modelInfo.get("type")

                #Check if the model type is present
                if modelType is None:
                    self.logger.error("[VLMP] Model type not specified")
                    raise ValueError("Model type not specified")

                #Read model name, if not present use the model type
                modelName = modelInfo.get("name",modelType)

                #Check if a model with the same name already exists
                if modelName in models.keys():
                    self.logger.error("[VLMP] Model name \"%s\" already exists",modelName)
                    raise ValueError("Model name already exists")

                #Create the model
                self.logger.debug("[VLMP] Creating model \"%s\" of type \"%s\"",modelName,modelType)
                model     = eval("mdls." + modelType)(**(modelInfo["parameters"]))

                #Store the model
                models[modelName] = model
            #Model creation finished


            #Process model operations
            addedOperations = []
            if "modelOperations" in simulationInfo.keys():
                for modelOperation in simulationInfo["modelOperations"]:
                    operationType = modelOperation.get("type")

                    #Check if the operation type is present
                    if operationType is None:
                        self.logger.error("[VLMP] Operation type not specified")
                        raise ValueError("Operation type not specified")

                    #Read operation name, if not present use the operation type
                    operationName = modelOperation.get("name",operationType)

                    #Check if a operation with the same name already exists.
                    #If not, add it to the list of added operations
                    if operationName in addedOperations:
                        self.logger.error("[VLMP] Operation \"%s\" has been applied before",operationName)
                    else:
                        addedOperations.append(operationName)

                    #Check if the operation is applied in a subset of models
                    if "applyOnModel" in modelOperation.keys():
                        modelsToApply = modelOperation["applyOnModel"]
                        #If is not a list, make it a list
                        if not isinstance(modelsToApply,list):
                            modelsToApply = [modelsToApply]
                    #Else, apply the operation to all models
                    else:
                        modelsToApply = models.keys()

                    for modelName in modelsToApply:
                        #Check if the model exists
                        if modelName not in models.keys():
                            self.logger.error("[VLMP] Model \"%s\" does not exist",modelName)
                            raise ValueError("Model does not exist")

                        #Apply the operation
                        self.logger.debug("[VLMP] Applying operation \"%s\" on model \"%s\"",operationName,modelName)
                        #models[modelName].applyOperation(operationType,**(modelOperation["parameters"]))
            #Model operations finished


            #Process model extensions
            #TODO
            #Model extensions finished

            #Merge all models into a single simulation
            self.logger.debug("[VLMP] Merging models into a single simulation")

            sim = None
            for modelName in models.keys():
                mdl = models[modelName]
                if sim is None:
                    sim  = mdl.getSimulation()
                else:
                    sim.append(mdl.getSimulation(),mode="mdl")
            #Simulation creation finished

            #Store the simulation
            self.simulations.append(sim)

    def splitSimulationPool(self,nSets:int,mode:str="balanced",weighing:str="numberOfParticles"):

        if nSets < 1:
            self.logger.error("[VLMP] Number of sets must be greater than 0")
            raise ValueError("Number of sets must be greater than 0")

        if nSets > len(self.simulations):
            self.logger.error("[VLMP] Number of sets must be less than the number of simulations")
            raise ValueError("Number of sets must be less than the number of simulations")

        availableModes = ["balanced"]

        if mode not in availableModes:
            self.logger.error("[VLMP] Splitting mode \"%s\" not available",mode)
            raise ValueError("Splitting mode not available")

        availableWeighing = ["numberOfParticles"]

        if weighing not in availableWeighing:
            self.logger.error("[VLMP] Weighing mode \"%s\" not available",weighing)
            raise ValueError("Weighing mode not available")

        weights = []
        if weighing == "numberOfParticles":
            for sim in self.simulations:
                weights.append(sim.getNumberOfParticles())

        if mode == "balanced":
            #Distribution of simulations in sets in a balanced way according to weights

            #Sort simulations by weights
            sortedSimulations = [x for _,x in sorted(zip(weights,self.simulations),key=lambda pair: pair[0],reverse=True)]

            #Distribute simulations in sets
            sets = [[] for i in range(nSets)]
            for i in range(len(sortedSimulations)):
                sets[i%nSets].append(sortedSimulations[i])

            #Store sets
            self.simulations = sets

        self.logger.info("[VLMP] Simulation pool splitted into %d sets, mode \"%s\", weighing \"%s\"",nSets,mode,weighing)

        #Plot the final weight for each set
        for i in range(nSets):
            self.logger.debug("[VLMP] Set %d weight: %f",i,sum([set_.getNumberOfParticles() for set_ in self.simulations[i]]))

    def aggregateSimulationPool(self):
        #If the simulation pool is not a list of lists, make it a list of lists
        if not isinstance(self.simulations[0],list):
            self.simulations = [self.simulations]

        #Generate a simulation merging all simulations in each set
        for i in range(len(self.simulations)):
            self.logger.debug("[VLMP] Generating simulation set %d",i)
            sim = None
            for j in range(len(self.simulations[i])):
                if sim is None:
                    sim = self.simulations[i][j]
                else:
                    sim.append(self.simulations[i][j],mode="sim")
            self.simulations[i] = sim

    def writeSimulationPool(self,fileName:str):
        #If simulation is not a list, make it a list
        if not isinstance(self.simulations,list):
            self.simulations = [self.simulations]

        #Write each simulation set
        for i in range(len(self.simulations)):
            self.logger.debug("[VLMP] Writing simulation set %d",i)
            self.simulations[i].write(fileName + "_" + str(i) + ".json")




