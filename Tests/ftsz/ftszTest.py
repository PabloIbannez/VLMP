import VLMP

import itertools

import json
import jsbeautifier

from VLMP.utils import bounds

import numpy as np

padding = 4
aspectRatio = 0.3

N = 20
concentration = 0.0001

particleDiameter = 1.0

mode = "bulk"
if mode == "bulk":
    bnd = bounds.BoundsBox(N, concentration)
elif mode == "surface":
    bnd = bounds.BoundsPlates(N, concentration, particleDiameter, padding, aspectRatio)

simulationPool = []

Eb = np.linspace(-50,-30,1)
El = np.linspace(20,1,1)

for eb,el in itertools.product(Eb,El):
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":f"ftsz_Eb{round(eb,2)}_El{round(el,2)}"}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":bnd.getSimulationBox(),"temperature":1.0}}],
                           "integrators":[{"type":"EulerMaruyamaRigidBodyPatchesState","parameters":{"timeStep":0.0005,"viscosity":1.0,"integrationSteps":1000000}}],
                           "models":[{"type":"HELIX",
                                     "parameters":{"mode":mode,"init":"helix",
                                                   "bounds":bnd,
                                                   "nMonomers":N,
                                                   "monomerRadius":particleDiameter/2.0,
                                                   "epsilon_mm":-0.25,
                                                   "Eb":round(eb,2),"rc":0.5,
                                                   "theta0":0.125,"phi0":0.3,
                                                   "varDst":0.0001,"varTheta":0.0015,"varPhi":0.005,
                                                   "stiffnessFactor":0.8,
                                                   "Es":10.0,"beta0":1.57,"El":round(el,2),"Sl":0.1,
                                                   "variant":{"twoStates":{"Eb2":round(eb,2)*0.8,"rc2":0.5,
                                                                           "theta02":0.125,"phi02":0.3,
                                                                           "varDst2":0.0001,"varTheta2":0.0015,"varPhi2":0.005,
                                                                           "prob_1_to_2":0.01,"prob_2_to_1":0.01}}}}],
                            "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                 "outputFilePath":"test",
                                                                                 "outputFormat":"spo"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}],
                           })

    if mode == "surface":
        plates = bnd.getSimulationBounds()
        simulationPool[-1]["model"][0]["parameters"]["plateTop"]    = plates["plateTop"]
        simulationPool[-1]["model"][0]["parameters"]["plateBottom"] = plates["plateBottom"]


vlmp = VLMP.VLMP("addComp")

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

