import VLMP

N      = 10
copies = 10

simulationPool = []
for i in range(copies):
    simulationPool.append({"global":[{"type":"NVT","parameters":{"box":[100.0,100.0,100.0],"temperature":1.0}}],
                           "integrator":[{"type":"BBK","parameters":{"timeStep":0.001,"frictionConstant":1.0,"totalIntegrationTime":1000.0}}],
                           "model":[{"name":"modelTest1",
                                     "type":"wlc",
                                     "parameters":{"N":100}},
                                    {"name":"modelTest2",
                                     "type":"wlc",
                                     "parameters":{"N":100}}],
                           "modelOperations":[{"name":"test","type":"setCenterOfMassPosition","parameters":{}}],
                           "modelExtensions":[{"name":"constantForce","type":"constantForce","parameters":{"force":[1.0,2.0,3.0]}}],
                           "simulationSteps":[{"type":"info"}]})


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.splitSimulationPool("upperLimit","numberOfParticles",1000)
vlmp.aggregateSimulationPool()
vlmp.setUpSimulation("test_sim")

