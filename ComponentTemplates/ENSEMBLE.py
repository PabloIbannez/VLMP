#Template for the ENSEMBLE component.
#This template is used to create the ENSEMBLE component.
#Comments begin with a hash (#) and they can be removed.

import sys, os
import logging
from . import ensembleBase

class __ENSEMBLE_TEMPLATE__(ensembleBase):
    """
    {"author": "__AUTHOR__",
     "description":
     "Brief description of what this ensemble does and its purpose in the simulation.
      Provide any relevant background information or key features here.
      You can use multiple lines for clarity",

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
            \"type\":\"__ENSEMBLE_TEMPLATE__\",
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

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         **params)

        ############################################################
        ############################################################
        ############################################################

        # Access logger if needed
        # self.logger.info("Initializing __ENSEMBLE_TEMPLATE__")

        # Read parameters
        param1 = params["param1"]
        param2 = params["param2"]
        param3 = params.get("param3", "default_value")

        # Process parameters if necessary
        # processed_param = some_function(param1, param2)

        # Set the ensemble name
        self.setEnsembleName("__ENSEMBLE_TEMPLATE__") # This has to be a UAMMD-structured available ensemble name

        self.addEnsembleComponent("componentName1", value)
        self.addEnsembleComponent("componentName2", value)
        # ...

        # Log completion if needed
        # self.logger.info("__ENSEMBLE_TEMPLATE__ initialized successfully")
