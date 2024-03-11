import sys, os

import logging

from . import simulationStepBase

class oscillatoryForceMeasurement(simulationStepBase):
    """
    Component name: oscillatoryForceMeasurement
    Component type: simulationStep

    Author: Pablo Palacios-Alonso
    Date: 23/02/2024

    """


    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath",
                                                "kernel",
                                                "tolerance",
                                                "f",
                                                "hydrodynamicRadius",
                                                "viscosity",
                                                "fluidDensity",
                                                "maxNIterations",
                                                "toleranceConvergence",
                                                "maxNIterations",
                                                "memory",
                                                "damping",
                                                "notAcceleratedInterval",
                                                "h",
                                                "printSteps",
                                                "id_and_force"
                                                },
                         requiredParameters  = {"outputFilePath",
                                                "f",
                                                "hydrodynamicRadius",
                                                "viscosity",
                                                "fluidDensity",
                                                "id_and_force"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params["outputFilePath"]

        parameters["kernel"]    = params.get("kernel", "Peskin3p")

        if parameters["kernel"] != "Gaussian" and parameters["kernel"] != "Peskin3p":
            self.logger.error("[oscillatoryForceMeasurement] The selected kernel is not valid. Valid kernels: Gaussian, Peskin3p")
            
        if "tolerance" in params and parameters["kernel"] == "Peskin3p":
            self.logger.error("[oscillatoryForceMeasurement] tolerance parameter is not available for Peskin3p kernel")

        if parameters["kernel"] == "Gaussian":
            parameters["tolerance"] = params.get("tolerance", 1e-5)
            parameters["h"]         = params.get("h", 0.0) # 0.0 means it is computed by UAMMD

        parameters["f"]                  = params["f"]
        parameters["hydrodynamicRadius"] = params["hydrodynamicRadius"]
        parameters["viscosity"]          = params["viscosity"]
        parameters["fluidDensity"]       = params["fluidDensity"]
        id_and_force                     = params["id_and_force"]

        
        parameters["maxNIterations"]         = params.get("maxNIterations", 10000)
        parameters["toleranceConvergence"]   = params.get("toleranceConvergence", 1e-4)
        parameters["memory"]                 = params.get("memory", 15)
        parameters["damping"]                = params.get("damping", 1e-5)
        parameters["notAcceleratedInterval"] = params.get("notAcceleratedInterval", 2)
        parameters["printSteps"]             = params.get("printSteps", 0)
        
        labels = ["id_list", "force"]
        data   = []

        for id_i in id_and_force.keys():
            data += [[id_i, id_and_force[id_i]]]
        
        simulationStep = {
            name:{
              "type":["OscillatingFluidMeasure","VAFMMeasure"],
                "parameters":{**parameters},
                "labels":labels,
                "data":data
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



