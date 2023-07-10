import VLMP

import json
import jsbeautifier

from VLMP.utils.utils import picosecond2KcalMol_A_time

ps2AKMA = picosecond2KcalMol_A_time()

copies = 10

simulationPool = []
for i in range(copies):
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"TGEV_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "globals":[{"type":"NVT","parameters":{"box":[2000.0,2000.0,4000.0],"temperature":300.0}}],
                           "integrators":[{"type":"EulerMaruyamaRigidBody","parameters":{"timeStep":0.1*ps2AKMA,"viscosity":1.0/ps2AKMA,"integrationSteps":1000000}}],
                           "models":[{"type":"CORONAVIRUS","parameters":{"nSpikes":40,"surface":True}}],
                           "modelExtensions":[{"type":"constantTorqueOverCenterOfMass",
                                               "parameters":{"torque":[0.0,0.0,-1.0],
                                                             "selection":{"expression":{"type":"lipids"}}
                                                            },

                                               }],
                           "simulationSteps":[{"type":"saveState","parameters":{"startStep":10000,
                                                                                "intervalStep":10000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })

#with open("wlc.json","w") as f:
#    json.dump(simulationPool,f)

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",6000)
vlmp.setUpSimulation("TEST")

