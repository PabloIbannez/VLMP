import logging
import copy

import numpy as np

from scipy.spatial.transform import Rotation as R
from pyquaternion import Quaternion

from .bounds import *
from .particlesDistribution import *

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

