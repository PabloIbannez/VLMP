import VLMP

import json
import jsbeautifier

L=10
Kb=100.0
Ka=40.0

setName_idList = {"A":[0,3,6,9], "B":[1,4,7], "C":[2,5,8]}

simulationPool = [{"system":[{"type":"simulationName",
                             "parameters":{"simulationName":"wlc_Ka_"+str(Ka)}},
                            {"type":"backup","parameters":{"backupIntervalStep":10000}}],
                  "units":[{"type":"none"}],
                  "types":[{"type":"basic"}],
                  "ensemble":[{"type":"NVT",
                               "parameters":{"box":[200.0,200.0,200.0],
                            "temperature":1.0}}],
                  "integrators":[{"type":"BBK",
                                  "parameters":{"timeStep":0.001,
                                                "frictionConstant":1.0,
                                                "integrationSteps":1000000}}],
                  "models":[{"type":"WLC",
                             "parameters":{"N":L,"b":1.0,"Kb":Kb,"Ka":Ka}}],
                  "simulationSteps":[{"type":"saveState",
                                      "parameters":{"intervalStep":10000,
                                                    "outputFilePath":"output",
                                                    "outputFormat":"sp"}},
                                     {"type":"forceBetweenSetsMeasurement",
                                      "parameters":{"intervalStep":10000,
                                                    "outputFilePath":"setsForce.out",
                                                    "setName_idList":setName_idList}},
                                     
                                     {"type":"info","parameters":{"intervalStep":10000}}]
                  
                  }]


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("one")
vlmp.setUpSimulation("TEST")

