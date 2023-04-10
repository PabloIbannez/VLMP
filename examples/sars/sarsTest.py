import VLMP

from VLMP.experiments.SurfaceUmbrellaSampling import SurfaceUmbrellaSampling

#############################################################################################################################

ps2AKMA = VLMP.utils.picosecond2KcalMol_A_time()

parameters = {"umbrella":{"nWindows":66,
                          "windowsStartPosition":135.0,
                          "windowsEndPosition":735.0,
                          "K":[0.001,0.05],
                          "Ksteps":[150000,150000000],
                          "measurementsIntervalStep":1000},
              "simulation":{"backupIntervalStep":100000,
                            "units":"KcalMol_A",
                            "temperature":300.0,
                            "box":[2000.0, 2000.0, 4000.0],
                            "models":[],
                            "selection":{"type":"lipids"},
                            "integrator":{"type":"EulerMaruyamaRigidBody","parameters":{"timeStep":0.1*ps2AKMA,"viscosity":1.0/ps2AKMA}}},
              "output":{"infoIntervalStep":10000,
                        "saveStateIntervalStep":100000,
                        "saveStateOutputFilePath":"output",
                        "saveStateOutputFormat":"sp"}
              }

for i in range(1):
    parameters["simulation"]["models"].append({"type":"CORONAVIRUS","parameters":{"nSpikes":40,"surface":True}})

surfUmbrella = SurfaceUmbrellaSampling(parameters)

vlmp = VLMP.VLMP()

vlmp.loadSimulationPool(surfUmbrella.generateSimulationPool())
#vlmp.distributeSimulationPool("upperLimit","numberOfParticles",40000)
vlmp.distributeSimulationPool("one")
vlmp.setUpSimulation("TEST")

