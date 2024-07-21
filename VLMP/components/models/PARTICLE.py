from VLMP.components.models import modelBase

class PARTICLE(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire",
     "description":
     "PARTICLE model for creating a single particle in a simulation. This simple model allows
      users to add a single particle with specified properties to the simulation environment.
      It's particularly useful for creating reference points, probes, or simple objects within
      a larger simulation context.
      <p>
      The model allows customization of various particle properties including:
      <p>
      - Name (type) of the particle
      <p>
      - Mass
      <p>
      - Radius
      <p>
      - Charge
      <p>
      - Initial position
      <p>
      This model can be used in conjunction with other models to create more complex systems.
      It's especially useful for testing
      and debugging purposes, or for creating simple scenarios to study specific interactions
      or behaviors.",
     "parameters":{
        "particleName":{"description":"Name or type of the particle.",
                        "type":"str"},
        "particleMass":{"description":"Mass of the particle.",
                        "type":"float",
                        "default":1.0},
        "particleRadius":{"description":"Radius of the particle.",
                          "type":"float",
                          "default":1.0},
        "particleCharge":{"description":"Charge of the particle.",
                          "type":"float",
                          "default":0.0},
        "position":{"description":"Initial position of the particle in 3D space.",
                    "type":"list of float",
                    "default":[0.0, 0.0, 0.0]}
     },
     "example":"
         {
            \"type\":\"PARTICLE\",
            \"parameters\":{
                \"particleName\":\"probe\",
                \"particleMass\":2.5,
                \"particleRadius\":0.5,
                \"particleCharge\":-1.0,
                \"position\":[10.0, 0.0, 5.0]
            }
         }
        "
    }
    """

    availableParameters = {"particleName",
                           "particleMass","particleRadius","particleCharge",
                           "position"}
    requiredParameters  = {"particleName"}
    definedSelections   = set()

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
                         **params)

        ############################################################

        particleName = params["particleName"]

        particleMass   = params.get("particleMass",1.0)
        particleRadius = params.get("particleRadius",1.0)
        particleCharge = params.get("particleCharge",0.0)

        types = self.getTypes()
        types.addType(name = particleName,
                      mass = particleMass,
                      radius = particleRadius,
                      charge = particleCharge)

        state = {}
        state["labels"] = ["id","position"]

        particlePosition = params.get("position",[0.0,0.0,0.0])
        state["data"] = [[0,particlePosition]]

        structure = {}
        structure["labels"] = ["id","type"]
        structure["data"] = [[0,particleName]]

        ############################################################

        self.setState(state)
        self.setStructure(structure)


    def processSelection(self,selectionType,selectionOptions):
        return None

