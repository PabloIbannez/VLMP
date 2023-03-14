#Template for the GLOBALS component.
#This template is used to create the GLOBALS component.
#Comments begin with a hash (#) and they can be removed.

import sys, os

import logging

from . import globalBase

class __GLOBALS_TEMPLATE__(globalBase):
    """
    Component name: __GLOBALS_TEMPLATE__ # Name of the component
    Component type: global # Type of the component

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
        super().__init__(_type= self.__class__.__name__,
                         _name= name,
                         availableParameters  = ["param1","param2","param3",...], # List of parameters used by the component
                         requiredParameters = ["param1","param2",...], # List of required parameters
                         **kwargs)

        ############################################################
        ############################################################
        ############################################################

        #Note logger is accessible through self.logger !!!
        #self.logger.info("Message")

        #Define the component dictionary
        #Particular characteristics of the component are defined here
        #Rembember this dictionary is inteterpreted by the UAMMD-structured !!!
        self.globals = {}

        #Editable part ...

        #Read the parameters

        param1 = kwargs.get("param1")
        param2 = kwargs.get("param2")

        #It is recommended to define a default value those parameters that are not required
        param3 = kwargs.get("param3",defaultValue = 0.0)

        ############################################################

        #Process the parameters

        #For example:
        param1 = param1 + param2
        ...

        ############################################################

        #Define the component dictionary

        self.globals["parameters"] = {"param1":param1,
                                      "param2":param2,
                                      "param3":param3,
                                      ...}
