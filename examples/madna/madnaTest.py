import VLMP

copies = 100

ps2AKMA = 20/0.978

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}},
                                     {"type":"backup","parameters":{"backupIntervalStep":100000}}],
                           "units":[{"type":"KcalMol_A"}],
                           "global":[{"type":"NVT","parameters":{"box":[1000.0,1000.0,1000.0],"temperature":300.0}}],
                           "integrator":[{"type":"BBK","parameters":{"timeStep":0.02*ps2AKMA,"frictionConstant":1.0,"integrationSteps":1000000}}],
                           "model":[{"name":"madnaTest",
                                     "type":"MADna",
                                     "parameters":{"sequence":"GATACAGATACAGATACAGATACAGATACAGATACAGATACAGATACAGATACA"}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":10000,
                                                                                "outputFilePath":"test",
                                                                                "outputFormat":"sp"}},
                                              {"type":"info","parameters":{"intervalStep":10000}}]

                           })


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.distributeSimulationPool("upperLimit","numberOfParticles",2000)
vlmp.setUpSimulation("TEST")

