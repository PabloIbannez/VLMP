from VLMP.components.models import modelBase

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

    availableParameters = {"inputFilePath","removeInteractionsByType"}
    requiredParameters  = {"inputFilePath"}
    definedSelections   = {"particleId","forceField"}

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        ############################################################

        self.inputFilePath = params["inputFilePath"]
        self.logger.info(f"[FILE] Loading model from file {self.inputFilePath}")

        ########################################################

        with open(self.inputFilePath) as f:
            inputJSON = json.load(f)

        # TYPES

        types = self.getTypes()

        typesLabels = inputJSON["global"]["types"]["labels"]
        for typ in inputJSON["global"]["types"]["data"]:
            typInfo = {l:typ[i] for i,l in enumerate(typesLabels)}
            types.addType(**typInfo)

        #Generate positions
        state = copy.deepcopy(inputJSON["state"])

        #Generate structure
        structure = copy.deepcopy(inputJSON["topology"]["structure"])

        #Generate forceField
        forceField = copy.deepcopy(inputJSON["topology"]["forceField"])

        #Remove interactions by type
        if "removeInteractionsByType" in params:
            entriesToRemove = []
            for interaction in forceField:
                tpy = forceField[interaction]["type"][0]
                if tpy in params["removeInteractionsByType"]:
                    entriesToRemove.append(interaction)

            for interaction in entriesToRemove:
                _ = forceField.pop(interaction)
                self.logger.debug(f"[FILE] Removing interaction {interaction} due to type: {tpy}")

        ########################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,selectionType,selectionOptions):
        return None
