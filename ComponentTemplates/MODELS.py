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
