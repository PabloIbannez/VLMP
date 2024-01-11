import numpy as np

from scipy.optimize import fsolve
from scipy.spatial.transform import Rotation

def helixEquation(s,a,b,e):

    H = np.sqrt(a**2 + b**2)

    x = a*np.cos(s/H)
    y = a*np.sin(s/H)*e
    z = b*s/H

    return np.asarray([x,y,z])

def helixPointsDistanceMinimization(s1,s2,a,b,e,sigma):

    p1 = helixEquation(s1,a,b,e)
    p2 = helixEquation(s2,a,b,e)

    dx = p1[0]-p2[0]
    dy = p1[1]-p2[1]
    dz = p1[2]-p2[2]

    d = np.sqrt(dx*dx+dy*dy+dz*dz)-sigma

    return d

def computeHelixParticlesDistance(a,b,e,sigma):

    try:
        sOne = fsolve(helixPointsDistanceMinimization,sigma,args=(0.0,a,b,e,sigma),xtol=1e-5)[0] # x0 = sigma
        #Check if sOne is correct
        diff = np.abs(helixPointsDistanceMinimization(sOne,0.0,a,b,e,sigma))
        if diff >1e-5:
            print(f"Error computing sOne, diff: {diff}")
            raise Exception("sOne is not correct")
    except:
        print(f"Error computing sOne")
        raise Exception("Error computing sOne")

    return sOne


def discreteHelixFrame(i,sOne,a,b,e):

    pos     = helixEquation( i*sOne,a,b,e)
    posNext = helixEquation((i+1)*sOne,a,b,e)

    dr = posNext-pos
    ex = dr/np.linalg.norm(dr)

    ey = np.cross(np.asarray([0.0,0.0,1.0]),ex)
    ey = ey/np.linalg.norm(ey)

    ez = np.cross(ex,ey)
    ez = ez/np.linalg.norm(ez)

    return np.asarray([ex,ey,ez]).T

def computeHelixMatrix(a,pitch,e,sigma):

    b     = pitch/ (2.0 * np.pi)

    sOne = computeHelixParticlesDistance(a,b,e,sigma)

    R_0 = discreteHelixFrame(0,sOne,a,b,e)
    R_1 = discreteHelixFrame(1,sOne,a,b,e)

    return R_0.T@R_1 # R_1 in the basis of R_0

def computeConnections(a,pitch,helicity,sigma):

    R_H = computeHelixMatrix(a,pitch,helicity,sigma)

    b     = pitch/ (2.0 * np.pi)

    sOne = computeHelixParticlesDistance(a,b,helicity,sigma)

    R_0 = discreteHelixFrame(0,sOne,a,b,helicity)
    R_1 = discreteHelixFrame(1,sOne,a,b,helicity)

    pos0 = helixEquation(0.0,a,b,helicity)
    pos1 = helixEquation(sOne,a,b,helicity)

    pos0 = R_0.T@pos0
    pos1 = R_0.T@pos1

    dr   = (pos1-pos0)
    dr   = dr/np.linalg.norm(dr)
    dr   = dr*sigma/2.0

    connectionNext = dr

    pos0 = helixEquation(0.0,a,b,helicity)
    pos1 = helixEquation(sOne,a,b,helicity)

    pos0 = R_1.T@pos0
    pos1 = R_1.T@pos1

    dr   = (pos0-pos1)
    dr   = dr/np.linalg.norm(dr)
    dr   = dr*sigma/2.0

    connectionPrevious = dr

    return connectionNext,connectionPrevious

def computeLinker(a,pitch,helicity,sigma,angle):

    ez = np.asarray([0.0,0.0,1.0])

    b     = pitch/ (2.0 * np.pi)

    sOne = computeHelixParticlesDistance(a,b,helicity,sigma)

    R    = discreteHelixFrame(0,sOne,a,b,helicity)

    pos0         = helixEquation(0.0,a,b,helicity)
    helixAxisPos = np.asarray([0.0,0.0,0.0])

    dr   = (pos0-helixAxisPos)
    dr   = dr/np.linalg.norm(dr)

    linkerMax = R.T@dr
    linkerMax = linkerMax/np.linalg.norm(linkerMax)
    linkerMax = linkerMax*sigma/2.0

    axis = np.cross(linkerMax,ez)
    axis = axis/np.linalg.norm(axis)

    ## Rotate the dr vector around the axis by angle
    Raxis = Rotation.from_rotvec(axis*angle).as_matrix()

    linker = Raxis@linkerMax
    linker = linker/np.linalg.norm(linker)
    linker = linker*sigma/2.0

    return linker

def generateHelix(N,a,pitch,helicity,sigma,initPos = np.array([0.0,0.0,0.0]),initOri = np.eye(3)):
    """
    Generates a helix with N beads, pitch and helicity
    """

    R_H = computeHelixMatrix(a,pitch,helicity,sigma)

    pos = np.zeros((N,3))
    ori = np.zeros((N,3,3))

    pos[0]     = initPos
    ori[0,:,:] = initOri

    for i in range(1,N):
        pos[i]  = ori[i-1]@np.asarray([sigma,0.0,0.0])+pos[i-1]
        ori[i]  = ori[i-1]@R_H

    return pos,ori
