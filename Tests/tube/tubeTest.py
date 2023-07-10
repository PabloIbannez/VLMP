import VLMP

import itertools

import json
import jsbeautifier

import numpy as np

N = 500
concentration = 0.0001

# Compute the box size to get concentration
L = np.power(N / concentration, 1.0 / 3.0)
box = [L, L, L]

particleDiameter = 1.0

Eb = -13

simulationPool = []
simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":f"tube"}},
                                 {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                       "units":[{"type":"none"}],
                       "types":[{"type":"basic"}],
                       "globals":[{"type":"NVT","parameters":{"box":box,"temperature":1.0}}],
                       "integrators":[{"type":"EulerMaruyamaRigidBody","parameters":{"timeStep":0.0005,"viscosity":1.0,"integrationSteps":1000000000}}],
                       "models":[{"type":"TUBE",
                                 "parameters":{"init":"tube",
                                               "box":box,
                                               "nMonomers":N,
                                               "monomerRadius":particleDiameter/2.0,
                                               "pitch":7,"monomersPerTurn":30,
                                               "epsilon_mm":1.0,
                                               "EbT":Eb*0.4,"rcT":0.3,
                                               "KbT":1.0,"KaT":1.0,"KdT":1.0,
                                               "EbL":Eb*1.6,"rcL":0.3,
                                               "KbL":1.0,"KaL":1.0,"KdL":1.0,
                                               "theta0L":0.1}}],
                        "simulationSteps":[{"type":"savePatchyParticlesState","parameters":{"intervalStep":1000,
                                                                                            "outputFilePath":"test",
                                                                                            "outputFormat":"sp"}},
                                          {"type":"info","parameters":{"intervalStep":10000}}],
                       })

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

