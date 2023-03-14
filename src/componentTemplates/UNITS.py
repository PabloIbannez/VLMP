#Template for the UNITS component.
#This template is used to create the UNITS component.
#Comments begin with a hash (#) and they can be removed.

import sys, os

import logging

from . import unitsBase

class __UNITS_TEMPLATE__(unitsBase):
    """
    Component name: __UNITS_TEMPLATE__ # Name of the component
    Component type: units # Type of the component

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

    def __init__(self,name,**kwargs):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters  = ["param1","param2","param3",...], # List of parameters used by the component
                         requiredParameters = ["param1","param2",...], # List of required parameters
                         **kwargs)

        ############################################################
        ############################################################
        ############################################################

        #Note logger is accessible through self.logger !!!
        #self.logger.info("Message")

        #AvailableConstants is required by the integratorBase class
        #If this parameter is not provided, an error is raised
        self.availableConstants = { # List of constants defined by the component
            "KBOLTZ": 123141241,
            "ELECOEF": 78428429,
            ...
        }

        self.unitsUAMMD = "unitsUAMMD" # Name of the units in UAMMD-structured

        def getConstant(self,constantName):
            if constantName not in self.availableConstants:
                self.logger.error("[__UNITS_TEMPLATE__] Constant {} not available".format(constantName))
                raise "Constant not available"

            return self.availableConstants[constantName]
