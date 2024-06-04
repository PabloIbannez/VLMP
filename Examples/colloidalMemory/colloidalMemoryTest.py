import VLMP
import numpy as np
import tempfile
import os

T = 300 # K

#Constants in Kcalmol_A
vacuumPermittivity = 1/(4*np.pi*332.0636)
kb = 0.0019872041

#Parameters
Sigma = 50 # Amstrong
radius = Sigma # reduced units
density = 0.602214 #Density of water in Da/A^3
density_factor = 1.01
M = density*density_factor*4*np.pi*(Sigma**3)/3 # mass of a particle in Da
m = M # mass of a particle in reduced units
Epsilon = 5*kb*T # KcalMol_A
#frictionConstant = Sigma*6*np.pi*0.001 # ps^-1
frictionConstant = 0.2

integrationSteps = 10000000
Npart = 100000
V = 2 # mV

epsP = 100
epsM = 30
CM = -np.logspace(-1,2,3)
#CM = -(epsP-epsM)/(epsP+2*epsM)

r_ring = 1.5*radius # reduced unit
ring_width = r_ring/10
E0 = V/np.log(8*r_ring/ring_width)/r_ring # V/Sigma

alpha = 2*np.pi*Sigma**3*epsM*vacuumPermittivity*CM*E0**2*Sigma # KcalMol_Sigma

# Create simulation pool
simulationPool = []

for j in range(len(CM)):
    dt = 0.2*10**(4)
    #name = "escapeTimeTest_V"+str(V[i])
    name = "BBK_CM"+str(int(-CM[j]))
    theta = [np.random.uniform(0.0,2*np.pi) for i in range(Npart)]
    r = [np.random.uniform(0.0,10.0*radius) for i in range(Npart)]
    z = [np.random.uniform(-7.0*radius+(2**(1/6)*radius),10.0*radius-(2**(1/6)*radius)) for i in range(Npart)]
    simulationPool.append(
            {"system": [{"type":"simulationName","parameters":{"simulationName":name}}],
             "units": [{"type":"KcalMol_A"}],
             "types": [{"type":"polarizable","parameters":{"mass":1.0,"charge":0.0,"radius":1.0,"polarizability":1.0}}],
             "ensemble": [{"type":"NVT","parameters":{"temperature":T,"box":[20.0*radius,20.0*radius,20.0*radius]}}],
             "integrators": [{"type":"BBK","parameters":{"timeStep":dt,"frictionConstant":frictionConstant,"integrationSteps":integrationSteps}}],
             "models": [{"type":"polarizableParticle","parameters":{"particleName":"A",
                                                                    "particleNumber":Npart,
                                                                    "particlePolarizability":alpha[j],
                                                                    "particleMass":m,
                                                                    "particleRadius":radius,
                                                                    "position":[[r[i]*np.cos(theta[i]),r[i]*np.sin(theta[i]),z[i]] for i in range(Npart)]}}],
             "modelExtensions": [{"type":"colloidalMemory","parameters":{"interactionMatrix":[["A",Epsilon,radius]],
                                                                         "cellNumber":[21,21,21],
                                                                         "plainPosition":-7.0*radius,
                                                                         "cylinderRadius":r_ring,
                                                                         "ringRadius":[r_ring],
                                                                         "ringHeight":[-10*radius],
                                                                         }},
                                 {"name":"ceil", "type":"surface","parameters":{"epsilon":Epsilon,"surfacePosition":10.0*radius}},
                                 {"name":"floor","type":"surface","parameters":{"epsilon":Epsilon,"surfacePosition":-10.0*radius}}],
            # "modelOperations": [{"type":"distributeRandomly","parameters":{
            #     "mode":{
            #         "orthoedron":{"center":[0.0,0.0,5.0],"size":[20.0,20.0,10-2*(2**(1/6)*radius)]},
            #         },
            #     "avoidClashes":3,
            #     "selection":{}
            #     }}
            #                     ],
             "simulationSteps": [{"type":"saveState","parameters":{"outputFilePath":"coords"+name,"outputFormat":"xyz","intervalStep":integrationSteps+1}},
                                 {"type":"escapeTime","parameters":{"outputFilePath":name+".esctime","intervalStep":250,"normalVector":[[0.0,0.0,1.0]],"independentVector":[[0.0,0.0,-7.0*radius]]}},
                                 #{"type":"thermodynamicMeasurement","parameters":{"outputFilePath":name+".thermo","intervalStep":100}}
                                 ]
                })
vlmp = VLMP.VLMP ("addComp")
vlmp.DEBUG_MODE = False
vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("size", 1)
vlmp.setUpSimulation("escapeTimeTest")
print(alpha)
