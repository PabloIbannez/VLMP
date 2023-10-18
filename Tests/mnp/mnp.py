#!/home/pablo/anaconda3/bin/python

import os,sys

import VLMP

import numpy as np

import json
import jsbeautifier


with open('data_main.txt') as f:
    param = json.load(f)

sessionName = 'TEST'

#Read the parameters

msat               = param["msat"]
coreRadius         = param["coreRadius"]
coreRadiusStd      = param["coreRadiusStd"]
anisotropy         = param["anisotropy"]
anisotropyStd      = param["anisotropyStd"]
coatingWidth       = param["coatingWidth"]
coatingWidthStd    = param["coatingWidthStd"]
lbox               = param["lbox"]

nParticles      = param["nParticles"]
viscosity       = param["viscosity"]
temperature     = param["temperature"]
timeStep        = param["timeStep"]
nSteps          = param["nSteps"]

gyroRatio       = param["gyroRatio"]
damping         = param["damping"]

b0 = 10
f = 0.01

copies          = 1
MIA             = "LLG_Heun"

simulationPool = []
for i in range(copies):
    simulationPool.append({
        "system": [
            {"type": "simulationName", "parameters": {"simulationName": "Test"+str(i)}},
            {"type": "backup", "parameters": {"backupIntervalStep": 100000}}
        ],
        "units": [{"type": "none"}],
        "types": [{"type": "basic"}],
        "ensemble": [
            {"type": "NVT", "parameters": {"box": [lbox, lbox, lbox],
                                           "temperature": temperature}}
        ],
        "integrators": [
            {"type": "MagneticBrownian", "parameters": {"timeStep": timeStep,
                                                        "viscosity": viscosity,
                                                        "damping": damping,
                                                        "gyroRatio": gyroRatio,
                                                        "msat": msat,
                                                        "magneticIntegrationAlgorithm": MIA,
                                                        "integrationSteps": nSteps}}
        ],
        "models": [
            {"type": "MAGNETICNP2", "parameters": {"msat":msat,
                                                   "nParticles":nParticles,
                                                   "coreRadius":coreRadius,
                                                   "coreRadiusStd":coreRadiusStd,
                                                   "coatingWidth":coatingWidth,
                                                   "coatingWidthStd":coatingWidthStd,
                                                   "anisotropy":anisotropy,
                                                   "anisotropyStd":anisotropyStd,
                                                   "initOrientation":"random"}}
        ],

        "modelExtensions":[{"type":"ACMagneticField",
                            "parameters":{
                                "b0":b0,
                                "frequency":f
                            }
                        }],

        "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                             "outputFilePath":"test",
                                                             "outputFormat":"svvma"}},
                           {"type":"meanMagnetizationMeasurement","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"test.magnet",
                                                                                }},
                           {"type":"info","parameters":{"intervalStep":10000}}]
    
    })

vlmp = VLMP.VLMP("addComp")

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation(sessionName)
