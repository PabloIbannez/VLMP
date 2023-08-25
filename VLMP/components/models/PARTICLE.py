from VLMP.components.models import modelBase

class PARTICLE(modelBase):
    """
    Component name: PARTILCE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 18/06/2023

    Single particle model.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"particleName",
                                                "particleMass","particleRadius","particleCharge",
                                                "position"},
                         requiredParameters  = {"particleName"},
                         definedSelections   = {"particleId"},
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


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += [0]

        return sel

