import os,sys

import VLMP

import numpy as np

from VLMP.utils import bounds

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

nParticlesPerBlob = 31

#Read the parameters
temperature    = 1.0

tolerance       = param["tolerance"]
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
nParticles      = param["nParticles"]

overtone        = param["overtone"]
f0              = param["f0"] #MHz
kappa           = param["kappa"] #K/mw^2

maxNIter        = param["maxNIterations"]
nGammas         = param["nGammas"]
toleranceConvergence = param["toleranceConvergence"]

#Process the parameters

icosidodecahedronRadius = rParticle

nIcosidodecahedrons     = nParticles
isIcosidodecahedronsList = isinstance(nIcosidodecahedrons, list)
if not isIcosidodecahedronsList:
    nIcosidodecahedrons = [nIcosidodecahedrons]

nK = kappa
#Check if nK is a list or a single value
isKappaList = isinstance(nK, list)
if not isKappaList:
    nK = [nK]

X = Lxy
Y = Lxy
Z = Lz

heightMean = z0
heightStd  = zstd

particleRadius = computeHydrodynamicRadius(rParticle, nParticlesPerBlob)
particleMass = particleDensity*(2*particleRadius)**3

simulationPool = []
for n in nIcosidodecahedrons:
    for k in nK:
        k = round(k,2)
        simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":sessionName+"_"+str(n)+"_"+str(k)}}],
                               "units":[{"type":"none"}],
                               "types":[{"type":"basic"}],
                               "globals":[{"type":"NVT","parameters":{"box":[X,Y,Z],"temperature":1.0}}],
                               "integrators":[{"type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"integrationSteps":1}}],
                               "models":[{"type":"ICOSIDODECAHEDRON",
                                          "parameters":{"numberOfIcosidodecahedrons":n,
                                                        "particlesPerIcosidodecahedron":nParticlesPerBlob,
                                                        "radiusOfIcosidodecahedron":icosidodecahedronRadius,
                                                        "particleMass":particleMass,
                                                        "particleRadius":particleRadius,
                                                        "K":k,
                                                        "heightMean":heightMean,
                                                        "heightStd":heightStd,
                                                        "heightReference":-Z/2.0,
                                                        "box":[X,Y,Z]}}],
                               "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                    "outputFilePath":sessionName+"_"+str(n)+"_"+str(k),
                                                                                    "outputFormat":"sp"}},
                                                  {"type":"info","parameters":{"intervalStep":10000}}]

                               })

vlmp = VLMP.VLMP("dev")

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation(sessionName)

#######################################

omega = 2*np.pi*f0*overtone
k     = kappa*particleMass*omega**2

processedParameters = {}
processedParameters["outputFilePath"]   = "vqcm.dat"
processedParameters["H"]   = 0.5*Lz
processedParameters["Lxy"] = Lxy
processedParameters["fluidDensity"]         = fluidDensity
processedParameters["viscosity"]            = viscosity
processedParameters["particleDensity"]      = particleDensity
processedParameters["tolerance"]            = tolerance
processedParameters["toleranceConvergence"] = toleranceConvergence
processedParameters["hydrodynamicRadius"]   = particleRadius
processedParameters["omega"]                = 2*np.pi*f0*overtone
processedParameters["maxNIterations"]       = maxNIter
processedParameters["nGammas"]              = nGammas
processedParameters["vwall"]                = vwall

with open(os.path.join(sessionName, "VLMPsession.json"), 'r') as sessionFile:
    session = json.load(sessionFile)

for s in session["simulations"]:
    qcm = os.path.join(sessionName, s[2],"QCM.json")
    with open(qcm, "w") as f:
        opts = jsbeautifier.default_options()
        opts.indent_size  = 2
        f.write(jsbeautifier.beautify(json.dumps(processedParameters), opts))

