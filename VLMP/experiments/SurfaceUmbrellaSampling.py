import VLMP

import VLMP.components.units as _units

import os

import numpy as np
import matplotlib.pyplot as plt

import json
import jsbeautifier

import copy
import logging

class SurfaceUmbrellaSampling(VLMP.VLMP):

    def __init__(self,parameters):
        super().__init__()

        requiredParameters = ["nWindows","windowsStartPosition","windowsEndPosition","K","Ksteps"]

        self.logger.info("[SurfaceUmbrellaSampling] Initializing ...")

        #Load umbrella parameters

        for parameter in requiredParameters:
            if parameter not in parameters["umbrella"]:
                self.logger.error("[SurfaceUmbrellaSampling] Required parameter %s not found!" % parameter)
                raise Exception("Required parameter not found!")

        self.nWindows        = parameters["umbrella"]["nWindows"]

        self.windowsStartPosition    = parameters["umbrella"]["windowsStartPosition"]
        self.windowsEndPosition      = parameters["umbrella"]["windowsEndPosition"]

        self.windowsSize             = (self.windowsEndPosition - self.windowsStartPosition)/(self.nWindows-1)

        self.K                       = parameters["umbrella"]["K"]
        self.Ksteps                  = parameters["umbrella"]["Ksteps"]
        if type(self.K) is not list:
            self.K = [self.K]

        if type(self.Ksteps) is not list:
            self.Ksteps = [self.Ksteps]

        if len(self.K) != len(self.Ksteps):
            self.logger.error("[SurfaceUmbrellaSampling] K and Ksteps must have the same length!")
            raise Exception("K and Ksteps must have the same length!")

        #Measurements
        self.measurementsIntervalStep = parameters["umbrella"]["measurementsIntervalStep"]

        self.logger.info((f"[SurfaceUmbrellaSampling] Number of windows: {self.nWindows}, "
                          f"windows start position: {self.windowsStartPosition}, "
                          f"windows end position: {self.windowsEndPosition}, "
                          f"windows size: {round(self.windowsSize,2)}",
                          f"measurements interval step: {self.measurementsIntervalStep}"))

        self.windowPositions = []
        for i in range(self.nWindows):
            self.windowPositions.append(self.windowsStartPosition + i*self.windowsSize)

        #Load simulation parameters

        requiredSimulationParameters = ["units","types","temperature","box","models","selection","integrator"]
        for parameter in requiredSimulationParameters:
            if parameter not in parameters["simulation"]:
                self.logger.error("[SurfaceUmbrellaSampling] Required parameter %s not found!" % parameter)
                raise Exception("Required parameter not found!")

        self.units  = parameters["simulation"]["units"]
        self.types  = parameters["simulation"]["types"]

        self.temperature = parameters["simulation"]["temperature"]
        #Check if the temperature is a float
        if not isinstance(self.temperature,float):
            raise Exception("The temperature must be a float")

        self.box         = parameters["simulation"]["box"]
        #Check box is a list of 3 floats
        if not isinstance(self.box,list):
            raise Exception("The box must be a list of 3 floats")
        if len(self.box) != 3:
            raise Exception("The box must be a list of 3 floats")
        for i in self.box:
            if not isinstance(i,float):
                raise Exception("The box must be a list of 3 floats")

        self.integrator = parameters["simulation"]["integrator"]
        self.integrator["parameters"]["integrationSteps"] = sum(self.Ksteps)

        self.models     = parameters["simulation"]["models"]
        self.selection  = parameters["simulation"]["selection"]

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

        self.umbrellaInfo = {}

        ########################################

        unitsComponent = eval(f"_units.{self.units}")(name="units")

        ########################################

        simulationPool = []

        mdlNames = []
        for mdl in self.models:
            if "name" not in mdl.keys():
                self.logger.error("[SurfaceUmbrellaSampling] Model name not found! (Model: %s)" % mdl)
                raise Exception("Model name not found")

            if mdl["name"] in mdlNames:
                self.logger.error("[SurfaceUmbrellaSampling] Model with the same name found! (Model: %s)" % mdl)
                raise Exception("Model with the same name found")
            else:
                mdlNames.append(mdl["name"])

        for mdl in self.models:
            self.umbrellaInfo[mdl["name"]] = {}
            self.umbrellaInfo[mdl["name"]]["kT"] = unitsComponent.getConstant("KBOLTZ")*self.temperature
            self.umbrellaInfo[mdl["name"]]["K"]  = self.K[-1]
            self.umbrellaInfo[mdl["name"]]["centers"] = {}
            for i,center in enumerate(self.windowPositions):

                sim = {"system":[{"type":"simulationName","parameters":{"simulationName":mdl["name"]+"_"+str(i)}}],
                       "units":[{"type":self.units}],
                       "types":[{"type":self.types}],
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
                        if ik != len(self.Ksteps)-1:
                            sim["modelExtensions"][ik]["parameters"]["endStep"]   = stepsSum + steps
                        stepsSum += steps

                #Add measures
                measureStartStep = 0
                #Iterate over all Ksteps but the last one
                for ik,steps in enumerate(self.Ksteps[:-1]):
                    measureStartStep += steps

                centerOutputFilePath = f"constraint_{center}.dat"
                sim["simulationSteps"].append({"type":"centerOfMassMeasurement","parameters":{"outputFilePath":centerOutputFilePath,
                                                                                              "intervalStep":self.measurementsIntervalStep,
                                                                                              "startStep":measureStartStep,
                                                                                              "selection":{"expression":self.selection}}})

                self.umbrellaInfo[mdl["name"]]["centers"][center] = "results/{}/{}".format(mdl["name"]+"_"+str(i),centerOutputFilePath)

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

                simulationPool.append(sim.copy())

        self.loadSimulationPool(copy.deepcopy(simulationPool))

    def setUpSimulation(self, sessionName):
        super().setUpSimulation(sessionName)

        #Write umbrella info
        with open(os.path.join(sessionName,"surfaceUmbrella.json"),"w") as f:
            f.write(jsbeautifier.beautify(json.dumps(self.umbrellaInfo)))

class AnalysisSurfaceUmbrellaSampling:

    def __computePotential(self,centers,data,beta,K,outputFolderPath):

        outputPlot      = os.path.join(outputFolderPath,"histogram.png")
        outputPotential = os.path.join(outputFolderPath,"potential.dat")

        #Check if histogram.png and potential.dat already exist
        if os.path.exists(outputPlot) and os.path.exists(outputPotential):
            self.logger.info("[AnalysisSurfaceUmbrellaSampling] Histogram and potential already computed")
            return True

        from WHAM import binless
        from WHAM.lib import potentials

        fig, (ax1, ax2) = plt.subplots(2,1)

        potMin = np.amin(np.array([np.amin(np.array(d)) for d in data]).flatten())
        potMax = np.amax(np.array([np.amin(np.array(d)) for d in data]).flatten())

        ######### HISTOGRAM ########

        cmap = plt.get_cmap('spring')
        ax1.set_prop_cycle(color=[cmap(1.*i/len(centers)) for i in range(len(centers))])

        for i,x_0 in enumerate(centers):
            traj = data[i]
            bins = 100
            ax1.hist(traj, bins=bins, alpha=0.8,density=True)

        ax1.set_xlabel("z")
        ax1.set_xlim(potMin, potMax)
        ax1.set_ylabel("Counts")

        ######### POTENTIAL ########

        x_it = []
        u_i  = []
        for i,x_0 in enumerate(centers):
            traj = data[i]
            x_it.append(traj)
            u_i.append(potentials.harmonic(K, x_0))

        #Check all traj in x_it have the same length
        if not all(len(x_it[0]) == len(x) for x in x_it):
            if self.ignoreDifferentLength:
                self.logger.error("[AnalysisSurfaceUmbrellaSampling] Not all trajectories have the same length. Ignoring ...")
                return False
            else:
                self.logger.warning("[AnalysisSurfaceUmbrellaSampling] Not all trajectories have the same length.")

        #Smamllest center -> potMin
        #Largest center  -> potMax
        #potMin = np.amin(centers)
        potMax = np.amax(centers)
        x_bin  = np.linspace(potMin,potMax,1001)

        calc_binless = binless.Calc1D()
        bF, _, _ = calc_binless.compute_betaF_profile(x_it, x_bin, u_i, beta=beta)

        bF = bF - np.min(bF)

        ax2.plot(x_bin, bF)

        ax2.set_xlabel("z")
        ax2.set_xlim(potMin, potMax)
        ax2.set_ylabel(r"Free energy ($k_B T$)")

        with open(outputPotential,"w") as fpot:
            for x,e in zip(x_bin, bF):
                fpot.write(f"{x} {e}\n")

        fig.set_size_inches(24, 17)
        fig.savefig(outputPlot, dpi=300)

        return True

    def __init__(self,
                 infoFilePath,
                 skip=0,
                 ignoreDifferentLength=True):

        self.logger = logging.getLogger("VLMP")

        with open(infoFilePath,"r") as f:
            self.info = json.load(f)
        #Path from current file to infoFilePath
        self.sessionPath = os.path.dirname(infoFilePath)

        self.skip = skip + 1
        self.ignoreDifferentLength = ignoreDifferentLength

        ########################################################

    def run(self):

        for mdlName in self.info.keys():

            self.logger.info(f"[AnalysisSurfaceUmbrellaSampling] Processing {mdlName}")

            kT   = self.info[mdlName]["kT"]
            beta = 1.0/kT

            K = self.info[mdlName]["K"]

            centers = []
            data    = []

            process = True
            for center,file in self.info[mdlName]["centers"].items():
                #Check if file exists
                if not os.path.isfile(os.path.join(self.sessionPath,file)):
                    self.logger.error(f"[AnalysisSurfaceUmbrellaSampling] Center file not found! (File: {file})")
                    process = False
                    break

                try:
                    centers.append(float(center))
                    data.append(np.loadtxt(os.path.join(self.sessionPath,file),skiprows=self.skip)[:,3])
                except:
                    self.logger.error(f"[AnalysisSurfaceUmbrellaSampling] Error loading file {file}")
                    process = False
                    break

            if not process:
                continue

            outputFolderPath = os.path.join(self.sessionPath,"results",mdlName+"_surfaceUmbrella")
            #Create output directory if it does not exist
            if not os.path.isdir(outputFolderPath):
                os.makedirs(outputFolderPath)

            if(self.__computePotential(centers,data,beta,K,outputFolderPath)):
                self.logger.info(f"[AnalysisSurfaceUmbrellaSampling] Results for model {mdlName} saved in {outputFolderPath}")
            else:
                self.logger.error(f"[AnalysisSurfaceUmbrellaSampling] Error while computing potential for model {mdlName}")



