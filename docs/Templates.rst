Templates
=========

List of available templates for creating new components.

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

Units
-----

.. code-block:: python

    #Template for the UNITS component.
    #This template is used to create the UNITS component.
    #Comments begin with a hash (#) and they can be removed.
    
    import sys, os
    
    import logging
    
    from . import unitsBase
    
    class __UNITS_TEMPLATE__(unitsBase):
        """
        Component name: __UNITS_TEMPLATE__ # Name of the component
        Component type: units # Type of the component
    
        Author: __AUTHOR__ # Author of the component
        Date: __DATE__ # Date of last modification
    
        # Description of the component
        ...
        ...
        ...
    
        :param param1: Description of the parameter 1
        :type param1: type of the parameter 1
        :param param2: Description of the parameter 2
        :type param2: type of the parameter 2
        :param param3: Description of the parameter 3
        :type param3: type of the parameter 3, optional
        ...
        """
    
        def __init__(self,name,**kwargs):
            super().__init__(_type = self.__class__.__name__,
                             _name = name,
                             availableParameters  = ["param1","param2","param3",...], # List of parameters used by the component
                             requiredParameters = ["param1","param2",...], # List of required parameters
                             **kwargs)
    
            ############################################################
            ############################################################
            ############################################################
    
            #Note logger is accessible through self.logger !!!
            #self.logger.info("Message")
    
            #AvailableConstants is required by the integratorBase class
            #If this parameter is not provided, an error is raised
            self.availableConstants = { # List of constants defined by the component
                "KBOLTZ": 123141241,
                "ELECOEF": 78428429,
                ...
            }
    
            self.unitsUAMMD = "unitsUAMMD" # Name of the units in UAMMD-structured
    
            def getConstant(self,constantName):
                if constantName not in self.availableConstants:
                    self.logger.error("[__UNITS_TEMPLATE__] Constant {} not available".format(constantName))
                    raise "Constant not available"
    
                return self.availableConstants[constantName]

 
Ensemble
--------

.. code-block:: python

    #Template for the ENSEMBLE component.
    #This template is used to create the ENSEMBLE component.
    #Comments begin with a hash (#) and they can be removed.
    
    import sys, os
    
    import logging
    
    from . import ensembleBase
    
    class __ENSEMBLE_TEMPLATE__(ensembleBase):
        """
        Component name: __ENSEMBLE_TEMPLATE__ # Name of the component
        Component type: ensemble # Type of the component
    
        Author: __AUTHOR__ # Author of the component
        Date: __DATE__ # Date of last modification
    
        # Description of the component
        ...
        ...
        ...
    
        :param param1: Description of the parameter 1
        :type param1: type of the parameter 1
        :param param2: Description of the parameter 2
        :type param2: type of the parameter 2
        :param param3: Description of the parameter 3
        :type param3: type of the parameter 3, optional
        ...
        """
    
        def __init__(self,name,**kwargs):
            super().__init__(_type= self.__class__.__name__,
                             _name= name,
                             availableParameters  = ["param1","param2","param3",...], # List of parameters used by the component
                             requiredParameters = ["param1","param2",...], # List of required parameters
                             **kwargs)
    
            ############################################################
            ############################################################
            ############################################################
    
            #Note logger is accessible through self.logger !!!
            #self.logger.info("Message")
    
            #Define the component dictionary
            #Particular characteristics of the component are defined here
            #Rembember this dictionary is inteterpreted by the UAMMD-structured !!!
            self.ensemble = {}
    
            #Editable part ...
    
            #Read the parameters
    
            param1 = kwargs.get("param1")
            param2 = kwargs.get("param2")
    
            #It is recommended to define a default value those parameters that are not required
            param3 = kwargs.get("param3",defaultValue = 0.0)
    
            ############################################################
    
            #Process the parameters
    
            #For example:
            param1 = param1 + param2
            ...
    
            ############################################################
    
            #Define the component dictionary
    
            self.ensemble["parameters"] = {"param1":param1,
                                           "param2":param2,
                                           "param3":param3,
                                           ...}

