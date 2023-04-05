import copy

import logging

class SurfaceUmbrellaSampling:

    def __init__(self,parameters):

        requiredParameters = ["nWindows","windowsStartPosition","windowsEndPosition","K","Ksteps"]

        self.logger = logging.getLogger("VLMP")

        self.logger.info("[SurfaceUmbrellaSampling] Initializing ...")

        #Load umbrella parameters

        for parameter in requiredParameters:
            if parameter not in parameters["umbrella"]:
                self.logger.error("[SurfaceUmbrellaSampling] Required parameter %s not found!" % parameter)
                raise Exception("Required parameter not found!")

        self.nWindows        = parameters["umbrella"].get("nWindows")

        self.windowsStartPosition    = parameters["umbrella"].get("windowsStartPosition")
        self.windowsEndPosition      = parameters["umbrella"].get("windowsEndPosition")

        self.windowsSize             = (self.windowsEndPosition - self.windowsStartPosition)/(self.nWindows-1)

        self.K                       = parameters["umbrella"].get("K")
        self.Ksteps                  = parameters["umbrella"].get("Ksteps")
        if type(self.K) is not list:
            self.K = [self.K]

        if type(self.Ksteps) is not list:
            self.Ksteps = [self.Ksteps]

        if len(self.K) != len(self.Ksteps):
            self.logger.error("[SurfaceUmbrellaSampling] K and Ksteps must have the same length!")
            raise Exception("K and Ksteps must have the same length!")

        self.logger.info((f"[SurfaceUmbrellaSampling] Number of windows: {self.nWindows}, "
                          f"windows start position: {self.windowsStartPosition}, "
                          f"windows end position: {self.windowsEndPosition}, "
                          f"windows size: {round(self.windowsSize,2)}"))

        self.windowPositions = []
        for i in range(self.nWindows):
            self.windowPositions.append(self.windowsStartPosition + i*self.windowsSize)

        #Load simulation parameters

        requiredSimulationParameters = ["units","temperature","box","models","selection","integrator"]
        for parameter in requiredSimulationParameters:
            if parameter not in parameters["simulation"]:
                self.logger.error("[SurfaceUmbrellaSampling] Required parameter %s not found!" % parameter)
                raise Exception("Required parameter not found!")

        self.units  = parameters["simulation"].get("units")

        self.temperature = parameters["simulation"].get("temperature")
        #Check if the temperature is a float
        if not isinstance(self.temperature,float):
            raise Exception("The temperature must be a float")

        self.box         = parameters["simulation"].get("box")
        #Check box is a list of 3 floats
        if not isinstance(self.box,list):
            raise TypeError("The box must be a list of 3 floats")
        if len(self.box) != 3:
            raise ValueError("The box must be a list of 3 floats")
        for i in self.box:
            if not isinstance(i,float):
                raise TypeError("The box must be a list of 3 floats")

        self.integrator = parameters["simulation"].get("integrator")
        self.integrator["parameters"]["integrationSteps"] = sum(self.Ksteps)

        self.models     = parameters["simulation"].get("models")
        self.selection  = parameters["simulation"].get("selection")

        self.backupIntervalStep = parameters["simulation"].get("backupIntervalStep",None)

        requiredOutputParameters = []
        for parameter in requiredOutputParameters:
            if parameter not in parameters["output"]:
                self.logger.error("[SurfaceUmbrellaSampling] Required parameter %s not found!" % parameter)
                raise Exception("Required parameter not found!")

        #Load output parameters

        #Info
        self.infoIntervalStep = parameters["output"].get("infoIntervalStep",None)

        #Save state
        self.saveStateIntervalStep   = parameters["output"].get("saveStateIntervalStep",None)
        self.saveStateOutputFilePath = parameters["output"].get("saveStateOutputFilePath",None)
        self.saveStateOutputFormat   = parameters["output"].get("saveStateOutputFormat",None)

        #If at least one of the save state parameters is specified, check all of them are specified
        self.saveState = False
        if self.saveStateIntervalStep is not None or self.saveStateOutputFilePath is not None or self.saveStateOutputFormat is not None:
            self.saveState = True
            if self.saveStateIntervalStep is None or self.saveStateOutputFilePath is None or self.saveStateOutputFormat is None:
                self.logger.error("[SurfaceUmbrellaSampling] All the save state parameters must be specified")
                raise Exception("All the save state parameters must be specified")

    def generateSimulationPool(self):

        self.simulationPool = []

        for i,mdl in enumerate(self.models):
            for j,center in enumerate(self.windowPositions):

                sim = {"system":[{"type":"simulationName","parameters":{"simulationName":mdl["type"]+"_"+str(i)+"_"+str(j)}}],
                       "units":[{"type":self.units}],
                       "global":[{"type":"NVT","parameters":{"box":self.box,"temperature":self.temperature}}],
                       "integrator":[self.integrator],
                       "model":[mdl],
                       "modelExtensions":[],
                       "simulationSteps":[]

                       }
                for ik,k in enumerate(self.K):
                    sim["modelExtensions"].append({"name":f"constraint_{ik}",
                                                   "type":"constraintCenterOfMassPosition",
                                                   "parameters":{"K":k,
                                                                 "r0":0.0,
                                                                 "position":[0.0,0.0,center],
                                                                 "selection":{"expression":self.selection}
                                                                }
                                                   })
                if len(self.K) > 1:
                    stepsSum = 0
                    for ik,steps in enumerate(self.Ksteps):
                        sim["modelExtensions"][ik]["parameters"]["startStep"] = stepsSum
                        sim["modelExtensions"][ik]["parameters"]["endStep"]   = stepsSum + steps
                        stepsSum += steps

                #Add backup
                if self.backupIntervalStep is not None:
                    sim["system"].append({"type":"backup","parameters":{"backupIntervalStep":self.backupIntervalStep}})

                #Add info
                if self.infoIntervalStep is not None:
                    sim["simulationSteps"].append({"type":"info","parameters":{"intervalStep":self.infoIntervalStep}})

                #Add save state
                if self.saveState:
                    sim["simulationSteps"].append({"type":"saveState","parameters":{"intervalStep":self.saveStateIntervalStep,
                                                                                   "outputFilePath":self.saveStateOutputFilePath,
                                                                                   "outputFormat":self.saveStateOutputFormat}})

                self.simulationPool.append(sim.copy())

        return copy.deepcopy(self.simulationPool)
