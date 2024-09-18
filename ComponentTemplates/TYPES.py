import sys, os
import logging
from . import typesBase

class __TYPES_TEMPLATE__(typesBase):
    """
    {
    "author": "__AUTHOR__",
    "description": "Brief description of what these types represent in the simulation.",
    "parameters": {
        "defaultMass": {"description": "Default mass for new types",
                        "type": "float",
                        "default": 1.0},
        "defaultRadius": {"description": "Default radius for new types",
                          "type": "float",
                          "default": 0.5},
        "param1": {"description": "Description of additional parameter 1",
                   "type": "type of param1"},
        "param2": {"description": "Description of additional parameter 2",
                   "type": "type of param2"}
    },
    "example": "
    {
        \"type\": \"__TYPES_TEMPLATE__\",
        \"parameters\": {
            \"defaultMass\": 2.0,
            \"defaultRadius\": 0.75,
            \"param1\": value1,
            \"param2\": value2
        }
    }
    "
    }
    """

    availableParameters = {"defaultMass", "defaultRadius", "param1", "param2"}
    requiredParameters = set()  # All parameters are optional in this example

    def __init__(self, name, **params):
        super().__init__(_type=self.__class__.__name__,
                         _name=name,
                         availableParameters=self.availableParameters,
                         requiredParameters=self.requiredParameters,
                         **params)

        ############################################################
        # Access and process parameters
        ############################################################

        self.defaultMass = params.get("defaultMass", 1.0)
        self.defaultRadius = params.get("defaultRadius", 0.5)
        self.param1 = params.get("param1")
        self.param2 = params.get("param2")

        ############################################################
        # Set up types
        ############################################################

        self.setTypesName("CustomTypes")  # Set the name for this set of types

        # Add default components for each type
        self.addTypesComponent("mass", self.defaultMass)
        self.addTypesComponent("radius", self.defaultRadius)

        # Add additional components if needed
        if self.param1 is not None:
            self.addTypesComponent("param1", self.param1)
        if self.param2 is not None:
            self.addTypesComponent("param2", self.param2)

        ############################################################
        # Define specific types (example)
        ############################################################

        self.addType(name="TypeA", mass=1.0, radius=0.5)
        self.addType(name="TypeB", mass=2.0, radius=0.75)

        # If additional parameters were defined, include them in type definitions
        if self.param1 is not None and self.param2 is not None:
            self.addType(name="TypeC", mass=1.5, radius=0.6, param1=self.param1, param2=self.param2)

        ############################################################
        # Log types setup
        ############################################################

        self.logger.info(f"Initialized {name} types with {len(self.getTypes())} defined types")
