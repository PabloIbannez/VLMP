import sys, os
import logging
from . import modelExtensionBase

class __MODEL_EXTENSION_TEMPLATE__(modelExtensionBase):
    """
    {"author": "__AUTHOR__",
     "description":
     "Brief description of what this model extension does and its purpose in the simulation.
      Explain how it extends or modifies the existing model, its advantages, and when it should be used.
      Provide any relevant background information or key features here.
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
     "selections":{
        "selection1":{"description":"Description of selection 1",
                      "type":"list of ids"},
        "selection2":{"description":"Description of optional selection 2",
                      "type":"list of ids"}
     },
     "example":"
         {
            \"type\":\"__MODEL_EXTENSION_TEMPLATE__\",
            \"parameters\":{
                \"param1\":value1,
                \"param2\":value2,
                \"param3\":value3
            },
            \"selections\":{
                \"selection1\":\"model1 type A\",
                \"selection2\":\"model2 resid 1 to 10\"
            }
         }
        "
    }
    """

    availableParameters = {"param1", "param2", "param3"}
    requiredParameters  = {"param1", "param2"}
    availableSelections = {"selection1", "selection2"}
    requiredSelections  = {"selection1"}

    def __init__(self, name, **params):
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

        # Access logger if needed
        # self.logger.info("Initializing __MODEL_EXTENSION_TEMPLATE__")

        # Read parameters
        param1 = params["param1"]
        param2 = params["param2"]
        param3 = params.get("param3", "default_value")

        # Get selections
        selection1 = self.getSelection("selection1")
        selection2 = self.getSelection("selection2") if "selection2" in params else None

        # Process parameters if necessary
        # processed_param = some_function(param1, param2)

        # Define the extension dictionary using UAMMD-structured format
        extension = {
            name: {
                "type": ["ModelExtension", "__MODEL_EXTENSION_TEMPLATE__"],  # UAMMD-structured type
                "parameters": {  # UAMMD-structured parameters
                    "param1": param1,
                    "param2": param2,
                    "param3": param3
                    # Add any other necessary parameters
                },
                "labels": ["id", "value1", "value2"],  # UAMMD-structured labels
                "data": []  # UAMMD-structured data
            }
        }

        # Fill the data based on selections
        for id in selection1:
            # Example of how to fill data, adjust as needed for your specific extension
            extension[name]["data"].append([id, some_value1, some_value2])

        if selection2:
            for id in selection2:
                # Add data for selection2 if it exists
                extension[name]["data"].append([id, some_other_value1, some_other_value2])

        # You can add more complex logic here if needed
        # For example, adding conditional parameters or computed values

        # Set the extension
        self.setExtension(extension)

        # Set group if needed
        # self.setGroup("selection1")

        # Log completion if needed
        # self.logger.info("__MODEL_EXTENSION_TEMPLATE__ initialized successfully")
