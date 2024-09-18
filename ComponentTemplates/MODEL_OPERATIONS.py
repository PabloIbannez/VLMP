import sys, os
import logging
from . import modelOperationBase

class __MODEL_OPERATION_TEMPLATE__(modelOperationBase):
    """
    {
    "author": "__AUTHOR__",
    "description": "Short description of what this model operation does.",
    "parameters": {
        "param1": {"description": "Description of parameter 1",
                   "type": "type of param1"},
        "param2": {"description": "Description of parameter 2",
                   "type": "type of param2"},
        "param3": {"description": "Description of parameter 3",
                   "type": "type of param3",
                   "default": "default value if any"}
    },
    "selections": {
        "selection1": {"description": "Description of selection 1",
                       "type": "type of selection1"},
        "selection2": {"description": "Description of selection 2",
                       "type": "type of selection2"}
    },
    "example": "
    {
        \"type\": \"__MODEL_OPERATION_TEMPLATE__\",
        \"parameters\": {
            \"param1\": value1,
            \"param2\": value2,
            \"selection1\": \"model1 type A\",
            \"selection2\": \"model2 type B\"
        }
    }
    "
    }
    """

    availableParameters = {"param1", "param2", "param3"}
    requiredParameters = {"param1", "param2"}
    availableSelections = {"selection1", "selection2"}
    requiredSelections = {"selection1"}

    def __init__(self, name, **params):
        super().__init__(_type=self.__class__.__name__,
                         _name=name,
                         availableParameters=self.availableParameters,
                         requiredParameters=self.requiredParameters,
                         availableSelections=self.availableSelections,
                         requiredSelections=self.requiredSelections,
                         **params)

        ############################################################
        # Access and process parameters
        ############################################################

        param1 = params["param1"]
        param2 = params["param2"]
        param3 = params.get("param3", "default_value")

        # Process selections
        selection1 = self.getSelection("selection1")
        selection2 = self.getSelection("selection2") if "selection2" in params else None

        ############################################################
        # Implement the model operation logic
        ############################################################

        # Example: Modify positions of selected particles
        selected_ids = selection1  # Assuming selection1 is the main selection to operate on
        positions = self.getIdsState(selected_ids, "position")

        # Perform operations on positions...
        new_positions = [self._process_position(pos, param1, param2) for pos in positions]

        # Update the state with new positions
        self.setIdsState(selected_ids, "position", new_positions)

        ############################################################
        # Log the operation
        ############################################################

        self.logger.info(f"Completed {self._name} operation on {len(selected_ids)} particles")

    def _process_position(self, position, param1, param2):
        # Example processing function
        return [p + param1 * param2 for p in position]
