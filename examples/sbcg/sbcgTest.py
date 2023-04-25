import VLMP

copies = 1

ps2AKMA = 20/0.978

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "types":[{"type":"basic"}],
                           "global":[{"type":"NVT","parameters":{"box":[10000.0,10000.0,10000.0],"temperature":300.0}}],
                           "integrator":[{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,"frictionConstant":1.0,"integrationSteps":1000000}}],
                           "model":[{"type":"SBCG",
                                     "parameters":{"PDB":"mergedTMV_20.pdb",
                                                   "resolution":150,
                                                   "steps":10000,
                                                   "SASA":False,
                                                   "bondsModel":{"name":"ENM",
                                                                 "parameters":{"enmCut":12.0,
                                                                               "K":10.0}},
                                                   "nativeContactsModel":{"name":"CA",
                                                                          "parameters":{"ncCut":8.0,
                                                                                        "epsilon":0.5,
                                                                                        "D":1.5}}}
                                     }],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",2000)
vlmp.setUpSimulation("TEST")

