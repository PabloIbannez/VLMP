from VLMP.components.models import modelBase

import numpy as np
from scipy.spatial import cKDTree

from icosphere import icosphere

class SPHEREMULTIBLOB(modelBase):
    """
    {"author": "Pablo Ibáñez-Freire and Pablo Palacios-Alonso",
     "description":
     "SPHEREMULTIBLOB model for creating spherical multiblob structures. This model generates
      a spherical particle represented by multiple smaller particles (blobs) arranged on its
      surface. The spherical particle can be created using either icosphere (a sphere placing
      blobs on the vertices of an icosahedron, or icosahedron iteratively subdivided) or icododecahedral
      (a sphere placing blobs on the vertices of an icosidodecahedron) geometry.
      <p>
      The model allows for the creation of spherical structures with varying levels of detail,
      making it useful for representing large spherical objects in coarse-grained simulations,
      such as colloidal particles, nanoparticles, or simplified representations of complex
      biological structures like virus capsids.
      <p>
      Key features of the SPHEREMULTIBLOB model include:
      <p>
      - Flexible control over the number of particles representing the sphere
      <p>
      - Option to use either icododecahedral or icosphere geometry
      <p>
      - Customizable particle properties (mass, radius, charge)
      <p>
      - Automatic generation of bonds between particles to maintain the spherical structure
      <p>
      - Optional steric interactions between particles
      <p>
      This model is particularly useful for studying the behavior of large spherical objects
      in various environments, their interactions with other particles or surfaces, and for
      simulations where the internal structure of the sphere needs to be represented explicitly.",
     "parameters":{
        "sphereType":{"description":"Type of sphere geometry to use ('icosidodecahedron' or 'icosphere').",
                      "type":"str",
                      "default":"icosidodecahedron"},
        "particleName":{"description":"Name or type of the particles making up the sphere.",
                        "type":"str"},
        "particleMass":{"description":"Mass of each particle.",
                        "type":"float",
                        "default":1.0},
        "particleRadius":{"description":"Radius of each particle.",
                          "type":"float"},
        "particleCharge":{"description":"Charge of each particle.",
                          "type":"float",
                          "default":0.0},
        "numberOfSpheres":{"description":"Number of spheres to create.",
                           "type":"int",
                           "default":1},
        "particlesPerSphere":{"description":"Number of particles per sphere.",
                              "type":"int",
                              "default":31},
        "radiusOfSphere":{"description":"Radius of the overall spherical structure.",
                          "type":"float",
                          "default":1.0},
        "K":{"description":"Spring constant for bonds between particles.",
             "type":"float"},
        "steric":{"description":"Whether to include steric interactions between particles.",
                  "type":"bool",
                  "default":false},
        "heightMean":{"description":"Mean height for sphere placement.",
                      "type":"float",
                      "default":0.0},
        "heightStd":{"description":"Standard deviation of height for sphere placement.",
                     "type":"float",
                     "default":0.0},
        "heightReference":{"description":"Reference height for sphere placement.",
                           "type":"float",
                           "default":0.0},
        "Ktethers":{"description":"Spring constant for tether bonds.",
                    "type":"float",
                    "default":0.0},
        "heightTethersThreshold":{"description":"Height threshold for adding tethers.",
                                  "type":"float"},
        "tethersPerBlob":{"description":"Number of tethers per blob particle.",
                          "type":"int"},
        "thetaTethers":{"description":"Angle for tether placement.",
                        "type":"float"},
        "maxTries":{"description":"Maximum number of attempts to place spheres.",
                    "type":"int",
                    "default":100}
     },
     "example":"
         {
            \"type\":\"SPHEREMULTIBLOB\",
            \"parameters\":{
                \"sphereType\":\"icosphere\",
                \"particleName\":\"blob\",
                \"particleRadius\":0.1,
                \"numberOfSpheres\":5,
                \"particlesPerSphere\":42,
                \"radiusOfSphere\":2.0,
                \"K\":100.0,
                \"steric\":true
            }
         }
        "
    }
    """

    availableParameters = {"sphereType",
                           "particleName",
                           "particleMass","particleRadius","particleCharge",
                           "numberOfSpheres",
                           "particlesPerSphere",
                           "radiusOfSphere",
                           "K",
                           "heightMean","heightStd",
                           "heightReference",
                           "Ktethers",
                           "heightTethersThreshold",
                           "tethersPerBlob",
                           "thetaTethers",
                           "maxTries"}
    requiredParameters  = {"K"}
    definedSelections   = set()

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

    def __applyPBC(self, positions, box_size):
        """
        Create periodic images of the system.

        Parameters:
        positions (np.ndarray): Array of positions of shape (N, D) where N is the number of points and D is the dimensionality.
        box_size (float): The size of the periodic box.

        Returns:
        np.ndarray: Array of replicated positions considering periodic boundary conditions.
        """
        shifts = np.array([-1, 0, 1])
        offsets = np.array(np.meshgrid(shifts, shifts, shifts)).T.reshape(-1, 3)

        replicated_positions = []
        for offset in offsets:
            replicated_positions.append(positions + offset * box_size)

        return np.vstack(replicated_positions)

    def __computeNewPosition(self, sphPositions,X,Y,Z, radius,
                             heightMean, heightStd, heightReference,
                             ntries):

        newPosition = []
        count = 0
        while count<ntries:
            if heightStd > 0.0:
                height = np.random.normal(heightMean,heightStd)
            else:
                height = heightMean
            height += heightReference
            if height > Z - radius or height < -Z + radius:
                continue

            x = np.random.uniform(-X,X)
            y = np.random.uniform(-Y,Y)
            center = [x,y,height]

            if len(sphPositions)>0:
                sphPositionsPBC = self.__applyPBC(sphPositions, 2*X)
                tree = cKDTree(sphPositionsPBC)
                minDst, minDstIndex = tree.query(center, k=1)
            else:
                minDst = np.inf

            if minDst > 2.0*radius*1.05:
                newPosition = center
                break
            count+=1

        return newPosition


    def __init__(self,name,**params):
        super().__init__(_type = self.__class__.__name__,
                         _name= name,
                         availableParameters = self.availableParameters,
                         requiredParameters  = self.requiredParameters,
                         definedSelections   = self.definedSelections,
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

        Ktethers = params.get("Ktethers", 0.0)
        if Ktethers>0.0:
            heightTethersThreshold = params["heightTethersThreshold"]
            tethersPerBlob         = params["tethersPerBlob"]
            thetaTethers           = params["thetaTethers"]

        box = self.getEnsemble().getEnsembleComponent("box")

        self.maxTries    = params.get("maxTries",100)

        X = box[0]/2.0
        Y = box[1]/2.0

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
        i            = 0
        tries        = 0
        while i < numberOfSpheres:
            newPosition = self.__computeNewPosition(sphPositions,X,Y,Z, radiusOfSphere,
                                                    heightMean, heightStd, heightReference,
                                                    self.maxTries*100*(i+1))

            if len(newPosition)>0:
                sphPositions.append(newPosition)
                i+=1
            else:
                sphPositions = []
                i            = 0
                tries       += 1

        if tries >= self.maxTries:
            print("Unable to find a correct configuration adshfdsoafjidosajfidoajfidosj")
            raise ValueError("The number of spheres is too high for the box size")

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
        forceField["BondPair"] = {}
        forceField["BondPair"]["parameters"] = {}
        forceField["BondPair"]["type"] = ["Bond2", "Harmonic"]
        forceField["BondPair"]["labels"] = ["id_i", "id_j", "K", "r0"]
        forceField["BondPair"]["data"] = []

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
            forceField["BondPair"]["data"].append([i,j,k,r0])

        forceField["BondTether"] = {}
        forceField["BondTether"]["parameters"] = {}
        forceField["BondTether"]["type"]   = ["Bond1", "FixedHarmonic"]
        forceField["BondTether"]["labels"] = ["id_i", "K", "r0", "position"]
        forceField["BondTether"]["data"]   = []
        ############################################################
        print(Ktethers)
        if Ktethers > 0:
            bondsTethers = []
            for i in range(numberOfSpheres):
                for n in range(self.sphN):
                    pn = sph2pos[i][n]
                    height = pn[2]-heightReference
                    if height > heightTethersThreshold:
                        tetherLength = height/np.sin(thetaTethers)
                        for j in range(tethersPerBlob):
                            phi     = 2*np.pi*j/tethersPerBlob
                            xtether = pn[0] + tetherLength * np.cos(phi) * np.sin(thetaTethers)
                            ytether = pn[1] + tetherLength * np.sin(phi) * np.sin(thetaTethers)
                            posTether = [xtether, ytether, -Z]
                            bondsTethers.append([sph2ids[i][n], Ktethers, tetherLength, posTether])

            for i,k,r0,p in bondsTethers:
                forceField["BondTether"]["data"].append([i,k,r0, p])

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,selectionType,selectionOptions):
        return None

