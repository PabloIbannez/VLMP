import VLMP

import itertools

import json
import jsbeautifier

from VLMP.utils import bounds

import numpy as np

padding = 4
aspectRatio = 0.3

N = 1000
concentration = 0.03

particleDiameter = 1.0

mode = "surface"
if mode == "bulk":
    bnd = bounds.BoundsBox(N, concentration)
elif mode == "surface":
    bnd = bounds.BoundsPlates(N, concentration, particleDiameter, padding, aspectRatio)

simulationPool = []

Eb = np.linspace(-50,-25,10)
El = np.linspace(8,1,1)

for eb,el in itertools.product(Eb,El):
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":f"ftsz_Eb{eb}_El{el}"}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "global":[{"type":"NVT","parameters":{"box":bnd.getSimulationBox(),"temperature":1.0}}],
                           "integrator":[{"type":"EulerMaruyamaRigidBody","parameters":{"timeStep":0.0005,"viscosity":1.0,"integrationSteps":100000000}}],
                           "model":[{"type":"HELIX",
                                     "parameters":{"mode":mode,"init":"random",
                                                   "bounds":bnd,
                                                   "nMonomers":N,
                                                   "monomerRadius":particleDiameter/2.0,
                                                   "epsilon_mm":-0.25,
                                                   "Eb":eb,"rc":0.5,
                                                   "theta0":0.125,"phi0":0.3,
                                                   "varDst":0.0001,"varTheta":0.0015,"varPhi":0.005,
                                                   "Es":10.0,"beta0":1.57,"El":el,"Sl":0.1}}],
                            "simulationSteps":[{"type":"savePatchyParticlesState","parameters":{"intervalStep":100000,
                                                                                                "outputFilePath":"test",
                                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}},
                                              {"type":"patchPolymersMeasurement","parameters":{"intervalStep":1000}}],
                           })

    if mode == "surface":
        plates = bnd.getSimulationBounds()
        simulationPool[-1]["model"][0]["parameters"]["plateTop"]    = plates["plateTop"]
        simulationPool[-1]["model"][0]["parameters"]["plateBottom"] = plates["plateBottom"]


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

