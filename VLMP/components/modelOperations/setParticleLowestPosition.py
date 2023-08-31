from VLMP.components.modelOperations import modelOperationBase

import numpy as np

class setParticleLowestPosition(modelOperationBase):

    """
    Component name: setParticleLowestPosition
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Set the lowest particle position to value.

    :param position: Position to set the lowest particle to.
    :type position: z coordinate, float
    :param considerRadius: Consider particle radius when setting the lowest position.
    :type considerRadius: bool, optional

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"position","considerRadius","radiusFactor"},
                         requiredParameters  = {"position"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        selectedIds = self.getSelection("selection")

        pos    = np.asarray(self.getIdsState(selectedIds,"position"))

        if params.get("considerRadius",False):
            rad = np.asarray(self.getIdsProperty(selectedIds,"radius"))
            radFactor = params.get("radiusFactor",1.0)
            rad = radFactor*rad

        # Find the lowest position
        lowestPosIndex = np.argmin(pos[:,2])
        lowestPos      = pos[lowestPosIndex,2]

        # Set the lowest position to the given value
        offset = 0.0
        if params.get("considerRadius",False):
            rad = np.asarray(self.getIdsProperty(selectedIds,"radius"))
            offset = rad[lowestPosIndex]

        translation = np.asarray([0,0,params["position"] - lowestPos + offset])

        for i in range(len(selectedIds)):
            pos[i] = pos[i] + translation

        self.setIdsState(selectedIds,"position",pos.tolist())
