import VLMP

from VLMP.utils.geometry import BoundsBox, BoundsPlates

import itertools

import json
import jsbeautifier

import numpy as np

import logging

helixPitch  = 12.0
helixRadius = 2.0

padding = 4
aspectRatio = 0.4

concentration = {}
concentration["helix"]  = 0.00001
concentration["line"]   = 0.00001
concentration["random"] = 0.01

N = {}
N["helix"]  = 20
N["line"]   = 20
N["random"] = 1000

particleDiameter = 1.0

variants = {"fixedCosine":     {"E":100,"Kb":1000.0,"theta_start":0.0,"theta_end":3.1415,"phi_start":0.0,"phi_end":1.5707},
            "fixedExponential":{"E":100,"Kb":1000.0,"Ka":1.0,"Kd":1.0},
            "dynamicCosine":{"energyThreshold":0.0,"Eb":25,"r_start":0.0,"rc":0.25,"theta_start":0.0,"theta_end":3.1415,"phi_start":0.0,"phi_end":1.5707},
            "dynamicExponential":{"energyThreshold":0.0,"Eb":30,"rc":0.25,"Kb":1.0,"Ka":1.0,"Kd":1.0}}

#mode = "surface"

simulationPool = []


modes = {"bulk":{},
         "surface":{"Es":10.0,
                    "beta0":0.0,
                    "El":5,"Sl":0.1}}

# variant, mode, init
toCheck = [("fixedCosine","bulk","helix"),
           ("fixedExponential","bulk","helix"),
           ("fixedCosine","surface","helix"),
           ("fixedExponential","surface","helix"),
           ("fixedCosine","bulk","line"),
           ("fixedExponential","bulk","line"),
           ("dynamicCosine","bulk","helix"),
           ("dynamicExponential","bulk","helix"),
           ("dynamicCosine","bulk","line"),
           ("dynamicExponential","bulk","line"),
           ("dynamicCosine","bulk","random"),
           ("dynamicExponential","bulk","random"),
           ("dynamicCosine","surface","random"),
           ("dynamicExponential","surface","random"),
           ("dynamicCosine","surface","helix"),
           ("dynamicExponential","surface","helix")]

for v,m,i in toCheck:

    n = N[i]

    c = concentration[i]
    if m == "bulk":
        bnd = BoundsBox(n, c)
    elif m == "surface":
        bnd = BoundsPlates(n, c, particleDiameter, padding, aspectRatio)
        plates = bnd.getSimulationBounds()

        modes["surface"]["plateTop"]    = plates["plateTop"]
        modes["surface"]["plateBottom"] = plates["plateBottom"]

    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":f"ftsz_{v}_{m}_{i}"}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":bnd.getSimulationBox(),"temperature":1.0}}],
                           "integrators":[{"parameters":{"timeStep":0.0001,"viscosity":1.0,"integrationSteps":100000000}}],
                           "models":[{"type":"HELIX",
                                     "parameters":{"mode":{m:modes[m].copy()},
                                                   "init":i,
                                                   "nMonomers":n,
                                                   "monomerRadius":particleDiameter/2.0,
                                                   "epsilon_mm":1.0,
                                                   "helixPitch":helixPitch,
                                                   "helixRadius":helixRadius,
                                                   "variant":{v:variants[v].copy()}}}
                                    ],
                            "simulationSteps":[
                                               {"type":"info","parameters":{"intervalStep":10000}}
                                               #,
                                               #{"type":"potentialMeasurement","parameters":{"intervalStep":10000,
                                               #                                             "outputFilePath":"potMeasure.dat",
                                               #                                             "selection":{}}}
                                               ]
                           })

    if "fixed" in v:

        simulationPool[-1]["integrators"][0]["type"] = "EulerMaruyamaRigidBody"

    else:
        simulationPool[-1]["integrators"][0]["type"] = "EulerMaruyamaRigidBodyPatchesState"

    if "dynamic" in v or m == "surface":
        simulationPool[-1]["simulationSteps"].append(
                                               {"type":"savePatchyParticlesState","parameters":{"intervalStep":10000,
                                                                                                "outputFilePath":"test",
                                                                                                "outputFormat":"sp"}}
                                               )
    else:
        simulationPool[-1]["simulationSteps"].append(
                                               {"type":"saveState","parameters":{"intervalStep":10000,
                                                                                 "outputFilePath":"test",
                                                                                 "outputFormat":"spo"}}
                                               )

    if "helix" in i and m == "surface":
        # Add constant force
        simulationPool[-1]["modelExtensions"] = [{"type":"constantForce","parameters":{"force":[0.0,0.0,-5.0],
                                                                                       "endStep":250000,
                                                                                       "selection":{}}}]

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("one")
vlmp.setUpSimulation("TEST")

