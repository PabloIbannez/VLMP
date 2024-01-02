import VLMP

from VLMP.utils.geometry import BoundsBox, BoundsPlates

import itertools

import json
import jsbeautifier

import numpy as np

import logging

padding = 4
aspectRatio = 0.3

N = 40
concentration = 0.00001

particleDiameter = 1.0

#mode = "surface"
mode = "bulk"
if mode == "bulk":
    bnd = BoundsBox(N, concentration)
elif mode == "surface":
    bnd = BoundsPlates(N, concentration, particleDiameter, padding, aspectRatio)

simulationPool = []

Eb = np.linspace(-100,-30,1)
El = np.linspace( 20,  1,1)

for eb,el in itertools.product(Eb,El):

    plates = bnd.getSimulationBounds()

    #mode = {"surface":{"Es":10.0,
    #                   "beta0":1.57,
    #                   "El":round(el,2),"Sl":0.1,
    #                   "plateTop":plates["plateTop"],
    #                   "plateBottom":plates["plateBottom"]}}

    mode = {"bulk":{}}

    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":f"ftsz_Eb{round(eb,2)}_El{round(el,2)}"}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":bnd.getSimulationBox(),"temperature":1.0}}],
                           "integrators":[{"type":"EulerMaruyamaRigidBodyPatchesState","parameters":{"timeStep":0.00001,"viscosity":1.0,"integrationSteps":1}}],
                           "models":[{"type":"HELIX2",
                                     "parameters":{"mode":mode,"init":"helix",
                                                   "nMonomers":N,
                                                   "monomerRadius":particleDiameter/2.0,
                                                   "epsilon_mm":-0.25,
                                                   "Eb":round(eb,2),"rc":0.5,
                                                   #"theta0":0.125,"phi0":0.3,
                                                   "helixRadius":3.0,"helixPitch":2.0*3.14,"rightHanded":True,
                                                   "varDst":0.0001,"varTheta":0.0015,"varPhi":0.005,
                                                   "stiffnessFactor":0.8
                                                   #"variant":{"twoStates":{"Eb2":round(eb,2)*0.8,"rc2":0.5,
                                                   #                        "theta02":0.125,"phi02":0.3,
                                                   #                        "varDst2":0.0001,"varTheta2":0.0015,"varPhi2":0.005,
                                                   #                        "prob_1_to_2":0.01,"prob_2_to_1":0.01}}}
                                                   }}
                                                  ],
                            "simulationSteps":[
                                               #{"type":"savePatchyParticlesState","parameters":{"intervalStep":10000,
                                               #                                                 "outputFilePath":"test",
                                               #                                                 "outputFormat":"sp"}},
                                               {"type":"saveState","parameters":{"intervalStep":10000,
                                                                                 "outputFilePath":"test",
                                                                                 "outputFormat":"spo"}},
                                               {"type":"potentialMeasurement","parameters":{"intervalStep":10000,
                                                                                            "outputFilePath":"potMeasure.dat",
                                                                                            "selection":{}}},
                                               {"type":"info","parameters":{"intervalStep":10000}}],
                           })

vlmp = VLMP.VLMP("addComp")

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

