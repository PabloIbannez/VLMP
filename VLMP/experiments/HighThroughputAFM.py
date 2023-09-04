import VLMP

import VLMP.components.units as _units

import os

import numpy as np
import matplotlib.pyplot as plt

import json
import jsbeautifier

import copy
import logging

class HighThroughputAFM(VLMP.VLMP):

    def __init__(self,parameters):
        super().__init__()

        requiredParameters = ["K","Kxy",
                              "epsilon",
                              "sigma",
                              "tipVelocity",
                              "tipMass","tipRadius",
                              "initialTipSampleDistance",
                              "thermalizationSteps","indentationSteps"]

        self.logger.info("[AFM] Initializing ...")

        for parameter in requiredParameters:
            if parameter not in parameters["AFM"]:
                self.logger.error("[AFM] Required parameter %s not found!" % parameter)
                raise Exception("Required parameter not found!")

        self.K   = parameters["AFM"]["K"]
        self.Kxy = parameters["AFM"]["Kxy"]

        self.epsilon = parameters["AFM"]["epsilon"]
        self.sigma   = parameters["AFM"]["sigma"]

        self.tipVelocity     = parameters["AFM"]["tipVelocity"]

        self.tipMass   = parameters["AFM"]["tipMass"]
        self.tipRadius = parameters["AFM"]["tipRadius"]
        self.tipCharge = parameters["AFM"].get("tipCharge",0.0)

        self.initialTipSampleDistance = parameters["AFM"]["initialTipSampleDistance"]

        self.thermalizationSteps = parameters["AFM"]["thermalizationSteps"]
        self.indentationSteps    = parameters["AFM"]["indentationSteps"]

        self.fixSampleDuringThermalization = parameters["AFM"].get("fixSampleDuringThermalization",False)

        if "maxForce" in parameters.keys():
            self.maxForce             = parameters["maxForce"].get("force",None)
            self.maxForceIntervalStep = parameters["maxForce"].get("maxForceIntervalStep",None)

        if "surface" in parameters.keys():
            self.addSurface = True

            self.epsilonSurface  = parameters["surface"].get("epsilon",1.0)
            self.surfacePosition = parameters["surface"].get("position",0.0)

            self.absorptionHeight = parameters["surface"].get("absorptionHeight",None)

            if self.absorptionHeight is not None:
                self.absorptionK = parameters["surface"].get("absorptionK",None)
                if self.absorptionK is None:
                    self.logger.error("[AFM] Absorption height given but no absorption constant, K!")
                    raise Exception("Absorption K not found!")
                if self.absorptionHeight < self.surfacePosition:
                    self.logger.error("[AFM] Absorption height is below surface!")
                    raise Exception("Absorption height is below surface!")
        else:
            self.addSurface = False

        #Load simulation parameters

        requiredSimulationParameters = ["units","types","temperature","box","samples","integrator"]

        for parameter in requiredSimulationParameters:
            if parameter not in parameters["simulation"]:
                self.logger.error("[AFM] Required parameter %s not found!" % parameter)
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
        self.integrator["parameters"]["integrationSteps"] = self.thermalizationSteps + self.indentationSteps

        self.samples = parameters["simulation"]["samples"]
        #Check samples is dict of list
        if not isinstance(self.samples,dict):
            raise Exception("The samples must be a dict->dict->list")
        for key in self.samples:
            if not isinstance(self.samples[key],dict):
                raise Exception("The samples must be a dict->dict->list")
            for key2 in self.samples[key]:
                if not isinstance(self.samples[key][key2],list):
                    raise Exception("The samples must be a dict->dict->list")

        nSamples = len(self.samples)
        self.logger.info("[AFM] Number of samples: %d" % nSamples)

        self.backupIntervalStep = parameters["simulation"].get("backupIntervalStep",None)

        #Load output parameters
        requiredOutputParameters = []
        for parameter in requiredOutputParameters:
            if parameter not in parameters["output"]:
                self.logger.error("[AFM] Required parameter %s not found!" % parameter)
                raise Exception("Required parameter not found!")

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
                self.logger.error("[AFM] All the save state parameters must be specified")
                raise Exception("All the save state parameters must be specified")

        #Measurements
        self.afmMeasurementIntervalStep   = parameters["output"].get("afmMeasurementIntervalStep",None)
        self.afmMeasurementOutputFilePath = parameters["output"].get("afmMeasurementOutputFilePath","afm.dat")

        #Extend parameters


        allParameters = ["K", "Kxy",
                         "epsilon",
                         "sigma",
                         "tipVelocity",
                         "tipMass", "tipRadius", "tipCharge",
                         "initialTipSampleDistance",
                         "thermalizationSteps", "indentationSteps"]

        if self.addSurface:
            allParameters.extend(["epsilonSurface","surfacePosition"])
            if self.absorptionHeight is not None:
                allParameters.extend(["absorptionHeight","absorptionK"])

        for paramIndex in range(len(allParameters)):
            p = getattr(self,allParameters[paramIndex])
            if isinstance(p,list):
                #Check len matches nSamples
                if len(p) != nSamples:
                    self.logger.error(f"[AFM] The number of samples ({nSamples}) "
                                      f"does not match the number of parameters ({len(p)})"
                                      f" for parameter \"{allParameters[paramIndex]}\"")
                    raise Exception("The number of samples does not match the number of parameters")
            else:
                #Create list of len nSamples
                setattr(self,allParameters[paramIndex],[p]*nSamples)

    def generateSimulationPool(self):

        ########################################

        unitsComponent = eval(f"_units.{self.units}")(name="units")

        ########################################

        simulationPool = []

        #Check sample names are unique
        samplesNames = []
        for smp in self.samples.keys():
            if smp in samplesNames:
                self.logger.error("[AFM] Sample name %s is not unique!" % smp)
                raise Exception("Sample name is not unique!")
            else:
                samplesNames.append(smp)

        for index,[smp,smpModels] in enumerate(self.samples.items()):

            sim = {"system":[{"type":"simulationName","parameters":{"simulationName":smp}}],
                   "units":[{"type":self.units}],
                   "types":[{"type":self.types}],
                   "ensemble":[{"type":"NVT","parameters":{"box":self.box,"temperature":self.temperature}}],
                   "integrators":[self.integrator],
                   "models":copy.deepcopy(smpModels.get("models",[])),
                   "modelOperations":copy.deepcopy(smpModels.get("modelOperations",[])),
                   "modelExtensions":copy.deepcopy(smpModels.get("modelExtensions",[])),
                   "simulationSteps":copy.deepcopy(smpModels.get("simulationSteps",[])),
                   }

            K_smp   = self.K[index]
            Kxy_smp = self.Kxy[index]

            epsilon_smp = self.epsilon[index]
            sigma_smp   = self.sigma[index]

            tipVelocity_smp = self.tipVelocity[index]

            tipMass_smp   = self.tipMass[index]
            tipRadius_smp = self.tipRadius[index]
            tipCharge_smp = self.tipCharge[index]

            initialTipSampleDistance_smp = self.initialTipSampleDistance[index]

            thermalizationSteps_smp = self.thermalizationSteps[index]
            indentationSteps_smp    = self.indentationSteps[index]

            if self.addSurface:
                epsilonSurface_smp  = self.epsilonSurface[index]
                surfacePosition_smp = self.surfacePosition[index]

                if self.absorptionHeight is not None:
                    absorptionHeight_smp = self.absorptionHeight[index]
                    absorptionK_smp      = self.absorptionK[index]

            #Add tip
            if len(smpModels) > 0:
                sim["models"].append({"name":"TIP","type":"PARTICLE","parameters":{"particleName":"TIP",
                                                                                   "particleMass":tipMass_smp,
                                                                                   "particleRadius":tipRadius_smp,
                                                                                   "particleCharge":tipCharge_smp}})
            else:
                sim["models"].append({"name":"TIP","type":"PARTICLE","parameters":{"particleName":"TIP",
                                                                                   "particleMass":tipMass_smp,
                                                                                   "particleRadius":tipRadius_smp,
                                                                                   "particleCharge":tipCharge_smp,
                                                                                   "position":[0.0,0.0,initialTipSampleDistance_smp+tipRadius_smp]}})

            #Declare selections
            tipSelection = ["TIP"]
            sampleSelection = []

            if len(smpModels) > 0:

                for mdl in smpModels["models"]:
                    if "name" in mdl["parameters"]:
                        sampleSelection.append(mdl["name"])
                    else:
                        sampleSelection.append(mdl["type"])


                ###Model operations
                #if self.maxForce is not None:
                #    sim["modelOperations"].append({"type":"setParticleLowestPosition","parameters":{"position":self.surfacePosition,
                #                                                                                    "considerRadius":True,
                #                                                                                    "radiusFactor":2.0,
                #                                                                                    "selection":{"models":copy.deepcopy(sampleSelection)}}})
                #else:

                if self.addSurface:
                    sim["modelOperations"].append({"type":"setParticleLowestPosition","parameters":{"position":surfacePosition_smp,
                                                                                                    "considerRadius":True,
                                                                                                    "selection":{"models":copy.deepcopy(sampleSelection)}}})

                sim["modelOperations"].append({"type":"setContactDistance","parameters":{"distance":initialTipSampleDistance_smp,
                                                                                         "invert":True,
                                                                                         "reference":{"models":copy.deepcopy(sampleSelection)},
                                                                                         "mobile":{"models":copy.deepcopy(tipSelection)}}})
            ###Model extensions

            #Add AFM

            sim["modelExtensions"].append({"type":"AFM","parameters":{"K":K_smp,"Kxy":Kxy_smp,
                                                                      "epsilon":epsilon_smp,
                                                                      "sigma":sigma_smp,
                                                                      "tipVelocity":tipVelocity_smp,
                                                                      "indentationStartStep":thermalizationSteps_smp,
                                                                      "tip":{"models":copy.deepcopy(tipSelection)},
                                                                      "sample":{"models":copy.deepcopy(sampleSelection)}}})

            #Add sample constraint during thermalization
            if self.fixSampleDuringThermalization:
                sim["modelExtensions"].append({"type":"constraintCenterOfMassPosition",
                                               "parameters":{"K":[Kxy_smp,Kxy_smp,0.0],
                                                             "r0":0.0,
                                                             "position":[0.0,0.0,0.0],
                                                             "endStep":thermalizationSteps_smp,
                                                             "selection":{"models":copy.deepcopy(sampleSelection)}
                                                            }
                                               })

            ##Add surface
            if self.addSurface:

                if self.maxForce is not None:
                    sim["modelExtensions"].append({"type":"surfaceMaxForce","parameters":{"epsilon":epsilonSurface_smp,
                                                                                          "surfacePosition":surfacePosition_smp,
                                                                                          "maxForce":self.maxForce,
                                                                                          "selection":{"models":copy.deepcopy(sampleSelection)}}})
                else:
                    sim["modelExtensions"].append({"type":"surface","parameters":{"epsilon":epsilonSurface_smp,
                                                                                  "surfacePosition":surfacePosition_smp,
                                                                                  "selection":{"models":copy.deepcopy(sampleSelection)}}})

                if self.absorptionHeight is not None:
                    sim["modelExtensions"].append({"type":"absortionSurface","parameters":{"heightThreshold":absorptionHeight_smp,
                                                                                           "K":absorptionK_smp,
                                                                                           "startStep":thermalizationSteps_smp}})

            #Add maxForce
            if self.maxForce is not None:
                sim["simulationSteps"].append({"type":"AFMMaxForce","parameters":{"maxForce":self.maxForce,
                                                                                  "intervalStep":self.maxForceIntervalStep}})

            #Add measures

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

            #Add AFM measurement
            if self.afmMeasurementIntervalStep is not None:
                sim["simulationSteps"].append({"type":"afmMeasurement","parameters":{"intervalStep":self.afmMeasurementIntervalStep,
                                                                                     "outputFilePath":self.afmMeasurementOutputFilePath,
                                                                                     "startStep":thermalizationSteps_smp}})

            simulationPool.append(copy.deepcopy(sim))

        self.loadSimulationPool(copy.deepcopy(simulationPool))

    def setUpSimulation(self, sessionName):
        super().setUpSimulation(sessionName)

class AnalysisAFM:

    def __init__(self,
                 infoFilePath):

        self.logger = logging.getLogger("VLMP")

        ########################################################

    def run(self):
        pass