Models
------

.. code-block:: python

    from VLMP.components.models import modelBase
    
    class GENERIC_MODEL(modelBase):
        """
        {"author": "Your Name",
         "description":
         "GENERIC_MODEL description. Provide a detailed explanation of what this model does,
          its key features, and potential applications.
          <p>
          Include information about:
          <p>
          - The main purpose of the model
          <p>
          - Key features and capabilities
          <p>
          - Any specific algorithms or methods used
          <p>
          - Typical use cases or scenarios where this model is particularly useful
          <p>
          Add any other relevant details about the model's behavior or implementation.",
         "parameters":{
            "param1":{"description":"Description of parameter 1",
                      "type":"type of parameter 1 (e.g., int, float, str, list)",
                      "default":"default value if any"},
            "param2":{"description":"Description of parameter 2",
                      "type":"type of parameter 2",
                      "default":"default value if any"},
            # Add more parameters as needed
         },
         "example":"
             {
                \"type\":\"GENERIC_MODEL\",
                \"parameters\":{
                    \"param1\":value1,
                    \"param2\":value2
                    # Add example values for all parameters
                }
             }
            ",
         "references":[
             ".. [Ref1] Author, A. (Year). Title of the reference. Journal, Volume(Issue), Pages.",
             ".. [Ref2] Author, B. (Year). Title of another reference. Conference/Book, Pages.",
             # Add more references as needed
         ]
        }
        """
    
        availableParameters = {"param1", "param2"}  # List all available parameters
        requiredParameters  = {"param1"}  # List required parameters
        definedSelections   = {"selectionType1", "selectionType2"}  # List defined selection types
    
        def __init__(self,name,**params):
            super().__init__(_type = self.__class__.__name__,
                             _name = name,
                             availableParameters = self.availableParameters,
                             requiredParameters  = self.requiredParameters,
                             definedSelections   = self.definedSelections,
                             **params)
    
            ############################################################
            # Initialize model parameters
            param1 = params["param1"]
            param2 = params.get("param2", default_value)  # Use .get() for optional parameters
    
            # Log initialization information
            self.logger.info(f"[GENERIC_MODEL] Initializing with param1={param1}, param2={param2}")
    
            ############################################################
            # Set up model components (types, state, structure, force field)
    
            # Set up types
            types = self.getTypes()
            # Add types as needed, e.g.:
            # types.addType(name="TypeName", mass=mass_value, radius=radius_value)
    
            # Set up state
            state = {}
            state["labels"] = ["id", "position"]  # Add other state variables if needed
            state["data"] = []
            # Populate state data
    
            # Set up structure
            structure = {}
            structure["labels"] = ["id", "type"]  # Add other structure labels if needed
            structure["data"] = []
            # Populate structure data
    
            # Set up force field
            forceField = {}
            # Define force field components, e.g.:
            # forceField["interaction_name"] = {
            #     "type": ["InteractionType", "SpecificInteraction"],
            #     "parameters": {},
            #     "labels": ["label1", "label2", ...],
            #     "data": []
            # }
            # Populate force field data
    
            ############################################################
            # Set the model's state, structure, and force field
            self.setState(state)
            self.setStructure(structure)
            self.setForceField(forceField)
    
        def processSelection(self,selectionType,selectionOptions):
            # Implement selection processing logic
            if selectionType == "selectionType1":
                # Process selection type 1
                pass
            elif selectionType == "selectionType2":
                # Process selection type 2
                pass
            else:
                return None  # Return None for unrecognized selection types
    
            # Return the processed selection

ModelOperation
---------------

.. code-block:: python

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

ModelExtension
---------------

