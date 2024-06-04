from VLMP.components.models import modelBase

class polarizableParticle(modelBase):
    """
    Component name: POLARIZABLE_PARTILCE
    Component type: model

    Author: Pablo Diez-Silva
    Date: 12/05/2024

    Single polarizable particle model.

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"particleName",
                                                "particleMass","particleRadius","particleCharge","particlePolarizability",
                                                "particleNumber","position"},
                         requiredParameters  = {"particleName"},
                         definedSelections   = {"particleId"},
                         **params)

        ############################################################

        particleName = params["particleName"]
        particleNumber = params.get("particleNumber",1)

        particleMass   = params.get("particleMass",1.0)
        particleRadius = params.get("particleRadius",1.0)
        particleCharge = params.get("particleCharge",0.0)
        particlePolarizability = params.get("particlePolarizability",0.0)

        types = self.getTypes()
        types.addType(name = particleName,
                      mass = particleMass,
                      radius = particleRadius,
                      charge = particleCharge,
                      polarizability = particlePolarizability)

        state = {}
        state["labels"] = ["id","position"]

        particlePosition = params.get("position",[[0.0,0.0,0.0]]*particleNumber)
        state["data"] = [[i,particlePosition[i]] for i in range(particleNumber)]

        structure = {}
        structure["labels"] = ["id","modelId","type"]
        structure["data"] = [[i,i,particleName] for i in range(particleNumber)]

        ############################################################

        self.setState(state)
        self.setStructure(structure)


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += [0]

        return sel

