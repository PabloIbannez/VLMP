import VLMP

import itertools

import json
import jsbeautifier

import numpy as np

import logging

class BoundsBox:

    def __init__(self,nParticles,concentration):
        self.logger = logging.getLogger('VLMP')
        L = round((nParticles/concentration)**(1./3.),2)
        self.box = [L,L,L]

        self.logger.debug(f"[BoundsBox] Bounds box, box size : {L}")

    def getSimulationBox(self):
        return self.box

    def getSimulationBounds(self):
        return {}

    def check(self,position):

        boxX,boxY,boxZ = [b/2.0 for b in self.box]

        x,y,z = position
        if (x>boxX or y>boxY or z>boxZ or x<-boxX or y<-boxY or z<-boxZ):
            return False

        return True

class BoundsPlates:

    def __init__(self,nParticles,concentration,particleDiameter,padding,aspectRatio):
        self.logger = logging.getLogger('VLMP')

        self.particleDiameter = particleDiameter

        L = round((nParticles/(concentration*aspectRatio))**(1./3.),2)

        Lz = aspectRatio*L

        self.plateTop    =  Lz/2.0
        self.plateBottom = -Lz/2.0

        self.box = [L,L,self.plateTop + particleDiameter*padding - self.plateBottom]

        self.logger.debug(f"[BoundsPlates] Bounds box, box size : {L},{L},{Lz}")
        self.logger.debug(f"[BoundsPlates] Recomputed concentration {nParticles/(L*L*Lz)}")

    def getSimulationBox(self):
        return self.box

    def getSimulationBounds(self):
        return {"plateTop":self.plateTop,"plateBottom":self.plateBottom}

    def check(self,position):

        boxX,boxY,_ = [b/2.0 for b in self.box]

        x,y,z = position

        zSup    = self.plateTop - 1.05*self.particleDiameter
        zBottom = self.plateBottom + 1.05*self.particleDiameter

        if (x>boxX or y>boxY or z>zSup or x<-boxX or y<-boxY or z<zBottom):
            return False

        return True


padding = 4
aspectRatio = 0.3

N = 20
concentration = 0.0001

particleDiameter = 1.0

mode = "bulk"
if mode == "bulk":
    bnd = BoundsBox(N, concentration)
elif mode == "surface":
    bnd = BoundsPlates(N, concentration, particleDiameter, padding, aspectRatio)

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