.. code-block:: python

    #Template for the MODEL_EXTENSION component.
    #This template is used to create the MODEL_EXTENSION component.
    #Comments begin with a hash (#) and they can be removed.
    
    import sys, os
    
    import logging
    
    from . import modelExtensionBase
    
    class __MODEL_EXTENSION_TEMPLATE__(modelExtensionBase):
        """
        Component name: __MODEL_EXTENSION_TEMPLATE__ # Name of the component
        Component type: modelExtension # Type of the component
    
        Author: __AUTHOR__ # Author of the component
        Date: __DATE__ # Date of last modification
    
        # Description of the component
        ...
        ...
        ...
    
        :param param1: Description of the parameter 1
        :type param1: type of the parameter 1
        :param param2: Description of the parameter 2
        :type param2: type of the parameter 2
        :param param3: Description of the parameter 3
        :type param3: type of the parameter 3, optional
        ...
        """
    
        def __init__(self,name,**kwargs):
            super().__init__(_type = self.__class__.__name__,
                             _name = name,
                             availableParameters  = ["applyOnModel","selection","param1","param2","param3",...], # List of parameters used by the component
                             requiredParameters = ["applyOnModel","selection","param1","param2",...], # List of required parameters
                             **kwargs)
    
            targetModels = []
            for mdl in self.models:
                if mdl.getName() in self.applyOnModel:
                    targetModels.append(mdl)
    
            ############################################################
            ############################################################
            ############################################################
    
            #Note logger is accessible through self.logger !!!
            #self.logger.info("Message")
    
            #For a model extension units and models are accessible
            #through self.units and self.models.
            #Example
            #unitsName = self.units.getName()
            #
            #for mdl in self.models:
            #   mdl.getIds() ...
    
            #Define the component dictionary
            #Particular characteristics of the component are defined here
            #Rembember this dictionary is inteterpreted by the UAMMD-structured !!!
            self.extension = {}
    
            #Editable part ...
    
            #Read the parameters
    
            param1 = kwargs.get("param1")
            param2 = kwargs.get("param2")
    
            #It is recommended to define a default value those parameters that are not required
            param3 = kwargs.get("param3",defaultValue = 0.0)
    
            ############################################################
    
            #Process the parameters
    
            #For example:
            param1 = param1 + param2
            ...
    
            ############################################################
    
            #Define the component dictionary
    
            self.system["__MODEL_EXTENSION_TEMPLATE__"] = {
                                                            "type":[modelExtensionClass,modelExtensionSubClass],
                                                            "parameters":{
                                                                "param1":param1,
                                                                "param2":param2,
                                                                "param3":param3,
                                                                ...
                                                            }
                                                            "labels":[...] # Labels of the component
                                                            "data":[[...],
                                                                    [...],
                                                                     ...] # Data of the component
                                                            }

Integrator
-----------

.. code-block:: python

    #Template for the INTEGRATORS component.
    #This template is used to create the INTEGRATORS component.
    #Comments begin with a hash (#) and they can be removed.
    
    import sys, os
    
    import logging
    
    from . import integratorBase
    
    class __INTEGRATORS_TEMPLATE__(integratorBase):
        """
        Component name: __INTEGRATORS_TEMPLATE__ # Name of the component
        Component type: integrator # Type of the component
    
        Author: __AUTHOR__ # Author of the component
        Date: __DATE__ # Date of last modification
    
        # Description of the component
        ...
        ...
        ...
    
        :param param1: Description of the parameter 1
        :type param1: type of the parameter 1
        :param param2: Description of the parameter 2
        :type param2: type of the parameter 2
        :param param3: Description of the parameter 3
        :type param3: type of the parameter 3, optional
        ...
        """
    
        def __init__(self,name,**kwargs):
            super().__init__(_type= self.__class__.__name__,
                             _name= name,
                             availableParameters  = ["integrationSteps","param1","param2","param3",...], # List of parameters used by the component
                             requiredParameters = ["integrationSteps","param1","param2",...], # List of required parameters
                             **kwargs)
    
            ############################################################
            ############################################################
            ############################################################
    
            #Note logger is accessible through self.logger !!!
            #self.logger.info("Message")
    
            #Integration steps is required by the integratorBase class
            #If this parameter is not provided, an error is raised
            self.integrationSteps = kwargs.get("integrationSteps")
    
            #Define the component dictionary
            #Particular characteristics of the component are defined here
            #Rembember this dictionary is inteterpreted by the UAMMD-structured !!!
            self.integrator = {}
    
            #Editable part ...
    
            #Read the parameters
    
            param1 = kwargs.get("param1")
            param2 = kwargs.get("param2")
    
            #It is recommended to define a default value those parameters that are not required
            param3 = kwargs.get("param3",defaultValue = 0.0)
    
            ############################################################
    
            #Process the parameters
    
            #For example:
            param1 = param1 + param2
            ...
    
            ############################################################
    
            #Define the component dictionary
    
            self.integrator = {
                               "type"=["IntegratorClass","IntegratorSubClass"],
                               "parameters":{
                                    "param1":param1,
                                    "param2":param2,
                                    "param3":param3,
                                   ... #Note than integrationSteps is not included here !!!
                                }
                               }

