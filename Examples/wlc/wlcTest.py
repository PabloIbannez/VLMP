import VLMP

import json
import jsbeautifier

copies = 10

L=100
Kb=100.0
Ka=50.0

simulationPool = []
for i in range(copies):
    simulationPool.append(
                          {"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":10000}}],
                           "units":[{"type":"none"}],
                           "types":[{"type":"basic"}],
                           "ensemble":[{"type":"NVT","parameters":{"box":[200.0,200.0,100.0],"temperature":1.0}}],
                           "integrators":[{"type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"integrationSteps":1000000}}],
                           "models":[{"type":"WLC",
                                      "parameters":{"N":L,"b":1.0,"Kb":Kb,"Ka":Ka}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"output",
                                                                                "outputFormat":"sp"}},
                                              {"type":"anglesMeasurement","parameters":{"intervalStep":1000,
                                                                                        "outputFilePath":"angles.dat",
                                                                                        "selection":{"expression":{"forceField":["angles"]}}}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           }

)

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("none")
#vlmp.distributeSimulationPool("property",["topology","forceField","bonds","parameters","K"])
#vlmp.distributeSimulationPool("size",2)
vlmp.setUpSimulation("TEST")

