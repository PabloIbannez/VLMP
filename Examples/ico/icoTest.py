import VLMP

from VLMP.utils.units import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 1
icoPerSet = 1

simulationPool = []
for i in range(copies):

    models = []
    for m in range(icoPerSet):
        models.append({"name":f"sphere_{m}",
                       #"type":"ICOSPHERE",
                       "type":"CORONAVIRUS_MESH",
                       "parameters":{"particleName":"ICO",
                                     "particleRadius":3.0,
                                     "particleMass":1.0,
                                     "resolution":1,
                                     "radius":3.0,
                                     "Kb":1000.0,
                                     "Kd":0.0}})

    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[80.0,80.0,80.0],"temperature":300.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.0002*ps2AKMA,"frictionConstant":0.2/ps2AKMA,"integrationSteps":100000}}],
                           "models":models.copy(),
                           "modelOperations":[{"type":"distributeRandomly","parameters":{"mode":{"sphere":{"radius":40.0,"center":[0.0,0.0,0.0]}},
                                                                                         #"avoidClashes":False,
                                                                                         "selection":{}}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",2000)
vlmp.setUpSimulation("TEST")

