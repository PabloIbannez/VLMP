import VLMP

from VLMP.utils.utils import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 1000

simulationPool = []
for i in range(copies):
    print("ico_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[10000.0,10000.0,10000.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.0002*ps2AKMA,"frictionConstant":0.2/ps2AKMA,"integrationSteps":1000}}],
                           "models":[#{"type":"FILE",
                                     # "parameters":{"inputFilePath":"test.json"}},
                                     {"type":"ICOSPHERE",
                                      "parameters":{"particleName":"ICO",
                                                    "particleRadius":1.0,
                                                    "particleMass":1.0,
                                                    "resolution":1,
                                                    "radius":5.0,
                                                    "Kb":1000.0,
                                                    "Kd":0.0,
                                                    "position":[0.0,0.0,10.0]}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":100,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP("dev")

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",2000)
vlmp.setUpSimulation("TEST")

