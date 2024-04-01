import sys, os

import logging

from . import simulationStepBase

class vqcmMeasurementFromMobility(simulationStepBase):
    """
    Component name: vqcmMobilityMeasurement
    Component type: simulationStep

    Author: Pablo Palacios-Alonso
    Date: 01/04/2024

    """


    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath",
                                                "resonatorImpedance",
                                                "kernel",
                                                "tolerance",
                                                "f0",
                                                "overtone",
                                                "hydrodynamicRadius",
                                                "viscosity",
                                                "vwall",
                                                "fluidDensity",
                                                "h"},
                         requiredParameters  = {"outputFilePath",
                                                "f0","overtone",
                                                "hydrodynamicRadius",
                                                "viscosity",
                                                "vwall",
                                                "fluidDensity"},
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
            self.logger.error("[vqcmMobiltyMeasurement] The selected kernel is not valid. Valid kernels: Gaussian, Peskin3p")

        if "tolerance" in params and parameters["kernel"] == "Peskin3p":
            self.logger.error("[vqcmMobilityMeasurement] tolerance parameter is not available for Peskin3p kernel")
            
        if parameters["kernel"] == "Gaussian":
            parameters["tolerance"] = params.get("tolerance", 1e-5)
            
        parameters["f0"]                 = params["f0"]
        parameters["overtone"]           = params["overtone"]
        parameters["hydrodynamicRadius"] = params["hydrodynamicRadius"]
        parameters["viscosity"]          = params["viscosity"]
        parameters["vwall"]              = params["vwall"]
        parameters["fluidDensity"]       = params["fluidDensity"]
    
        parameters["h"]                      = params.get("h", 0.0) # 0.0 means it is computed by UAMMD
        #parameters["resonatorImpedance"]     = params.get("resonatorImpedance", -1.0) #-1.0 means UAMMD ignores it
        
        simulationStep = {
            name:{
                "type":["OscillatingFluidMeasure","VQCMMeasureFromMobility"],
                "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



