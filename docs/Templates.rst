Templates
=========

----

System
------

.. code-block:: python

    # Template for the SYSTEM component.
    # This template is used to create the SYSTEM component.
    # Comments begin with a hash (#) and they can be removed.

    import sys
    import os
    import logging
    from . import systemBase

    class __SYSTEM_TEMPLATE__(systemBase):
        """
        {
        "author": "__AUTHOR__",
        "description": "Short text describing what the new system does.",
        "parameters": {
            "param1": {"description": "Description of the first parameter.",
                       "type": "type1 (int, str, bool, ...)"},
            "param2": {"description": "Description of the second parameter.",
                       "type": "type2 (int, str, bool, ...)"},
            "param3": {"description": "Description of the third parameter.",
                       "type": "type3",
                       "default": false}
        },
        "example": "
        {
            \"type\": \"__SYSTEM_TEMPLATE__\",
            \"parameters\": {
                \"param1\": 1,
                \"param2\": 10,
                \"param3\": 12
            }
        }
        "
        }
        """

        # Define available and required parameters for the component
        availableParameters = {"param1", "param2", "param3"}  # List of all valid parameters for this component
        requiredParameters  = {"param1", "param2"}            # Parameters that must be provided by the user

        def __init__(self, name, **params):
            """
            Initializes the __SYSTEM_TEMPLATE__ component.

            :param name: The name of the component instance.
            :param params: A dictionary of parameters supplied to the component.
            """
            # Initialize the base class with the component type, name, and parameters
            super().__init__(_type=self.__class__.__name__,
                             _name=name,
                             availableParameters=self.availableParameters,
                             requiredParameters=self.requiredParameters,
                             **params)

            # Initialize the system dictionary for this component
            # Remember that this dictionary is interpreted by UAMMD-structured.
            system = {
                name: {
                    "type": ["Simulation", "__SYSTEM_TEMPLATE__"],  # Types of simulations this component can handle
                    "parameters": {}  # Parameters will be added here after processing
                }
            }

            ############################################################
            # Read and Validate Parameters
            ############################################################

            # Retrieve the required parameters from the input params dictionary
            param1 = params.get("param1")
            param2 = params.get("param2")
            
            # Retrieve the optional param3, providing a default value if it's not set
            param3 = params.get("param3", 0.0)

            ############################################################
            # Process Parameters
            ############################################################
            # Perform any necessary calculations or transformations on the input parameters.
            # Example: square of param1, add param2 and param3, and compute some new values
            newParam1 = param1 ** 2
            newParam2 = param2 + param3
            newParam3 = param3 ** 2 + 3

            # Assign processed parameters to the system dictionary
            system[name]["parameters"]["param1"] = newParam1
            system[name]["parameters"]["param2"] = newParam2

            # Only include param3 if it's non-zero (optional behavior)
            if param3 != 0: 
                system[name]["parameters"]["param3"] = newParam3

            ############################################################
            # Set System Configuration
            ############################################################
            # Set the component's system configuration using the processed system dictionary
            self.setSystem(system)

            # Log initialization info
            self.logger.info(f"Initialized {name} with parameters: {params}")
