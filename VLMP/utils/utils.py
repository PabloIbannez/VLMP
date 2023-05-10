import logging
import copy

import numpy as np

from scipy.spatial.transform import Rotation as R
from pyquaternion import Quaternion

#Units utils

def picosecond2KcalMol_A_time():
    return 20/0.978

#Geometry utils

def getEx(q):
    """ Given a quaternion, q, the function returns the z vector of the local basis"""

    q0,q1,q2,q3 = q

    return 2.0*np.asarray([q0*q0+q1*q1-0.5,q1*q2+q0*q3,q1*q3-q0*q2])

def getEy(q):
    """ Given a quaternion, q, the function returns the z vector of the local basis"""

    q0,q1,q2,q3 = q

    return 2.0*np.asarray([q1*q2-q0*q3,q0*q0+q2*q2-0.5,q2*q3+q0*q1])

def getEz(q):
    """ Given a quaternion, q, the function returns the z vector of the local basis"""

    q0,q1,q2,q3 = q

    return 2.0*np.asarray([q1*q3+q0*q2,q2*q3-q0*q1,q0*q0+q3*q3-0.5])


def quaternionFromVectors(vec1, vec2):
    """ Given two vector the function returns the rotation that transform one into another.
        The rotation is codified as a quaternion"""

    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)

    if any(v):
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        M = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    else:
        if np.dot(a,b) < 0:
            M = -np.eye(3)
        else:
            M =  np.eye(3)

    q1,q2,q3,q0 = R.from_matrix(M).as_quat()

    return np.asarray([q0,q1,q2,q3])


################################################################

def getLabelIndex(l,labels):
    logger = logging.getLogger("VLMP")

    if l in labels:
        return labels.index(l)
    else:
        logger.error("Label %s not found in labels list" % l)
        raise Exception("Label not found")

def getValuesAndPaths(d, key, path=None):
    """
    Recursively search a nested dictionary for all values associated with a given key,
    along with the path to each value.
    """

    if path is None:
        path = ()

    values = []
    for k, v in d.items():
        new_path = path + (k,)
        if k == key:
            values.append((v, new_path))
        elif isinstance(v, dict):
            values.extend(getValuesAndPaths(v, key, new_path))

    return values

def getSelections(models,selectionsList,**param):

    logger = logging.getLogger("VLMP")

    #Check params
    for p in param.keys():
        if p not in selectionsList:
            continue
        else:
            for k in param[p].keys():
                if k not in ["models","expression"]:
                    logger.error(f"[getSelections] Parameter {k} not recognized for selection {p}, available parameters are: models, expression")
                    raise Exception("Unknown parameter")

    selections = {}

    for sel in [s for s in param.keys() if s in selectionsList]:
        selections[sel] = []

        if "models" in param[sel]:
            selectedModels = [ m for m in models if m.getName() in param[sel]["models"]]
        else:
            selectedModels = models

        for mdl in selectedModels:
            if "expression" in param[sel]:
                mdlSelIds = mdl.getSelection(**param[sel]["expression"])
            else:
                mdlSelIds = mdl.getSelection()

            offSet = mdl.getIdOffset()
            mdlSelIds = [i+offSet for i in mdlSelIds]

            selections[sel] += mdlSelIds
        selections[sel] = list(set(selections[sel]))

    return copy.deepcopy(selections)
