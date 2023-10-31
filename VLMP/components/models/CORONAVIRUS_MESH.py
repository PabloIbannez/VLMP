from VLMP.components.models import modelBase

from VLMP.components.models.ICOSPHERE import ICOSPHERE

import numpy as np

class CORONAVIRUS_MESH(modelBase):
    """
    Component name: CORONAVIRUS_MESH
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 26/10/2023
    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"particleName",
                                                "particleMass","particleRadius","particleCharge",
                                                "position",
                                                "resolution",
                                                "radius",
                                                "Kb",
                                                "Kd",
                                                "steric",
                                                "surface",
                                                "surfacePosition",
                                                "surfaceEpsilon_kT"},
                         requiredParameters  = {"particleName"},
                         definedSelections   = {"particleId"},
                         **params)

        ############################################################

        paramsICO = params.copy()

        # Remove parameters that are not needed for ICOSPHERE
        paramsICO.pop("surface")
        paramsICO.pop("surfacePosition")
        paramsICO.pop("surfaceEpsilon_kT")

        self.SPHERE = ICOSPHERE(name = name + "_sphere",
                                **paramsICO)

        units      = self.getUnits()

        types      = self.SPHERE.getTypes()
        state      = self.SPHERE.getState()
        structure  = self.SPHERE.getStructure()
        forceField = self.SPHERE.getForceField()

        surface = params.get("surface",False)
        if surface:
            surfaceEpsilon  = params["surfaceEpsilon_kT"]*units.getConstant("kT")
            surfacePosition = params["surfacePosition"]

        ############################################################

        if surface:

            forceField["surface"] = {}
            forceField["surface"]["type"]       = ["Surface", "SurfaceGeneralLennardJonesType2"]
            forceField["surface"]["parameters"] = {"surfacePosition":surfacePosition}
            forceField["surface"]["labels"] = ["name","epsilon","sigma"]
            forceField["surface"]["data"]   = []

            for tn,tinfo in types.getTypes().items():
                forceField["surface"]["data"].append([tinfo["name"],surfaceEpsilon,tinfo["radius"]])

        ############################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,**params):

        sel = self.SPHERE.processSelection(**params)

        return sel

