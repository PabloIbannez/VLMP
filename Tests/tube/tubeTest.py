import VLMP

import itertools

import json
import jsbeautifier

import numpy as np

N = 15
concentration = 0.0001

# Compute the box size to get concentration
L = np.power(N / concentration, 1.0 / 3.0)
box = [L, L, L]

particleDiameter = 1.0

Eb = np.linspace(-50,-25,3)

simulationPool = []
for eb in Eb:
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":f"tube_Eb{round(eb,2)}"}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "global":[{"type":"NVT","parameters":{"box":box,"temperature":1.0}}],
                           "integrator":[{"type":"EulerMaruyamaRigidBody","parameters":{"timeStep":0.0005,"viscosity":1.0,"integrationSteps":100000000}}],
                           "model":[{"type":"TUBE",
                                     "parameters":{"init":"helix",
                                                   "box":box,
                                                   "nMonomers":N,
                                                   "monomerRadius":particleDiameter/2.0,
                                                   "epsilon_mm":-0.25,
                                                   "Eb":round(eb,2),"rc":0.5,
                                                   "theta0":0.403497,"phi0":0.418879,
                                                   "Kb":10.0,"Ka":1.0,"Kd":1.0,
                                                   "stiffnessFactor":1.0}}],
                            "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                  "outputFilePath":"test",
                                                                                  "outputFormat":"spo"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}],
                           })

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

