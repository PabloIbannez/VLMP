import VLMP

import itertools

import json
import jsbeautifier

import numpy as np

N = 2000
concentration = 0.0001

# Compute the box size to get concentration
L = np.power(N / concentration, 1.0 / 3.0)
box = [L, L, L]

particleDiameter = 1.0

Eb = -30

simulationPool = []
simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":f"lemon"}},
                                 {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                       "units":[{"type":"none"}],
                       "types":[{"type":"basic"}],
                       "ensemble":[{"type":"NVT","parameters":{"box":box,"temperature":1.0}}],
                       "integrators":[{"type":"EulerMaruyamaRigidBody","parameters":{"timeStep":0.0005,"viscosity":1.0,"integrationSteps":1000000000}}],
                       "models":[{"type":"LEMON",
                                  "parameters":{"init":"tube",
                                               "box":box,
                                               "nMonomers":N,
                                               "monomerRadius":particleDiameter/2.0,
                                               "pitch":7,"monomersPerTurn":30,
                                               "Eb":Eb,"rc":0.3,
                                               "Kb":1.0,"Ka":0.1,"Kd":0.1,
                                               "epsilonLipids":4.0,
                                               "muLipids":3.0,
                                               "chiLipids":4.0,
                                               "thetaLipids":0.0}}],
                       "modelExtensions":[{"type":"sphericalShell","parameters":{"shellCenter":[0.0,0.0,0.0],
                                                                                "shellRadius":0.0,
                                                                                "maxShellRadius":8.0,
                                                                                "radiusVelocity":0.001}}],
                       "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000000,
                                                                            "outputFilePath":"test",
                                                                            "outputFormat":"spo"}},
                                          {"type":"info","parameters":{"intervalStep":10000}}],
                       })

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

