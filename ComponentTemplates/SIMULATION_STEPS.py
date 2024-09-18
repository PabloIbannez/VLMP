import sys, os
import logging
from . import simulationStepBase

class __SIMULATION_STEPS_TEMPLATE__(simulationStepBase):
    """
    {
    "author": "__AUTHOR__",
    "description": "Brief description of what this simulation step does.",
    "parameters": {
        "intervalStep": {"description": "Interval at which this step is executed",
                         "type": "int"},
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
        \"type\": \"__SIMULATION_STEPS_TEMPLATE__\",
        \"parameters\": {
            \"intervalStep\": 100,
            \"param1\": value1,
            \"param2\": value2,
            \"selection1\": \"model1 type A\",
            \"selection2\": \"model2 type B\"
        }
    }
    "
    }
    """

    availableParameters = {"intervalStep", "param1", "param2", "param3"}
    requiredParameters = {"intervalStep", "param1", "param2"}
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

        intervalStep = params["intervalStep"]
        param1 = params["param1"]
        param2 = params["param2"]
        param3 = params.get("param3", "default_value")

        # Process selections
        selection1 = self.getSelection("selection1")
        selection2 = self.getSelection("selection2") if "selection2" in params else None

        ############################################################
        # Set up the simulation step
        ############################################################

        simulationStep = {
            name: {
                "type": ["SimulationStepType", "SimulationStepSubType"],
                "parameters": {
                    "intervalStep": intervalStep,
                    "param1": param1,
                    "param2": param2,
                    "param3": param3
                }
            }
        }

        # If the simulation step requires additional data, add it here
        if selection1:
            simulationStep[name]["labels"] = ["id"]
            simulationStep[name]["data"] = [[id] for id in selection1]

        # Set the group if needed (e.g., if the step applies to a specific selection)
        self.setGroup("selection1")

        # Set the simulation step
        self.setSimulationStep(simulationStep)

        ############################################################
        # Log simulation step setup
        ############################################################

        self.logger.info(f"Initialized {name} simulation step with interval {intervalStep}")

    def _additional_processing(self, selection):
        # Example method for additional processing if needed
        pass
