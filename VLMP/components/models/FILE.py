from VLMP.components.models import modelBase
from .SIMULATION import SIMULATION

import json
import copy

class FILE(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "FILE model for loading pre-existing simulation configurations. This model allows users to
      import a complete simulation setup from a JSON file, including particle positions, types,
      and force field parameters. It's particularly useful for continuing simulations from a
      previous state or for setting up complex initial configurations.
      <p>
      The model reads all necessary information from the input file, including:
      - Particle types and their properties
      <p>
      - Particle positions and other state variables
      <p>
      - Structure information (particle IDs, types, etc.)
      <p>
      - Force field parameters and interactions
      <p>
      This approach provides flexibility in setting up simulations, as users can manually create
      or modify the input files to achieve specific initial conditions or system configurations.
      It also allows for easy sharing and reproduction of simulation setups.
      <p>
      The FILE model includes an option to selectively remove certain types of interactions from
      the imported force field.",
     "parameters":{
        "inputFilePath":{"description":"Path to the JSON file containing the complete simulation setup.",
                         "type":"str"},
        "removeInteractionsByType":{"description":"List of interaction types to remove from the imported force field.",
                                    "type":"list of str",
                                    "default":null}
     },
     "example":"
         {
            \"type\":\"FILE\",
            \"parameters\":{
                \"inputFilePath\":\"path/to/simulation.json\",
                \"removeInteractionsByType\":[\"Bond2\", \"NonBonded\"]
            }
         }
        "
    }
    """

    availableParameters = {"inputFilePath", "removeInteractionsByType"}
    requiredParameters  = {"inputFilePath"}
    definedSelections   = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        inputFilePath = params["inputFilePath"]
        with open(inputFilePath, 'r') as file:
            simulation = json.load(file)

        # Sub inputFilePath by inputSimulation in parameters
        params["inputSimulation"] = copy.deepcopy(simulation)
        del params["inputFilePath"]

        self.SIM = SIMULATION(name+"_SIM",**params)

        self.setState(self.SIM.getState())
        self.setStructure(self.SIM.getStructure())
        self.setForceField(self.SIM.getForceField())

    def processSelection(self,selectionType,selectionOptions):
        sel = self.SIM.processSelection(selectionType,selectionOptions)
        return sel
