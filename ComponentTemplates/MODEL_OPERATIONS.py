from VLMP.components.modelOperations import modelOperationBase

import numpy as np

class GENERIC_OPERATION(modelOperationBase):
    """
    {
        "author": "Your Name",
        "description": "Brief description of what this operation does.",
        "parameters": {
            "param1": {
                "description": "Description of parameter 1",
                "type": "type of parameter (e.g., float, int, list, etc.)",
                "default": "default value if any"
            },
            "param2": {
                "description": "Description of parameter 2",
                "type": "type of parameter",
                "default": "default value if any"
            }
        },
        "selections": {
            "selection1": {
                "description": "Description of selection 1",
                "type": "list of ids"
            },
            "selection2": {
                "description": "Description of selection 2",
                "type": "list of ids"
            }
        },
        "example": "{
            \"type\": \"GENERIC_OPERATION\",
            \"parameters\": {
                \"param1\": value1,
                \"param2\": value2,
                \"selection1\": \"model1 type A\",
                \"selection2\": \"model2 resid 1 to 10\"
            }
        }"
    }
    """

    availableParameters = {"param1", "param2"}
    requiredParameters  = {"param1"}
    availableSelections = {"selection1", "selection2"}
    requiredSelections  = {"selection1"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         availableSelections = self.availableSelections,
                         requiredSelections  = self.requiredSelections,
                         **params)

        ############################################################
        # Extract parameters and selections
        param1 = params["param1"]
        param2 = params.get("param2", default_value)

        selection1 = self.getSelection("selection1")
        selection2 = self.getSelection("selection2") if "selection2" in params else None

        ############################################################
        # Perform the operation

        # Example: Get positions of selected particles
        pos1 = np.asarray(self.getIdsState(selection1, "position"))

        # Example: Get properties of selected particles
        property1 = np.asarray(self.getIdsProperty(selection1, "some_property"))

        # Implement your operation logic here
        # ...

        # Example: Update positions of selected particles
        new_positions = ... # Compute new positions
        self.setIdsState(selection1, "position", new_positions.tolist())

        ############################################################
        # Log operation results if needed
        self.logger.info(f"[GENERIC_OPERATION] Operation completed on {len(selection1)} particles")
