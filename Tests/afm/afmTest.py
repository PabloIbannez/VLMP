import VLMP

from VLMP.utils.units import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 1

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[10000.0,10000.0,10000.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,"frictionConstant":1.0,"integrationSteps":10000000}}],
                           "models":[{"type":"SOP",
                                     "parameters":{"PDB":"3dkt.pdb",
                                                   "epsilonNC":1.5}
                                     }],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":100000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"pdb"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("one")
vlmp.setUpSimulation("TEST")

