from VLMP.components.models import modelBase

import copy

class SIMULATION(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "SIMULATION model for loading pre-existing simulation configurations. This model allows users to
      import a complete simulation setup from a pyUAMMD simulation object, including particle positions, types,
      and force field parameters. It's particularly useful for continuing simulations from a
      previous state or for setting up complex initial configurations.
      <p>
      The model takes all necessary information from imported simulation object, including:
      - Particle types and their properties
      <p>
      - Particle positions and other state variables
      <p>
      - Structure information (particle IDs, types, etc.)
      <p>
      - Force field parameters and interactions
      <p>
      The SIMULATION model includes an option to selectively remove certain types of interactions from
      the imported simualtion.",
     "parameters":{
        "inputSimulation":{"description":"Simulation object to import. This object should contain all necessary information to set up the simulation.",
                           "type":"str"},
        "removeInteractionsByType":{"description":"List of interaction types to remove from the imported simulation.",
                                    "type":"list of str",
                                    "default":null}
     },
     "example":"
         {
            \"type\":\"SIMULATION\",
            \"parameters\":{
                \"inputSimulation\":\"simulationObject\",
                \"removeInteractionsByType\":[\"Bond2\", \"NonBonded\"]
            }
         }
        "
    }
    """

    availableParameters = {"inputSimulation","removeInteractionsByType"}
    requiredParameters  = {"inputSimulation"}
    definedSelections   = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        ############################################################

        inputSimulation = params["inputSimulation"]
        self.logger.info(f"[SIMULATION] Created model from pyUAMMD simulation")

        ########################################################

        # TYPES

        types = self.getTypes()

        typesLabels = inputSimulation["global"]["types"]["labels"]
        for typ in inputSimulation["global"]["types"]["data"]:
            typInfo = {l:typ[i] for i,l in enumerate(typesLabels)}
            types.addType(**typInfo)

        #Generate positions, a line along the z axis
        state = copy.deepcopy(inputSimulation["state"])

        #Generate structure
        structure = copy.deepcopy(inputSimulation["topology"]["structure"])

        #Generate forceField
        forceField = copy.deepcopy(inputSimulation["topology"]["forceField"])

        #Remove interactions by type
        if "removeInteractionsByType" in params:
            entriesToRemove = []
            for interaction in forceField:
                tpy = forceField[interaction]["type"][0]
                if tpy in params["removeInteractionsByType"]:
                    entriesToRemove.append(interaction)

            for interaction in entriesToRemove:
                _ = forceField.pop(interaction)
                self.logger.debug(f"[SIMULATION] Removing interaction {interaction} due to type: {tpy}")

        ########################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,selectionType,selectionOptions):
        return None
