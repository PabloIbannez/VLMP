from VLMP.components.modelExtensions import modelExtensionBase

import numpy as np
from scipy.optimize import fsolve

class surfaceMaxForce(modelExtensionBase):
    """
    {
        "author": "Pablo Ibáñez-Freire",
        "description": "Implements a surface interaction with a maximum force constraint.",
        "parameters": {
            "epsilon": {"description": "Energy parameter for surface-particle interaction", "type": "float", "default": null},
            "surfacePosition": {"description": "Z-coordinate of the surface", "type": "float", "default": null},
            "maxForce": {"description": "Maximum force allowed in the interaction", "type": "float", "default": null}
        },
        "selections": {
            "selection": {"description": "Particles interacting with the surface", "type": "list of ids"}
        },
        "example": "
        {
            \"type\": \"surfaceMaxForce\",
            \"parameters\": {
                \"epsilon\": 1.0,
                \"surfacePosition\": -10.0,
                \"maxForce\": 100.0,
                \"selection\": \"model1 all\"
            }
        }"
    }
    """

    availableParameters = {"epsilon",
                           "maxForce",
                           "surfacePosition"}
    requiredParameters  = {"surfacePosition",
                           "maxForce"}
    availableSelections = {"selection"}
    requiredSelections  = set()

    def __LJtype2_maxForce_fit(self, sigma, radius, epsilon, maxForce):
        return (12.0*epsilon*((sigma/radius)**12 - (sigma/radius)**6)*(1.0/radius) - maxForce)**2

    def __init__(self,name,**params):
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

        surfacePosition = params.get("surfacePosition",0.0)
        epsilon         = params.get("epsilon",1.0)
        maxForce        = params.get("maxForce",1.0)

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["Surface","SurfaceGeneralLennardJonesType2"]
        extension[name]["parameters"] = {"surfacePosition":surfacePosition}

        extension[name]["labels"] = ["name","epsilon","sigma"]
        extension[name]["data"] = []

        types = self.getTypes()
        for typ,info in types.getTypes().items():
            radius = info["radius"]

            sgm = radius*np.power(maxForce*radius/(12.0*abs(epsilon)), 1/12) #Tentative sigma
            sgm,_,ier,msg = fsolve(self.__LJtype2_maxForce_fit, sgm, args=(radius, abs(epsilon), maxForce), full_output=True)

            if ier != 1:

                maxForceSteps = np.linspace(maxForce/4.0, maxForce, 10)
                for mFS in maxForceSteps:
                    sgm = radius*np.power(mFS*radius/(12.0*abs(epsilon)), 1/12)
                    sgm,_,ier,msg = fsolve(self.__LJtype2_maxForce_fit, sgm, args=(radius, abs(epsilon), mFS), full_output=True)

                    if ier == 1:
                        break

                if ier != 1:
                    self.logger.error(f"[ModelExtension] (surfaceMaxForce) Could not find sigma for type {typ}. Message: {msg}")
                    raise Exception("Error in sigma calculation")

            sgm = sgm[0]
            self.logger.debug(f"[ModelExtension] (surfaceMaxForce) Sigma for type {typ} with radius {radius} is {sgm}")

            extension[name]["data"].append([typ,epsilon,round(sgm,2)])

        ############################################################

        self.setExtension(extension)
