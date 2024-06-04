from VLMP.components.modelExtensions import modelExtensionBase

class helixBoundaries(modelExtensionBase):

    """
    Component name: helixBoundaries
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 03/06/2024

    :param helixPitch: pitch of the helix
    :type helixPitch: float
    :param helixRadius: radius of the helix
    :type helixRadius: float
    :param eps: helix sign, 1 for right-handed, -1 for left-handed
    :type eps: float
    :param nTurns: number of turns of the helix
    :type nTurns: int
    :param nPointsHelix: number of points to discretize the helix
    :type nPointsHelix: int
    :param helixInnerRadius: inner radius of the helix
    :type helixInnerRadius: float
    :param nx: number of points in the x direction
    :type nx: int
    :param ny: number of points in the y direction
    :type ny: int
    :param nz: number of points in the z direction
    :type nz: int
    :param K: spring constant for boundary conditions
    :type K: float

    """

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name = name,
                         availableParameters = {"helixPitch","helixRadius",
                                                "eps","nTurns",
                                                "nPointsHelix","helixInnerRadius","K",
                                                "nx","ny","nz"},
                         requiredParameters  = {"helixPitch","helixRadius",
                                                "eps","nTurns",
                                                "nPointsHelix","helixInnerRadius","K",
                                                "nx","ny","nz"},
                         availableSelections = {"selection"},
                         requiredSelections  = set(),
                         **params)

        ############################################################
        ############################################################
        ############################################################

        helixPitch  = params["helixPitch"]
        helixRadius = params["helixRadius"]
        if not isinstance(helixPitch,float):
            self.logger.error("Invalid value for helixPitch. It must be a float")
            raise ValueError("Invalid value for helixPitch")
        if not isinstance(helixRadius,float):
            self.logger.error("Invalid value for helixRadius. It must be a float")
            raise ValueError("Invalid value for helixRadius")

        eps = params["eps"]
        eps = float(eps)

        if eps not in [-1.0,1.0]:
            self.logger.error("Invalid value for eps. It must be either 1.0 or -1.0")
            raise ValueError("Invalid value for eps")

        nTurns = params["nTurns"]
        #Check if nTurns is an integer
        if not isinstance(nTurns,int):
            self.logger.error("Invalid value for nTurns. It must be an integer")
            raise ValueError("Invalid value for nTurns")

        nPointsHelix = params["nPointsHelix"]
        #Check if nPointsHelix is an integer
        if not isinstance(nPointsHelix,int):
            self.logger.error("Invalid value for nPointsHelix. It must be an integer")
            raise ValueError("Invalid value for nPointsHelix")

        helixInnerRadius = params["helixInnerRadius"]
        #Check if helixInnerRadius is a float
        if not isinstance(helixInnerRadius,float):
            self.logger.error("Invalid value for helixInnerRadius. It must be a float")
            raise ValueError("Invalid value for helixInnerRadius")

        K = params["K"]
        #Check if K is a float
        if not isinstance(K,float):
            self.logger.error("Invalid value for K. It must be a float")
            raise ValueError("Invalid value for K")

        nx = params["nx"]
        ny = params["ny"]
        nz = params["nz"]

        #Check if nx, ny and nz are integers
        if not isinstance(nx,int):
            self.logger.error("Invalid value for nx. It must be an integer")
            raise ValueError("Invalid value for nx")
        if not isinstance(ny,int):
            self.logger.error("Invalid value for ny. It must be an integer")
            raise ValueError("Invalid value for ny")
        if not isinstance(nz,int):
            self.logger.error("Invalid value for nz. It must be an integer")
            raise ValueError("Invalid value for nz")

        if "selection" in params:
            self.setGroup("selection")

        ############################################################

        extension = {}

        extension[name] = {}
        extension[name]["type"] = ["External","HelixBoundaries"]
        extension[name]["parameters"] = {"helixPitch":helixPitch,
                                         "helixRadius":helixRadius,
                                         "eps":eps,
                                         "nTurns":nTurns,
                                         "nPointsHelix":nPointsHelix,
                                         "helixInnerRadius":helixInnerRadius,
                                         "nx":nx,"ny":ny,"nz":nz,
                                         "K":K}

        ############################################################

        self.setExtension(extension)
