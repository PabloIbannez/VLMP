from VLMP.components.modelOperations import modelOperationBase

import numpy as np

class setParticleXYPosition(modelOperationBase):

    """
    Component name: setParticleXYPosition
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 26/02/2024

    Set the XY particle position to value.

    :param position: Position to set the XY particle to.
    :type position: float list
    :param considerRadius: Consider particle radius when setting the XY position.
    :type considerRadius: bool, optional

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"position"},
                         requiredParameters  = {"position"},
                         availableSelections = {"selection"},
                         requiredSelections  = {"selection"},
                         **params)

        ############################################################
        ############################################################
        ############################################################

        # Check if the given position is a list of two floats
        if not isinstance(params["position"],list) or len(params["position"]) != 2:
            self.logger.error("The given position must be a list of two floats.")
            raise Exception("Parameter bad format")

        targetPosition = params["position"]

        selectedIds = self.getSelection("selection")
        pos = np.asarray(self.getIdsState(selectedIds,"position"))

        for i in range(len(selectedIds)):
            pos[i][0] = targetPosition[0]
            pos[i][1] = targetPosition[1]

        self.setIdsState(selectedIds,"position",pos.tolist())
