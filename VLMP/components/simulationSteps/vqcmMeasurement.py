import sys, os

import logging

from . import simulationStepBase

class vqcmMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Palacios-Alonso and Pablo Ibáñez-Freire",
        "description": "Performs Virtual Quartz Crystal Microbalance (VQCM) measurements to study viscoelastic properties of the system.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for VQCM measurements.",
                "type": "str",
                "default": null
            },
            "f0": {
                "description": "Fundamental frequency of the quartz crystal.",
                "type": "float",
                "default": null
            },
            "overtone": {
                "description": "Overtone number for the measurement.",
                "type": "int",
                "default": null
            },
            "hydrodynamicRadius": {
                "description": "Hydrodynamic radius of the particles.",
                "type": "float",
                "default": null
            },
            "viscosity": {
                "description": "Viscosity of the fluid.",
                "type": "float",
                "default": null
            },
            "vwall": {
                "description": "Velocity of the wall.",
                "type": "float",
                "default": null
            },
            "fluidDensity": {
                "description": "Density of the fluid.",
                "type": "float",
                "default": null
            },
            "kernel": {
                "description": "Kernel function for force calculation. Options: 'Gaussian' or 'Peskin3p'.",
                "type": "str",
                "default": "Peskin3p"
            },
            "tolerance": {
                "description": "Tolerance for Gaussian kernel. Only used if kernel is 'Gaussian'.",
                "type": "float",
                "default": 1e-5
            },
            "maxNIterations": {
                "description": "Maximum number of iterations for the solver.",
                "type": "int",
                "default": 10000
            },
            "toleranceConvergence": {
                "description": "Convergence tolerance for the solver.",
                "type": "float",
                "default": 1e-4
            },
            "memory": {
                "description": "Number of previous steps to consider in the solver.",
                "type": "int",
                "default": 5
            },
            "damping": {
                "description": "Damping factor for the solver.",
                "type": "float",
                "default": 1e-5
            },
            "notAcceleratedInterval": {
                "description": "Interval of non-accelerated steps in the solver.",
                "type": "int",
                "default": 2
            },
            "h": {
                "description": "Step size for numerical integration. If 0, it's computed automatically.",
                "type": "float",
                "default": 0.0
            },
            "resonatorImpedance": {
                "description": "Impedance of the resonator. If -1, it's ignored by UAMMD.",
                "type": "float",
                "default": -1.0
            },
            "printSteps": {
                "description": "Number of steps between prints of intermediate results.",
                "type": "int",
                "default": 0
            },
            "tetherInteractorNames": {
                "description": "List of names for tether interactors.",
                "type": "list of str",
                "default": null
            }
        },
        "selections": {},
        "example": "
        {
            \"type\": \"vqcmMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"vqcm_results.dat\",
                \"f0\": 5e6,
                \"overtone\": 3,
                \"hydrodynamicRadius\": 1e-9,
                \"viscosity\": 1e-3,
                \"vwall\": 1e-3,
                \"fluidDensity\": 1000,
                \"kernel\": \"Gaussian\",
                \"tolerance\": 1e-6,
                \"maxNIterations\": 20000,
                \"toleranceConvergence\": 1e-5,
                \"memory\": 10,
                \"damping\": 1e-6,
                \"notAcceleratedInterval\": 3,
                \"h\": 1e-6,
                \"resonatorImpedance\": 1e6,
                \"printSteps\": 100,
                \"tetherInteractorNames\": [\"tether1\", \"tether2\"]
            }
        }
        "
    }
    """

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
                           "maxNIterations",
                           "toleranceConvergence",
                           "maxNIterations",
                           "memory",
                           "damping",
                           "notAcceleratedInterval",
                           "h",
                           "printSteps",
                           "tetherInteractorNames"}
    requiredParameters  = {"outputFilePath",
                           "f0","overtone",
                           "hydrodynamicRadius",
                           "viscosity",
                           "vwall",
                           "fluidDensity"}
    availableSelections = set()
    requiredSelections  = set()


    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}

        parameters["outputFilePath"] = params["outputFilePath"]

        parameters["kernel"]    = params.get("kernel", "Peskin3p")
        if parameters["kernel"] != "Gaussian" and parameters["kernel"] != "Peskin3p":
            self.logger.error("[vqcmMeasurement] The selected kernel is not valid. Valid kernels: Gaussian, Peskin3p")

        if "tolerance" in params and parameters["kernel"] == "Peskin3p":
            self.logger.error("[vqcmMeasurement] tolerance parameter is not available for Peskin3p kernel")

        if parameters["kernel"] == "Gaussian":
            parameters["tolerance"] = params.get("tolerance", 1e-5)

        parameters["f0"]                 = params["f0"]
        parameters["overtone"]           = params["overtone"]
        parameters["hydrodynamicRadius"] = params["hydrodynamicRadius"]
        parameters["viscosity"]          = params["viscosity"]
        parameters["vwall"]              = params["vwall"]
        parameters["fluidDensity"]       = params["fluidDensity"]

        parameters["maxNIterations"]         = params.get("maxNIterations", 10000)
        parameters["toleranceConvergence"]   = params.get("toleranceConvergence", 1e-4)
        parameters["memory"]                 = params.get("memory", 5)
        parameters["damping"]                = params.get("damping", 1e-5)
        parameters["notAcceleratedInterval"] = params.get("notAcceleratedInterval", 2)
        parameters["h"]                      = params.get("h", 0.0) # 0.0 means it is computed by UAMMD
        parameters["resonatorImpedance"]     = params.get("resonatorImpedance", -1.0) #-1.0 means UAMMD ignores it
        parameters["printSteps"]             = params.get("printSteps", 0)
        tetherInteractorNames                = params.get("tetherInteractorNames",[])
        if len(tetherInteractorNames)>0:
            parameters["tetherInteractorNames"] = tetherInteractorNames

        simulationStep = {
            name:{
              "type":["OscillatingFluidMeasure","VQCMMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



