import VLMP

from VLMP.utils.utils import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 1
icoPerSet = 200

simulationPool = []
for i in range(copies):

    models = []
    for m in range(icoPerSet):
        models.append({"name":f"part_{m}",
                       "type":"PARTICLE",
                       "parameters":{"particleName":"A",
                                     "particleRadius":5.0,
                                     "particleMass":1.0}})

    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[100.0,100.0,100.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.0002*ps2AKMA,"frictionConstant":0.2/ps2AKMA,"integrationSteps":100000}}],
                           "models":models.copy(),
                           "modelOperations":[{"type":"distributeRandomly","parameters":{"mode":{"sphere":{"radius":40.0,
                                                                                                           "center":[10.0,0.0,0.0]}},
                                                                                         "avoidClashes":10000,
                                                                                         "selection":{}}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("size",1)
vlmp.setUpSimulation("TEST")

