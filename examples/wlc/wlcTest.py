import VLMP

copies = 10

simulationPool = []
for i in range(copies):
    print("testSimulation_"+str(i))
    simulationPool.append({"system":[{"type":"simulationName","parameters":{"simulationName":"testSimulation_"+str(i)}}],
                           "units":[{"type":"none"}],
                           "global":[{"type":"NVT","parameters":{"box":[1000.0,1000.0,1000.0],"temperature":1.0}}],
                           "integrator":[{"type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"totalIntegrationTime":1000.0}},
                                         {"name":"BBK2","type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"totalIntegrationTime":1000.0}}],
                           "model":[{"name":"modelTest1",
                                     "type":"wlc",
                                     "parameters":{"N":100,"b":1.0,"Kb":100.0,"Ka":50.0}},
                                    {"name":"modelTest2",
                                     "type":"wlc",
                                     "parameters":{"N":100,"b":1.0,"Kb":100.0,"Ka":50.0}}],
                           "modelOperations":[{"name":"test","type":"setCenterOfMassPosition","parameters":{}}],
                           "modelExtensions":[{"name":"constantForce","type":"constantForce","parameters":{"force":[1.0,2.0,3.0]}}],
                           "simulationSteps":[{"type":"saveState","parameters":{"intervalStep":1000,"outputFilePath":"test","outputFormat":"sp"}}]})


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.splitSimulationPool("upperLimit","numberOfParticles",200)
vlmp.aggregateSimulationPool()
vlmp.setUpSimulation("test_sim")

