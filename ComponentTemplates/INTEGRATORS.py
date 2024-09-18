import sys, os
import logging
from . import integratorBase

class __INTEGRATORS_TEMPLATE__(integratorBase):
    """
    {"author": "__AUTHOR__",
     "description":
     "Brief description of what this integrator does and its purpose in the simulation.
      Explain the integration method, its advantages, and when it should be used.
      Provide any relevant background information or key features here.
      You can use multiple lines for clarity",
     "parameters":{
        "integrationSteps":{"description":"Number of integration steps",
                            "type":"int",
                            "default":null},
        "timeStep":{"description":"Time step for integration",
                    "type":"float",
                    "default":null},
        "param1":{"description":"Description of parameter 1",
                  "type":"type of param1",
                  "default":null},
        "param2":{"description":"Description of optional parameter 2",
                  "type":"type of param2",
                  "default":"default_value"}
     },
     "example":"
         {
            \"type\":\"__INTEGRATORS_TEMPLATE__\",
            \"parameters\":{
                \"integrationSteps\":1000,
                \"timeStep\":0.001,
                \"param1\":value1,
                \"param2\":value2
            }
         }
        "
    }
    """

    availableParameters = {"integrationSteps", "timeStep", "param1", "param2"}
    requiredParameters  = {"integrationSteps", "timeStep", "param1"}

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
        # self.logger.info("Initializing __INTEGRATORS_TEMPLATE__")

        # Read parameters
        integrationSteps = params["integrationSteps"]
        timeStep = params["timeStep"]
        param1 = params["param1"]
        param2 = params.get("param2", "default_value")

        # Process parameters if necessary
        # processed_param = some_function(param1, timeStep)

        # Define the integrator dictionary using UAMMD-structured format
        integrator = {
            "type": ["Integrator", "__INTEGRATORS_TEMPLATE__"],  # UAMMD-structured type
            "parameters": {  # UAMMD-structured parameters
                "timeStep": timeStep,
                "param1": param1,
                "param2": param2
                # Add any other necessary parameters
                # Note: integrationSteps is handled separately by UAMMD
            }
        }

        # Set the integration steps
        self.setIntegrationSteps(integrationSteps)

        # Set the integrator
        self.setIntegrator(integrator)

        # Log completion if needed
        # self.logger.info("__INTEGRATORS_TEMPLATE__ initialized successfully")
