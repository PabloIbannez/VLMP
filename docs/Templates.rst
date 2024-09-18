Templates
=========

List of available templates for creating new components.

----

SYSTEM
------

.. code-block:: python
  :linenos:

  # Template for the SYSTEM component.
  # This template is used to create the SYSTEM component.
  # Comments begin with a hash (#) and they can be removed.

  import sys, os
  import logging
  from . import systemBase

  class __SYSTEM_TEMPLATE__(systemBase):
      """
      {"author": "__AUTHOR__",
       "description":
       "Brief description of what this system component does and its purpose in the simulation.
        Explain how it affects the overall simulation setup, any global properties it defines,
        and when it should be used. Provide any relevant background information here.
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
       "example":"
           {
              \"type\":\"__SYSTEM_TEMPLATE__\",
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

      def __init__(self, name, **params):
          super().__init__(_type = self.__class__.__name__,
                           _name = name,
                           availableParameters = self.availableParameters,
                           requiredParameters  = self.requiredParameters,
                           **params)

          # Access logger if needed
          # self.logger.info("Initializing __SYSTEM_TEMPLATE__")

          # Read parameters
          param1 = params["param1"]
          param2 = params["param2"]
          param3 = params.get("param3", "default_value")

          # Process parameters if necessary
          # processed_param = some_function(param1, param2)

          # Generate the system configuration using UAMMD-structured format
          system = {
              name: {
                  "type": ["System", "__SYSTEM_TEMPLATE__"],  # UAMMD-structured type
                  "parameters": {  # UAMMD-structured parameters
                      "param1": param1,
                      "param2": param2,
                      "param3": param3
                  }
              }
          }

          # Set the system configuration
          self.setSystem(system)

          # Log completion if needed
          # self.logger.info("__SYSTEM_TEMPLATE__ initialized successfully")

UNITS
-----

.. code-block:: python
  :linenos:

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

TYPES
-----

.. code-block:: python
  :linenos:

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

ENSEMBLE
--------

.. code-block:: python
  :linenos:

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

MODELS
------

.. code-block:: python
  :linenos:

  import sys, os
  import logging
  import numpy as np
  from . import modelBase

  class __MODEL_TEMPLATE__(modelBase):
      """
      {
      "author": "__AUTHOR__",
      "description": "Brief description of what this model represents or simulates.",
      "parameters": {
          "param1": {"description": "Description of parameter 1",
                     "type": "type of param1"},
          "param2": {"description": "Description of parameter 2",
                     "type": "type of param2"},
          "param3": {"description": "Description of parameter 3",
                     "type": "type of param3",
                     "default": "default value if any"}
      },
      "example": "
      {
          \"type\": \"__MODEL_TEMPLATE__\",
          \"parameters\": {
              \"param1\": value1,
              \"param2\": value2,
              \"param3\": value3
          }
      }
      "
      }
      """

      availableParameters = {"param1", "param2", "param3"}
      requiredParameters = {"param1", "param2"}
      definedSelections = {"selectionType1", "selectionType2"}  # Types of selections this model can process

      def __init__(self, name, **params):
          super().__init__(_type=self.__class__.__name__,
                           _name=name,
                           availableParameters=self.availableParameters,
                           requiredParameters=self.requiredParameters,
                           definedSelections=self.definedSelections,
                           **params)

          ############################################################
          # Access and process parameters
          ############################################################

          param1 = params["param1"]
          param2 = params["param2"]
          param3 = params.get("param3", "default_value")

          ############################################################
          # Set up model components
          ############################################################

          # Set up particle types
          types = self.getTypes()
          types.addType(name="TypeA", mass=1.0, radius=0.5)
          types.addType(name="TypeB", mass=2.0, radius=0.7)

          # Generate initial state (e.g., positions)
          num_particles = 100  # Example number of particles
          positions = self._generate_initial_positions(num_particles)

          # Set up state
          state = {
              "labels": ["id", "position"],
              "data": [[i, pos] for i, pos in enumerate(positions)]
          }
          self.setState(state)

          # Set up structure
          structure = {
              "labels": ["id", "type"],
              "data": [[i, "TypeA" if i % 2 == 0 else "TypeB"] for i in range(num_particles)]
          }
          self.setStructure(structure)

          # Set up force field
          force_field = self._setup_force_field(param1, param2)
          self.setForceField(force_field)

          ############################################################
          # Log model setup
          ############################################################

          self.logger.info(f"Initialized {name} model with {num_particles} particles")

      def _generate_initial_positions(self, num_particles):
          # Example: Generate random positions in a cube
          return np.random.uniform(-5, 5, (num_particles, 3)).tolist()

      def _setup_force_field(self, param1, param2):
          # Example: Set up a simple Lennard-Jones potential
          force_field = {
              "LennardJones": {
                  "type": ["NonBonded", "LennardJones"],
                  "parameters": {"epsilon": param1, "sigma": param2},
                  "labels": ["name_i", "name_j", "epsilon", "sigma"],
                  "data": [
                      ["TypeA", "TypeA", param1, param2],
                      ["TypeA", "TypeB", param1, param2],
                      ["TypeB", "TypeB", param1, param2]
                  ]
              }
          }
          return force_field

      def processSelection(self, selectionType, selectionOptions):
          # Implement selection processing logic here
          # This method should return a list of particle IDs based on the selection criteria
          if selectionType == "selectionType1":
              # Process selectionType1
              pass
          elif selectionType == "selectionType2":
              # Process selectionType2
              pass
          return None  # Replace with actual selection logic

MODEL_OPERATIONS
----------------

.. code-block:: python
  :linenos:

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

MODEL_EXTENSIONS
----------------

.. code-block:: python
  :linenos:

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

INTEGRATORS
-----------

.. code-block:: python
  :linenos:

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

SIMULATION_STEPS
----------------

.. code-block:: python
  :linenos:

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

