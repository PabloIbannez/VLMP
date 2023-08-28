import pyGrained.models.AlphaCarbon as proteinModel
import pyUAMMD

import copy

#      "data":[
#      ["MET",131.193,3.1,0.0],
#      ["GLU",129.115,2.95,-1.0],
#      "labels":["name","mass","radius","charge"],
#
#
#          "ARG":{
#          "charge":1.0,
#          "mass":156.188,
#          "name":"ARG",
#          "radius":3.3

sopParamsBase = {"SASA":False,
                 "centerInput":True,
                 "aggregateChains":True,
                 "parameters":{}}

names     = ["encapsulin","ccmv"]
pdbs      = ["encapsulin.pdb","ccmv.pdb"]
epsilonNC = [1.5,1.5]

for name,pdb,eps in zip(names,pdbs,epsilonNC):
    sopParams = sopParamsBase.copy()

    sopParams["parameters"]["epsilonNC"] = eps

    sop = proteinModel.SelfOrganizedPolymer(name = name,
                                            inputPDBfilePath = pdb,
                                            params = sopParams)

    types = {"type":["Types","Basic"],
             "labels":["name","mass","radius","charge"],
             "data":[]}

    for t,tinfo in sop.getTypes().items():
        types["data"].append([tinfo["name"],tinfo["mass"],tinfo["radius"],tinfo["charge"]])

    state      = sop.getState()
    structure  = sop.getStructure()
    forceField = sop.getForceField()

    sim = pyUAMMD.simulation()

    sim["global"] = {}
    sim["global"]["types"] = copy.deepcopy(types)

    sim["state"]           = copy.deepcopy(state)

    sim["topology"] = {}
    sim["topology"]["structure"]  = copy.deepcopy(structure)
    sim["topology"]["forceField"] = copy.deepcopy(forceField)

    sim.write(name+".json")



