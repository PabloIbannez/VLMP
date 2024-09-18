import sys, os
import logging
from . import unitsBase

class __UNITS_TEMPLATE__(unitsBase):
    """
    {
    "author": "__AUTHOR__",
    "description": "Brief description of this unit system and its application in the simulation.",
    "parameters": {
        "customConstant1": {"description": "Description of custom constant 1",
                            "type": "float",
                            "default": 1.0},
        "customConstant2": {"description": "Description of custom constant 2",
                            "type": "float",
                            "default": 1.0}
    },
    "example": "
    {
        \"type\": \"__UNITS_TEMPLATE__\",
        \"parameters\": {
            \"customConstant1\": 2.5,
            \"customConstant2\": 3.14
        }
    }
    "
    }
    """

    availableParameters = {"customConstant1", "customConstant2"}
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

        customConstant1 = params.get("customConstant1", 1.0)
        customConstant2 = params.get("customConstant2", 1.0)

        ############################################################
        # Set up units
        ############################################################

        # Set the name of this unit system
        self.setUnitsName("CustomUnits")

        # Add standard constants
        self.addConstant("KBOLTZ", 1.380649e-23)  # Boltzmann constant in SI units
        self.addConstant("ELECOEF", 8.9875517923e9)  # Coulomb's constant in SI units

        # Add custom constants
        self.addConstant("CUSTOM1", customConstant1)
        self.addConstant("CUSTOM2", customConstant2)

        ############################################################
        # Log units setup
        ############################################################

        self.logger.info(f"Initialized {name} units with {len(self._constants)} constants")
