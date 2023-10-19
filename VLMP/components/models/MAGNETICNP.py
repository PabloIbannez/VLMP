from VLMP.components.models import modelBase

import numpy as np
#from scipy.spatial import cKDTree

from icosphere import icosphere

class MAGNETICNP(modelBase):
    """
    Component name: MAGNETICNP
    Component type: model

    Author: P. Palacios-Alonso
    Date: 16/10/2023

    Model of magnetic nanoparticles
    """

    def __generateLogNormalDistribution(self, mean, std, N):
        distribution = np.full(N, mean)

        if (std>0.0):
            mean2 = mean*mean;
            std2  = std*std;

            sigma = (np.log(1+std2/(mean2)))**0.5;
            mu    = np.log(mean2/(mean2+std2)**0.5);

            distribution = np.random.lognormal(mean  = mu,
                                               sigma = sigma,
                                               size  = N)
        return distribution


    def __axisToQuaternion(self, axis):
        # Normalize the axis
        axis = axis / np.sqrt(np.dot(axis, axis))
        #When axis is parallel to u_z, v is zero and the have to be computed in a different way.
        if axis[2] == 1.0:
            return np.array([1.0, 0.0, 0.0, 0.0])
        if axis[2] == -1.0:
            return np.array([0.0, 1.0, 0.0, 0.0])

        phi = np.arccos(axis[2])
        # u_z x axis (cross product)

        v = np.array([-axis[1], axis[0], 0.0])
        v = v / np.sqrt(1 - axis[2]**2)

        # Compute sin and cos of phi/2
        sphi_2 = np.sin(phi * 0.5)
        cphi_2 = np.cos(phi * 0.5)

        qdir = np.array([cphi_2, sphi_2 * v[0], sphi_2 * v[1], sphi_2 * v[2]])
        return qdir


    def __generateRandomQuaternions(self, N):
        x0 = np.random.rand(N)
        r1 = np.sqrt(1.0-x0);
        r2 = np.sqrt(x0);
        ang1 = 2*np.pi*np.random.rand(N)
        ang2 = 2*np.pi*np.random.rand(N)
        return np.column_stack((r2*np.cos(ang2),
                                r1*np.sin(ang1),
                                r1*np.cos(ang1),
                                r2*np.sin(ang2)))



    def __generateInitialOrientations(self, N, mode, axis = [0,0,1]):
        if mode == "aligned":
            axis       = np.array(axis)
            quaternion = self.__axisToQuaternion(axis)
            qdirs      = np.tile(quaternion, (N, 1))
        elif mode == "random":
            qdirs = self.__generateRandomQuaternions(N)
        else:
            self.logger.error(f"[MAGNETICNP] Initial orientation {mode} not valid")
            raise Exception("Initial orientation not available")

        return qdirs

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"particleName",
                                                "nParticles",
                                                "msat",
                                                "anisotropy",
                                                "anisotropyStd",
                                                "coreRadius",
                                                "coreRadiusStd",
                                                "coatingWidth",
                                                "coatingWidthStd",
                                                "initOrientation",
                                                "initAxis"},
                         requiredParameters  = {"nParticles", "msat", "coreRadius"},
                         definedSelections   = {"particleId"},
                         **params)

        ############################################################

        partName = params.get("particleName", "A")

        msat           = params["msat"]
        coreRadiusMean = params["coreRadius"]
        nParticles     = params["nParticles"]

        anisotropyMean   = params.get("anisotropy"     , None)
        anisotropyStd    = params.get("anisotropyStd"  , 0.0)
        coreRadiusStd    = params.get("coreRadiusStd"  , 0.0)
        coatingWidthMean = params.get("coatingWidth"   , 0.0)
        coatingWidthStd  = params.get("coatingWidthStd", 0.0)
        initOrientation  = params.get("initOrientation", "aligned")
        initAxis         = params.get("initAxis"       , [0,0,1])

        coreRadius   = self.__generateLogNormalDistribution(coreRadiusMean,
                                                            coreRadiusStd,
                                                            nParticles)

        coatingWidth = self.__generateLogNormalDistribution(coatingWidthMean,
                                                            coatingWidthStd,
                                                            nParticles)

        magneticMoment     = 4./3.*np.pi*coreRadius**3*msat
        hydrodynamicRadius = coreRadius + coatingWidth

        if anisotropyMean is not None:
            anisotropy = self.__generateLogNormalDistribution(anisotropyMean,
                                                              anisotropyStd,
                                                              nParticles)



        directions = self.__generateInitialOrientations(nParticles, initOrientation, initAxis)
        types = self.getTypes()
        types.addType(name = partName)

        state = {}
        if anisotropyMean is not None:
            state["labels"] = ["id", "radius", "position", "direction", "magnetization", "anisotropy"]
            state["data"]   = []
            for i in range(nParticles):
                state["data"].append([i,
                                      hydrodynamicRadius[i],
                                      [0,0,0], directions[i].tolist(),
                                      [0,0,1,magneticMoment[i]],
                                      anisotropy[i]])
        else:
            state["labels"] = ["id", "radius", "position", "direction", "magnetization"]
            state["data"] = []
            for i in range(nParticles):
                state["data"].append([i,
                                      hydrodynamicRadius[i],
                                      [0,0,0], directions[i].tolist(),
                                      [0,0,1,magneticMoment[i]]])
        structure = {}
        structure["labels"] = ["id","type"]
        structure["data"] = []
        for i in range(nParticles):
            structure["data"].append([i,partName])


        #Generate forceField

        self.setState(state)
        self.setStructure(structure)

    def processSelection(self,**params):

        sel = []
        if "particleId" in params:
            sel += params["particleId"]
        return sel
