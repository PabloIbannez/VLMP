import VLMP

from VLMP.utils.utils import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 10

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "global":[{"type":"NVT","parameters":{"box":[1000.0,1000.0,1000.0],"temperature":300.0}}],
                           "integrator":[{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,"frictionConstant":1.0/ps2AKMA,"integrationSteps":1000000}}],
                           "model":[{"name":"madnaTest",
                                     "type":"MADna",
                                     "parameters":{"sequence":"GATACAGATACAGATACAGATACAGATACAGATACAGATACAGATACAGATACA"}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "pbc":False,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"thermodynamicMeasurement","parameters":{"intervalStep":10000,
                                                                                 "outputFilePath":"thermo.dat"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

