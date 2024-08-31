import VLMP

from VLMP.utils.units import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 1

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[200.0,200.0,200.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,"frictionConstant":1.0,"integrationSteps":1000000}}],
                           "models":[{"type":"MEMBRANE","parameters":{"composition":{"DPPC":0.5,"POPC":0.5}}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("size",1)
vlmp.setUpSimulation("TEST")

