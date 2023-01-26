import VLMP

N      = 1000
copies = 1000

simulationPool = []
for i in range(copies):
    simulationPool.append({"model":{"name":"wlc","parameters":{"N":1000}}})

vlmp = VLMP.VLMP()

vlmp.addSimulationPool(simulationPool)

