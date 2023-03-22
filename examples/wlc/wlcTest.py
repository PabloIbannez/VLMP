import VLMP

import json
import jsbeautifier

copies = 10

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "global":[{"type":"NVT","parameters":{"box":[1000.0,1000.0,1000.0],"temperature":1.0}}],
                           "integrator":[{"type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"integrationSteps":1000000}}],
                           "model":[{"name":"modelTest1",
                                     "type":"wlc",
                                     "parameters":{"N":100,"b":1.0,"Kb":100.0,"Ka":50.0}}],
                           "modelOperations":[{"type":"setCenterOfMassPosition",
                                               "parameters":{"position":[10,10,10],
                                                             "selection":{"models":["modelTest1"]}}
                                               }],
                           "modelExtensions":[{"type":"constantForce",
                                               "parameters":{
                                                             "force":[1.0,2.0,3.0],
                                                             "selection":{"models":["modelTest1"],
                                                                          "expression":{"particleId":[1,2,3],"polymerIndex":[2,-2]}}
                                                            },

                                               }],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })

with open("wlc.json","w") as f:
    json.dump(simulationPool,f)

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",100)
vlmp.setUpSimulation("TEST")

