import VLMP

N      = 10
copies = 10

simulationPool = []
for i in range(copies):
    simulationPool.append({"modelCreation":[{"name":"modelTest1",
                                             "type":"wlc",
                                             "parameters":{"N":100}},
                                            {"name":"modelTest2",
                                             "type":"wlc",
                                             "parameters":{"N":100}}],
                           "modelOperations":[{"name":"test","type":"testType","parameters":{"A":1.0}}],
                           "modelExtensions":[]})


vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(simulationPool)
vlmp.splitSimulationPool(6)
vlmp.aggregateSimulationPool()
vlmp.writeSimulationPool("set_test")