SimulationStep
--------------

.. code-block:: python

    #Template for the SIMULATION_STEPS component.
    #This template is used to create the SIMULATION_STEPS component.
    #Comments begin with a hash (#) and they can be removed.
    
    import sys, os
    
    import logging
    
    from . import simulationStepBase
    
    class __SIMULATION_STEPS_TEMPLATE__(simulationStepBase):
        """
        Component name: __SIMULATION_STEPS_TEMPLATE__ # Name of the component
        Component type: simulationStepBase # Type of the component
    
        Author: __AUTHOR__ # Author of the component
        Date: __DATE__ # Date of last modification
    
        # Description of the component
        ...
        ...
        ...
    
        :param param1: Description of the parameter 1
        :type param1: type of the parameter 1
        :param param2: Description of the parameter 2
        :type param2: type of the parameter 2
        :param param3: Description of the parameter 3
        :type param3: type of the parameter 3, optional
        ...
        """
    
        def __init__(self,name,**params):
            super().__init__(_type = self.__class__.__name__,
                             _name = name,
                             availableParameters  = ["param1","param2","param3",...], # List of parameters used by the component
                             requiredParameters   = ["param1","param2",...], # List of required parameters
                             availableSelections  = ["selection1","selection2",...], # List of selections used by the component
                             requiredSelections   = ["selection1","selection2",...], # List of required selections
                             #If none use set() instead of [] for available and required parameters and selections
                             **params)
    
            ############################################################
            ############################################################
            ############################################################
    
            #Note there several accesible methods than can be used
            #Units: getUnits()
            #Types: getTypes()
    
            #Note logger is accessible through self.logger
            #self.logger.info("Message")
    
            #Read the parameters
    
            outputFilePath = self.getParameter("outputFilePath")
    
            param1 = self.getParameter("param1")
            param2 = self.getParameter("param2")
    
            #It is recommended to define a default value those parameters that are not required
            param3 = self.getParameter("param3",defaultValue = 0.0)
    
            ############################################################
    
            #Here we have to fill the simulationStep itself.
            #Remember you have to use UAMMD-structured syntax
    
            parameters = {}
    
            parameters["outputFilePath"] = outputFilePath
            parameters["param1"] = param1
            parameters["paramA"] = param2+param3
    
            simulationStep = {
                name : { #We use the name of the component as the name of the simulationStep
                    "type" : ["SimulationStepClass","SimulationStepSubClass"], #Type of the simulationStep
                    "parameters" : {**parameters} #Parameters of the simulationStep
                }
            }
    
            ############################################################
    
            #We can add the group the simulationSteps is applied to
            #We can use a given selection
    
            self.setGroup("selection1")
    
            #We finally add the simulationStep to the component
            self.setSimulationSteps(simulationStep)

