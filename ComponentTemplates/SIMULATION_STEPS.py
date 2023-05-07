#Template for the SIMULATION_STEPS component.
#This template is used to create the SIMULATION_STEPS component.
#Comments begin with a hash (#) and they can be removed.

import sys, os

import logging

from . import simulationStepBase

class __SIMULATION_STEPS_TEMPLATE__(simulationStepBase):
    """
    Component name: __SIMULATION_STEPS_TEMPLATE__ # Name of the component
    Component type: simulationStepBase # Type of the component

    Author: __AUTHOR__ # Author of the component
    Date: __DATE__ # Date of last modification

    # Description of the component
    ...
    ...
    ...

    :param param1: Description of the parameter 1
    :type param1: type of the parameter 1
    :param param2: Description of the parameter 2
    :type param2: type of the parameter 2
    :param param3: Description of the parameter 3
    :type param3: type of the parameter 3, optional
    ...
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters  = ["param1","param2","param3",...], # List of parameters used by the component
                         requiredParameters   = ["param1","param2",...], # List of required parameters
                         availableSelections  = ["selection1","selection2",...], # List of selections used by the component
                         requiredSelections   = ["selection1","selection2",...], # List of required selections
                         #If none use set() instead of [] for available and required parameters and selections
                         **params)

        ############################################################
        ############################################################
        ############################################################

        #Note there several accesible methods than can be used
        #Units: getUnits()
        #Types: getTypes()

        #Note logger is accessible through self.logger
        #self.logger.info("Message")

        #Read the parameters

        outputFilePath = self.getParameter("outputFilePath")

        param1 = self.getParameter("param1")
        param2 = self.getParameter("param2")

        #It is recommended to define a default value those parameters that are not required
        param3 = self.getParameter("param3",defaultValue = 0.0)

        ############################################################

        #Here we have to fill the simulationStep itself.
        #Remember you have to use UAMMD-structured syntax

        parameters = {}

        parameters["outputFilePath"] = outputFilePath
        parameters["param1"] = param1
        parameters["paramA"] = param2+param3

        simulationStep = {
            name : { #We use the name of the component as the name of the simulationStep
                "type" : ["SimulationStepClass","SimulationStepSubClass"], #Type of the simulationStep
                "parameters" : {**parameters} #Parameters of the simulationStep
            }
        }

        ############################################################

        #We can add the group the simulationSteps is applied to
        #We can use a given selection

        self.setGroup("selection1")

        #We finally add the simulationStep to the component
        self.setSimulationSteps(simulationStep)

