from VLMP.components.models import modelBase

import numpy as np
from scipy.spatial import cKDTree

class ICOSIDODECAHEDRON(modelBase):
    """
    Component name: ICOSIDODECAHEDRON
    Component type: model

    Author: Pablo Ibáñez-Freire and Pablo Palacios-Alonso
    Date: 18/07/2023

    Icosidodecahedron model: https://en.wikipedia.org/wiki/Icosidodecahedron.
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


    def __icosahedron(self, amp):

        if self.icoN != 31:
            self.logger.error("Number of particles must be 31")
            #Not implemented yet
            raise NotImplementedError

        pos = np.zeros((self.icoN, 3), dtype=float)
        ic = np.zeros(self.icoN, dtype=int)

        fac = amp  # vertex distance

        a = 0
        b = 0
        c = self.goldenRatio
        cm = -c
        self.__even_permutation(a, b, c, pos, 0)
        self.__even_permutation(a, b, cm, pos, 3)

        a = 0.5
        b = self.goldenRatio / 2.0
        c = (self.goldenRatio + 1.) / 2.
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

        pos[30, :] = 0  # central
        ic[0] = 2
        ic[6] = 3
        ic[9] = 3
        ic[12] = 3
        ic[18] = 3
        pos = fac * pos

        dvertex = self.__vertex_distances(30, pos, 23)
        rad = self.__radius(30, pos)
        return pos, rad

    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = {"particleName","particleMass","particleRadius","particleCharge",
                                                "numberOfIcosidodecahedrons",
                                                "particlesPerIcosidodecahedron",
                                                "radiusOfIcosidodecahedron",
                                                "K",
                                                "box",
                                                "heightMean","heightStd",
                                                "heightReference"},
                         requiredParameters  = {"K"},
                         definedSelections   = {"particleId"},
                         **params)

        self.goldenRatio = (1.0 + np.sqrt(5.0))/2.0

        ############################################################

        self.icoN        = params.get("particlesPerIcosidodecahedron",31)

        particleName = params.get("particleName","A")

        particleMass   = params.get("particleMass",1.0)
        particleRadius = params.get("particleRadius",1.0)
        particleCharge = params.get("particleCharge",0.0)

        types = self.getTypes()
        types.addType(name = particleName,
                      mass = particleMass,
                      radius = particleRadius,
                      charge = particleCharge)

        numberOfIcosidodecahedrons = params.get("numberOfIcosidodecahedrons",1)
        radiusOfIcosidodecahedron  = params.get("radiusOfIcosidodecahedron",1.0)

        K = params["K"]

        heightMean = params.get("heightMean",0.0)
        heightStd  = params.get("heightStd",0.0)

        heightReference = params.get("heightReference",0.0)

        box = params.get("box",[0.0,0.0,0.0])

        #TODO: apply pbc, now box size is reduced by 2*radiusOfIcosidodecahedron

        X = (box[0]-2*radiusOfIcosidodecahedron)/2
        Y = (box[1]-2*radiusOfIcosidodecahedron)/2

        #X = box[0]/2.0
        #Y = box[1]/2.0

        #Check box height and genration height
        Z = box[2]/2.0
        if heightReference > Z or heightReference < -Z:
            self.logger.error(f"Height reference is out of box {heightReference} > {Z} or {heightReference} < {-Z}")
            raise ValueError("Height reference is out of box")

        if heightMean + heightReference > Z or heightMean + heightReference < -Z:
            self.logger.error(f"Generation height is out of box {heightMean + heightReference} > {Z} or {heightMean + heightReference} < {-Z}")
            raise ValueError("Generation height is out of box")

        ############################################################

        icoPositions = []

        i=0;
        while i < numberOfIcosidodecahedrons:

            if heightStd > 0.0:
                height = np.random.normal(heightMean,heightStd)
            else:
                height = heightMean
            height += heightReference

            x = np.random.uniform(-X,X)
            y = np.random.uniform(-Y,Y)

            center = [x,y,height]

            if height > Z - radiusOfIcosidodecahedron or height < -Z + radiusOfIcosidodecahedron:
                continue

            if icoPositions:
                minDst,minDstIndex = cKDTree(icoPositions).query(center, 1)
            else:
                minDst = np.inf

            if minDst > 2.0*radiusOfIcosidodecahedron*1.05:
                icoPositions.append(center)
                i+=1

        # Generate icosidodecahedrons
        edgeLength = radiusOfIcosidodecahedron / self.goldenRatio

        state = {}
        state["labels"]=["id","position"]
        state["data"]  =[]

        idCounter = 0
        ico2ids = []
        ico2pos = []
        for center in icoPositions:
            pos, _ = self.__icosahedron(edgeLength)
            pos += center
            ids = []
            for p in pos:
                state["data"].append([idCounter,list(p)])
                ids.append(idCounter)
                idCounter += 1
            ico2ids.append(ids.copy())
            ico2pos.append(pos.copy())

        structure = {}
        structure["labels"] = ["id", "type", "modelId"]
        structure["data"]   = []

        for i in range(numberOfIcosidodecahedrons):
            for j in ico2ids[i]:
                structure["data"].append([j,particleName,i])

        forceField = {}
        forceField["Bond"] = {}
        forceField["Bond"]["parameters"] = {}
        forceField["Bond"]["type"] = ["Bond2", "Harmonic"]
        forceField["Bond"]["labels"] = ["id_i", "id_j", "K", "r0"]
        forceField["Bond"]["data"] = []

        bonds = []
        for i in range(numberOfIcosidodecahedrons):
            for n in range(self.icoN):
                for m in range(n + 1, self.icoN):
                    pn = ico2pos[i][n]
                    pm = ico2pos[i][m]

                    dst = np.linalg.norm(pn - pm)

                    if dst < 1.05 * edgeLength:
                        bonds.append([ico2ids[i][n], ico2ids[i][m], K, edgeLength])

            #All particles are bonded to central particle, which is the last one
            for j in ico2ids[i][:-1]:
                bonds.append([ico2ids[i][-1], j, K, radiusOfIcosidodecahedron])

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

