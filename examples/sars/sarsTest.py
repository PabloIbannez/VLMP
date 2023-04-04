import VLMP

import json
import jsbeautifier

copies = 10

ps2AKMA = 20/0.978

simulationPool = []
for i in range(copies):
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"TGEV_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "global":[{"type":"NVT","parameters":{"box":[2000.0,2000.0,4000.0],"temperature":300.0}}],
                           "integrator":[{"type":"EulerMaruyamaRigidBody","parameters":{"timeStep":0.1*ps2AKMA,"viscosity":1.0/ps2AKMA,"integrationSteps":1000000}}],
                           "model":[{"type":"CORONAVIRUS","parameters":{"nSpikes":40,"surface":True}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })

#with open("wlc.json","w") as f:
#    json.dump(simulationPool,f)

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",25000)
vlmp.setUpSimulation("TEST")

