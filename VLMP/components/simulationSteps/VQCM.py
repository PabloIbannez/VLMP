import sys, os

import logging

from VLMP.components.simulationSteps import simulationStepBase

class VQCM(simulationStepBase):
    """
    Component name: VQCM
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire and Pablo Palacios
    Date: 19/06/2023

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :tolerance: Tolerance
    :type tolerance: float
    :param omega: QCM angular frequency
    :type omega: float
    :param hydrodynamicRadius: Hydrodynamic radius
    :type hydrodynamicRadius: float
    :param viscosity: Viscosity
    :type viscosity: float
    :param fluidMass: Fluid mass
    :type fluidMass: float
    :param vwall: Wall velocity
    :type vwall: complex, [float,float]
    :param nIterations: Number of iterations
    :type nIterations: int
    :param gamma: Gamma
    :type gamma: float

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"outputFilePath",
                                                "tolerance",
                                                "omega",
                                                "hydrodynamicRadius",
                                                "viscosity",
                                                "fluidMass",
                                                "vwall",
                                                "nIterations",
                                                "gamma"},
                         requiredParameters  = {"outputFilePath",
                                                "tolerance",
                                                "omega",
                                                "hydrodynamicRadius",
                                                "viscosity",
                                                "fluidMass",
                                                "vwall",
                                                "nIterations",
                                                "gamma"},
                         availableSelections = set(),
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        parameters = {}
        parameters["outputFilePath"] = params["outputFilePath"]

        parameters["tolerance"] = params["tolerance"]

        parameters["omega"] = params["omega"]

        parameters["hydrodynamicRadius"] = params["hydrodynamicRadius"]
        parameters["viscosity"]          = params["viscosity"]
        parameters["fluidMass"]          = params["fluidMass"]

        parameters["vwall"] = params["vwall"]

        parameters["nIterations"] = params["nIterations"]
        parameters["gamma"]       = params["gamma"]


        simulationStep = {
            name:{
              "type":["VQCMMeasure","VQCMMeasure"],
              "parameters":{**parameters}
            }
        }

        ############################################################

        self.setSimulationStep(simulationStep)



