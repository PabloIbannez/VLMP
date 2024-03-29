#!/home/pablo/anaconda3/bin/python

import os,sys

import VLMP

import numpy as np

import json
import jsbeautifier

def computeHydrodynamicRadius(rSphere, nParticles):
    vSphere = 4./3.*np.pi*pow(rSphere,3);
    vBlob   = vSphere/nParticles;
    rBlob   = 0.5*vBlob**(1./3.);
    return rBlob;

with open('data_main.txt') as f:
    param = json.load(f)

#

sessionName = 'TEST'

#Read the parameters
temperature    = 1.0

vwall           = param["vwall"] #nm/us?
z0              = param["z0"]  #nm
zstd            = param["zSTD"] #nm
Lxy             = param["Lxy"] #nm
Lz              = param["Lz"]  #nm

#Density input units: kg/m3; code unit ag/nm^3 (1ag = 1e-18 g)
particleDensity = param["particleDensity"]*1e-6
fluidDensity    = param["fluidDensity"]*1e-6

#Viscosity input units: Pa*s =  kg/(m*s); code unit ag/(nm*us) (1ag = 1e-18 g)
viscosity       = param["viscosity"]*1e6
rParticle       = param["rParticle"] #nm

nParticles        = param["nParticles"]
nBlobsPerParticle = param["blobsPerParticle"]

overtone        = param["overtone"]
f0              = param["f0"] #MHz
kappa           = param["kappa"] #K/mw^2

maxNIter             = param["maxNIterations"]
toleranceConvergence = param["toleranceConvergence"]

#Process the parameters

omega        = 2*np.pi*f0*overtone

sphereRadius = rParticle

nSpheres           = nParticles
nKappa             = kappa
nz0                = z0
nnBlobsPerParticle = nBlobsPerParticle

nLists = 0
isSpheresList = isinstance(nSpheres, list)
if not isSpheresList:
    nSpheres = [nSpheres]
else:
    nLists += 1

isKappaList = isinstance(nKappa, list)
if not isKappaList:
    nKappa = [nKappa]
else:
    nLists += 1

isz0List = isinstance(nz0, list)
if not isz0List:
    nz0 = [nz0]
else:
    nLists += 1

isnBlobsPerParticleList = isinstance(nnBlobsPerParticle, list)
if not isnBlobsPerParticleList:
    nnBlobsPerParticle = [nnBlobsPerParticle]
else:
    nLists += 1


X = Lxy
Y = Lxy
Z = Lz

heightStd  = zstd


simulationPool = []
if nLists > 1:
    with open('output.txt', 'w') as f:
        f.write('ERROR: Only one magnitude can be an array at the same time\n')
        f.close()
        sys.exit(1)

for n in nSpheres:
    for kappa_i in nKappa:
        for heightMean in nz0:
            for nbp in nnBlobsPerParticle:
                particleRadius = computeHydrodynamicRadius(rParticle, nbp)
                particleMass = particleDensity*(2*particleRadius)**3
                k = kappa_i*particleMass*omega**2
                kappa_i = round(kappa_i,2)
                filename = sessionName +"_"+str(n)+"_"+str(kappa_i)+"_"+str(heightMean)+"_"+str(nbp)
                simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":filename}}],
                                       "units":[{"type":"none"}],
                                       "types":[{"type":"basic"}],
                                       "ensemble":[{"type":"NVT","parameters":{"box":[X,Y,Z],"temperature":1.0}}],
                                       "integrators":[{"type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"integrationSteps":100000}}],
                                       "models":[{"type":"SPHEREMULTIBLOB",
                                                  "parameters":{"sphereType":"icosphere",
                                                                "numberOfSpheres":n,
                                                                "particlesPerSphere":nbp,
                                                                "radiusOfSphere":sphereRadius,
                                                                "particleMass":particleMass,
                                                                "particleRadius":particleRadius,
                                                                "K":k,
                                                                "heightMean":heightMean,
                                                                "heightStd":heightStd,
                                                                "heightReference":-Z/2.0}}],
                                       "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                            "outputFilePath":sessionName+"_"+str(n)+"_"+str(k),
                                                                                            "outputFormat":"sp"}},
                                                          {"type":"vqcmMeasurement","parameters":{"intervalStep":10000,
                                                                                                  "outputFilePath":sessionName+"_"+str(n)+"_"+str(k)+".json",
                                                                                                  "f0":f0,
                                                                                                  "overtone":[overtone],
                                                                                                  "hydrodynamicRadius":particleRadius,
                                                                                                  "viscosity":viscosity,
                                                                                                  "fluidDensity":fluidDensity,
                                                                                                  "vwall":vwall,
                                                                                                  "printSteps":10}},
                                                          {"type":"info","parameters":{"intervalStep":10000}}]

                                       })

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("one")
vlmp.setUpSimulation(sessionName)
