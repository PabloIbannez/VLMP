import VLMP

import json
import jsbeautifier

copies = 10

simulationPool = []
for i in range(copies):
    #print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[200.0,200.0,100.0],"temperature":1.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"integrationSteps":1000000}}],
                           "models":[{"name":"modelTest1",
                                      "type":"WLC",
                                      "parameters":{"N":50,"b":1.0,"Kb":100.0,"Ka":50.0}},
                                     {"name":"modelTest2",
                                      "type":"WLC",
                                      "parameters":{"N":50,"b":1.0,"Kb":100.0,"Ka":50.0}}],
                           "modelOperations":[{"type":"setCenterOfMassPosition",
                                               "parameters":{"position":[10,10,10],
                                                             "selection":{"models":["modelTest1"]}}
                                               }],
                           #"modelExtensions":[{"type":"constantForce",
                           #                    "parameters":{
                           #                                  "force":[1.0,2.0,3.0],
                           #                                  "selection":{"models":["modelTest1"],
                           #                                               "expression":{"particleId":[1,2,3],"polymerIndex":[2,-2]}}
                           #                                 },

                           #                    }],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
vlmp.setUpSimulation("TEST")

