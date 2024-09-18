# Template for the SYSTEM component.
# This template is used to create the SYSTEM component.
# Comments begin with a hash (#) and they can be removed.

import sys, os
import logging
from . import systemBase

class __SYSTEM_TEMPLATE__(systemBase):
    """
    {"author": "__AUTHOR__",
     "description":
     "Brief description of what this system component does and its purpose in the simulation.
      Explain how it affects the overall simulation setup, any global properties it defines,
      and when it should be used. Provide any relevant background information here.
      You can use multiple lines for clarity.",
     "parameters":{
        "param1":{"description":"Description of parameter 1",
                  "type":"type of param1 (e.g., float, int, str)",
                  "default":null},
        "param2":{"description":"Description of parameter 2",
                  "type":"type of param2",
                  "default":null},
        "param3":{"description":"Description of optional parameter 3",
                  "type":"type of param3",
                  "default":"default_value"}
     },
     "example":"
         {
            \"type\":\"__SYSTEM_TEMPLATE__\",
            \"parameters\":{
                \"param1\":value1,
                \"param2\":value2,
                \"param3\":value3
            }
         }
        "
    }
    """

    availableParameters = {"param1", "param2", "param3"}
    requiredParameters  = {"param1", "param2"}

    def __init__(self, name, **params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         **params)

        # Access logger if needed
        # self.logger.info("Initializing __SYSTEM_TEMPLATE__")

        # Read parameters
        param1 = params["param1"]
        param2 = params["param2"]
        param3 = params.get("param3", "default_value")

        # Process parameters if necessary
        # processed_param = some_function(param1, param2)

        # Generate the system configuration using UAMMD-structured format
        system = {
            name: {
                "type": ["System", "__SYSTEM_TEMPLATE__"],  # UAMMD-structured type
                "parameters": {  # UAMMD-structured parameters
                    "param1": param1,
                    "param2": param2,
                    "param3": param3
                }
            }
        }

        # Set the system configuration
        self.setSystem(system)

        # Log completion if needed
        # self.logger.info("__SYSTEM_TEMPLATE__ initialized successfully")
