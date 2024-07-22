import sys, os

import logging

from . import simulationStepBase

class oscillatoryForceMeasurement(simulationStepBase):
    """
    {
        "author": "Pablo Palacios-Alonso",
        "description": "Performs oscillatory force measurements to study viscoelastic properties of the system.",
        "parameters": {
            "outputFilePath": {
                "description": "Path to the output file for oscillatory force measurements.",
                "type": "str",
                "default": null
            },
            "f": {
                "description": "Frequency of the oscillatory force.",
                "type": "float",
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
            "fluidDensity": {
                "description": "Density of the fluid.",
                "type": "float",
                "default": null
            },
            "id_and_force": {
                "description": "Dictionary of particle IDs and corresponding force amplitudes.",
                "type": "dict",
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
                "default": 15
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
            "printSteps": {
                "description": "Number of steps between prints of intermediate results.",
                "type": "int",
                "default": 0
            }
        },
        "selections": {},
        "example": "
        {
            \"type\": \"oscillatoryForceMeasurement\",
            \"parameters\": {
                \"outputFilePath\": \"oscforce_results.dat\",
                \"f\": 1e6,
                \"hydrodynamicRadius\": 1e-9,
                \"viscosity\": 1e-3,
                \"fluidDensity\": 1000,
                \"kernel\": \"Gaussian\",
                \"tolerance\": 1e-6,
                \"maxNIterations\": 20000,
                \"toleranceConvergence\": 1e-5,
                \"memory\": 20,
                \"damping\": 1e-6,
                \"notAcceleratedInterval\": 3,
                \"h\": 1e-6,
                \"printSteps\": 100
            }
        }
        "
    }
    """

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
                           }
    requiredParameters  = {"outputFilePath",
                           "f",
                           "hydrodynamicRadius",
                           "viscosity",
                           "fluidDensity",
                           "id_and_force"}
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



