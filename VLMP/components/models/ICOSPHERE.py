from VLMP.components.models import modelBase

import numpy as np
import icosphere

class ICOSPHERE(modelBase):
    """
    Component name: ICOSPHERE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 18/06/2023

    Icosphere model
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
                                                "Kd"},
                         requiredParameters  = {"particleName"},
                         definedSelections   = {"particleId"},
                         **params)

        ############################################################

        particleName = params["particleName"]

        particleMass   = params.get("particleMass",1.0)
        particleRadius = params.get("particleRadius",1.0)
        particleCharge = params.get("particleCharge",0.0)

        types = self.getTypes()
        types.addType(name = particleName,
                      mass = particleMass,
                      radius = particleRadius,
                      charge = particleCharge)

        position = params.get("position",np.array([0.0,0.0,0.0]))

        resolution = params.get("resolution",1)
        radius     = params.get("radius",1.0)

        Kb = params.get("Kb",1.0)
        Kd = params.get("Kd",0.0)

        ############################################################

        vertices,faces = icosphere.icosphere(nu = resolution)

        #Update the vertices
        for i in range(len(vertices)):
            vertices[i] = radius*vertices[i]+position

        state = {}
        state["labels"] = ["id","position"]

        state["data"] = []
        for i,vertex in enumerate(vertices):
            x,y,z = vertex
            state["data"].append([i,[x,y,z]])

        structure = {}
        structure["labels"] = ["id","type"]

        structure["data"] = []
        for i,face in enumerate(vertices):
            structure["data"].append([i,particleName])

        forceField = {}

        forceField["bonds"] = {}
        forceField["bonds"]["type"]       = ["Bond2","Harmonic"]
        forceField["bonds"]["labels"]     = ["id_i","id_j","r0","K"]
        forceField["bonds"]["parameters"] = {}
        forceField["bonds"]["data"]       = []

        bonds = set()
        for face in faces:
            bonds.add(tuple(sorted([int(face[0]),int(face[1])])))
            bonds.add(tuple(sorted([int(face[1]),int(face[2])])))
            bonds.add(tuple(sorted([int(face[2]),int(face[0])])))

        for bond in bonds:
            dst = np.linalg.norm(vertices[bond[0]]-vertices[bond[1]])
            forceField["bonds"]["data"].append([bond[0],bond[1],dst,Kb])

        # List all pairs of faces that share an edge
        facesPairs = set()
        for i in range(len(faces)):
            for j in range(i+1,len(faces)):
                if len(set(faces[i]).intersection(set(faces[j]))) == 2:
                    facesPairs.add((i,j))

        if Kd > 0.0:
            forceField["dihedrals"] = {}
            forceField["dihedrals"]["type"]       = ["Bond4","Dihedral"]
            forceField["dihedrals"]["labels"]     = ["id_i","id_j","id_k","id_l","phi0","K","n"]
            forceField["dihedrals"]["parameters"] = {}
            forceField["dihedrals"]["data"]       = []

            for facePair in facesPairs:
                face1 = faces[facePair[0]]
                face2 = faces[facePair[1]]

                common = set(face1).intersection(set(face2))

                if len(common) == 2:
                    face1Id = list(set(face1).difference(common))[0]
                    face2Id = list(set(face2).difference(common))[0]

                    i = int(face1Id)
                    j = int(common.pop())
                    k = int(common.pop())
                    l = int(face2Id)

                    forceField["dihedrals"]["data"].append([i,j,k,l,0.0,Kd,1])
                else:
                    self.log("Faces do not share an edge, faces: {} {}".format(face1,face2))
                    raise Exception("Faces do not share an edge")

        ############################################################

        self.setState(state)
        self.setStructure(structure)
        self.setForceField(forceField)


    def processSelection(self,**params):

        sel = []

        if "particleId" in params:
            sel += params["particleId"]

        return sel

