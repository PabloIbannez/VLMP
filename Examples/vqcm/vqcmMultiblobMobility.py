import VLMP

import numpy as np

import json
import jsbeautifier

sessionName = "VQCM_MULTIBLOB_MOBILITY"

with open('data_main.txt') as f:
    param = json.load(f)


overtone          = param["overtone"]
f0                = param["f0"]
fluidDensity      = param["fluidDensity"]
blobDensity       = param["blobDensity"]
viscosity         = param["viscosity"]
vwall             = param["vwall"]

kernel            = param["kernel"]
tolerance         = param.get("tolerance", 1e-3)

Lxy               = param["Lxy"]
Lz                = param["Lz"]

numberOfSpheres   = param["numberOfSpheres"]
blobsPerSphere    = param["blobsPerSphere"]
sphereRadius      = param["sphereRadius"]
surfaceRatio      = param["surfaceRatio"]
kappa             = param["kappa"]
z0_mean           = param["z0_mean"]
z0_std            = param.get("z0_std", 0)

isnumberOfSpheresList = isinstance(numberOfSpheres, list)
if not isnumberOfSpheresList:
    nSpheres_list = [numberOfSpheres]
else:
    nSpheres_list = numberOfSpheres

isKappaList = isinstance(kappa, list)
if not isKappaList:
    kappa_list = [kappa]
else:
    kappa_list = kappa

isz0List = isinstance(z0_mean, list)
if not isz0List:
    z0_mean_list = [z0_mean]
else:
    z0_mean_list = z0_mean

isOvertoneList = isinstance(overtone, list)
if not isOvertoneList:
    overtone = [overtone]

isblobsPerSphereList = isinstance(blobsPerSphere, list)
if not isblobsPerSphereList:
    blobsPerSphere = [blobsPerSphere]

simulationPool = []

for n in nSpheres_list:
    for bps in blobsPerSphere:

        if bps == 30:
            sphereType = "icosidodecahedron"
        else:
            sphereType = "icosphere"
            for kappa_i in kappa_list:
                for heightMean in z0_mean_list:
                    K = kappa_i*(2*np.pi*f0)**2
                    kappa_i = round(kappa_i,2)
                    blobRadius = (4.0*surfaceRatio*sphereRadius**2/bps)**0.5
                    blobMass                  = blobDensity*(2*blobRadius)**3
                    filename = sessionName +"_"+str(n)+"_"+str(kappa_i)+"_"+str(heightMean)
                    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":filename}}],
                                           "units":[{"type":"none"}],
                                           "types":[{"type":"basic"}],
                                           "ensemble":[{"type":"NVT","parameters":{"box":[Lxy,Lxy,Lz],"temperature":1.0}}],
                                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.0001,"frictionConstant":1.0,"integrationSteps":1}}],
                                           "models":[{"type":"SPHEREMULTIBLOB",
					              "parameters":{"sphereType":sphereType,
							  	    "numberOfSpheres":n,
                                                                    "particlesPerSphere":bps,
                                                                    "radiusOfSphere":sphereRadius,
                                                                    "particleMass":blobMass,
                                                                    "particleRadius":blobRadius,
                                                                    "K":K,
                                                                    "heightMean":heightMean,
                                                                    "heightStd":z0_std,
                                                                    "heightReference":-Lz/2.0}}],
                                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1,
                                                                                                "outputFilePath":"test",
                                                                                                "outputFormat":"sp"}},
                                                              {"type":"vqcmMeasurementFromMobility","parameters":{"intervalStep":1,
                                                                                                                  "outputFilePath":"vqcmMobility.json",
                                                                                                                  "tolerance":tolerance,
                                                                                                                  "f0":f0,
                                                                                                                  "overtone":overtone,
                                                                                                                  "kernel":kernel,
                                                                                                                  "hydrodynamicRadius":blobRadius,
                                                                                                                  "viscosity":viscosity,
                                                                                                                  "fluidDensity":fluidDensity,
                                                                                                                  "vwall":vwall}},
                                                              {"type":"info","parameters":{"intervalStep":10000}}]
                                           
                                           
                                           })
                    

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("one")
vlmp.setUpSimulation(sessionName)

