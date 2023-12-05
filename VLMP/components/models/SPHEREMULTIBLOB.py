from VLMP.components.models import modelBase

import numpy as np
#from scipy.spatial import cKDTree

from icosphere import icosphere

class SPHEREMULTIBLOB(modelBase):
    """
    Component name: SPHEREMULTIBLOB
    Component type: model

    Author: Pablo Ibáñez-Freire and Pablo Palacios-Alonso
    Date: 18/07/2023

    Extension of Icosidodecahedron + icosphere
    """

    def __even_permutation(self, a, b, c, pos, i1):
        pos[i1, :] = [a, b, c]
        pos[i1 + 1, :] = [c, a, b]
        pos[i1 + 2, :] = [b, c, a]

    def __vertex_distances(self, NV, pos, iout):
        dmin = 10. ** 10
        for i in range(NV):
            for j in range(i + 1, NV):
                r1 = pos[i, :]
                r2 = pos[j, :]
                dist = self.__distance(r1, r2)
                if dist < dmin:
                    dmin = dist
        return dmin

    def __distance(self, r1, r2):
        dist = np.sum((r1 - r2) ** 2)
        return np.sqrt(dist)

    def __radius(self, nv, pos):
        r2 = pos[nv, :]  # center
        dists = np.zeros(nv, dtype=float)
        for i in range(nv):
            r1 = pos[i, :]
            dists[i] = self.__distance(r1, r2)
        return np.max(dists)


    def __sphere(self, rSphere):

        if self.sphereType == "icosphere":

            mu = int(np.sqrt(0.1*(self.sphN-12)+1))
            N    = 12+10*(mu**2-1)
            Nmax = 12+10*((mu+1)**2-1)

            if self.sphN != N:
                self.logger.error(f"The given number of spheres for sphere multiblob ({self.sphN}) is not valid for icosphere."
                                  f"The lower valid number is {N} and the upper valid number is {Nmax}.")
                raise Exception("Invalid number of spheres for icosphere")

            pos, _ = icosphere(mu)
            pos   *= rSphere

            edgeIco    = rSphere/np.sin(2*np.pi/5)
            edgeLength = edgeIco/mu

        elif self.sphereType == "icosidodecahedron":

            if self.sphN != 30:
                self.logger.error("Number of particles for icosidodecahedron must be 30")
                raise Exception("Number of particles for icosidodecahedron must be 30")

            goldenRatio = (1.0 + np.sqrt(5.0))/2.0

            pos = np.zeros((self.sphN+1, 3), dtype=float)
            ic  = np.zeros(self.sphN+1, dtype=int)
            edgeLength = rSphere / goldenRatio

            a = 0
            b = 0
            c = goldenRatio
            cm = -c
            self.__even_permutation(a, b, c, pos, 0)
            self.__even_permutation(a, b, cm, pos, 3)

            a = 0.5
            b = goldenRatio / 2.0
            c = (goldenRatio + 1.) / 2.
            am = -a
            bm = -b
            cm = -c

            self.__even_permutation(a, b, c, pos, 6)
            self.__even_permutation(am, b, c, pos, 9)
            self.__even_permutation(a, bm, c, pos, 12)
            self.__even_permutation(a, b, cm, pos, 15)
            self.__even_permutation(am, bm, c, pos, 18)
            self.__even_permutation(am, b, cm, pos, 21)
            self.__even_permutation(a, bm, cm, pos, 24)
            self.__even_permutation(am, bm, cm, pos, 27)

            ic[0] = 2
            ic[6] = 3
            ic[9] = 3
            ic[12] = 3
            ic[18] = 3
            pos = edgeLength * pos

        else:
            self.logger.error("Sphere type not recognized")
            raise Exception("Sphere type not recognized")

        return pos, edgeLength

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"sphereType",
                                                "particleName",
                                                "particleMass","particleRadius","particleCharge",
                                                "numberOfSpheres",
                                                "particlesPerSphere",
                                                "radiusOfSphere",
                                                "K",
                                                "heightMean","heightStd",
                                                "heightReference"},
                         requiredParameters  = {"K"},
                         definedSelections   = {"particleId"},
                         **params)

        ############################################################

        self.sphereType  = params.get("sphereType", "icosidodecahedron")

        if self.sphereType not in ["icosphere","icosidodecahedron"]:
            self.logger.error("Sphere type not recognized")
            raise Exception("Sphere type not recognized")

        self.sphN        = params.get("particlesPerSphere",31)

        particleName = params.get("particleName","A")

        numberOfSpheres = params.get("numberOfSpheres",1)
        radiusOfSphere  = params.get("radiusOfSphere",1.0)

        heightMean = params.get("heightMean",0.0)
        heightStd  = params.get("heightStd",0.0)

        heightReference = params.get("heightReference",0.0)

        box = self.getEnsemble().getEnsembleComponent("box")

        self.maxTries    = params.get("maxTries",100)

        #TODO: apply pbc, now box size is reduced by 2*radiusOfSphere

        X = (box[0]-2*radiusOfSphere)/2
        Y = (box[1]-2*radiusOfSphere)/2

        #X = box[0]/2.0
        #Y = box[1]/2.0

        #Check box height and genration height
        Z = box[2]/2.0
        if heightReference > Z or heightReference < -Z:
            self.logger.error(f"Height reference is out of box {heightReference} > {Z} or {heightReference} < {-Z}")
            raise ValueError("Height reference is out of box")

        if heightMean + heightReference > Z or heightMean + heightReference < -Z:
            self.logger.error(f"Generation height is out of box {heightMean + heightReference} > {Z} or "
                              f"{heightMean + heightReference} < {-Z}")
            raise ValueError("Generation height is out of box")

        ############################################################

        sphPositions = []

        i=0
        tries=0
        while i < numberOfSpheres:
            tries+=1
            if tries >= self.maxTries*numberOfSpheres:
                self.logger.error("Unable to find a correct configuration")
                raise ValueError("The number of spheres is too high for the box size")
            if heightStd > 0.0:
                height = np.random.normal(heightMean,heightStd)
            else:
                height = heightMean
            height += heightReference

            x = np.random.uniform(-X,X)
            y = np.random.uniform(-Y,Y)

            center = [x,y,height]

            if height > Z - radiusOfSphere or height < -Z + radiusOfSphere:
                continue

            if sphPositions:
                #minDst,minDstIndex = cKDTree(sphPositions).query(center, 1)
                minDst = np.inf
                for p in sphPositions:
                    dst = np.linalg.norm(p-np.asarray(center))
                    minDst = min(dst,minDst)

            else:
                minDst = np.inf

            if minDst > 2.0*radiusOfSphere*1.1:
                sphPositions.append(center)
                i+=1

        # Generate spheres

        state = {}
        state["labels"]=["id","position"]
        state["data"]  =[]

        idCounter = 0
        sph2ids = []
        sph2pos = []
        for center in sphPositions:
            pos, edgeLength = self.__sphere(radiusOfSphere)
            pos += center
            ids = []
            for p in pos:
                state["data"].append([idCounter,list(p)])
                ids.append(idCounter)
                idCounter += 1
            sph2ids.append(ids.copy())
            sph2pos.append(pos.copy())

        
        particleMass   = params.get("particleMass",1.0)
        particleRadius = params["particleRadius"]
        particleCharge = params.get("particleCharge",0.0)

        K = params["K"]
        
        types = self.getTypes()
        types.addType(name = particleName,
                      mass = particleMass,
                      radius = particleRadius,
                      charge = particleCharge)

        
        structure = {}
        structure["labels"] = ["id", "type", "modelId"]
        structure["data"]   = []

        for i in range(numberOfSpheres):
            for j in sph2ids[i]:
                structure["data"].append([j,particleName,i])

        forceField = {}
        forceField["Bond"] = {}
        forceField["Bond"]["parameters"] = {}
        forceField["Bond"]["type"] = ["Bond2", "Harmonic"]
        forceField["Bond"]["labels"] = ["id_i", "id_j", "K", "r0"]
        forceField["Bond"]["data"] = []

        bonds = []
        for i in range(numberOfSpheres):
            for n in range(self.sphN):
                for m in range(n + 1, self.sphN):
                    pn = sph2pos[i][n]
                    pm = sph2pos[i][m]

                    dst = np.linalg.norm(pn - pm)

                    if dst < 1.75 * edgeLength:
                        bonds.append([sph2ids[i][n], sph2ids[i][m], K, dst])

        for i,j,k,r0 in bonds:
            forceField["Bond"]["data"].append([i,j,k,r0])

        ############################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,**params):

        sel = []
        if "particleId" in params:
            sel += params["particleId"]
        return sel

