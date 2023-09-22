import logging

from MDAnalysis.lib.pkdtree import PeriodicKDTree

import numpy as np

def distributeRandomlyGeneratorChecker(box,posSets,radSets,newPosGenerator,distanceChecker,nMaxTries,radiusFactor):

    logger = logging.getLogger("VLMP")

    newPositions = []
    addedRads    = []

    maxRadius = np.max([np.max(r) for r in radSets])

    for i in range(len(posSets)):
        #Trying to find a new position for the particle set i

        if len(newPositions) == 0:
            center = np.mean(posSets[i],axis=0)
            # Generete a random 3D position
            mp = newPosGenerator()

            transVec = mp - center
            newPositions += [list(p + transVec) for p in posSets[i]]
            addedRads+=radSets[i]
            logger.debug(f"Added particle 1/{len(posSets)}")
            continue

        tree = PeriodicKDTree(box=np.asarray(box+[90,90,90],dtype=np.float32))
        tree.set_coords(coords=np.asarray(newPositions,dtype=np.float32),
                        cutoff=maxRadius*2.0)

        # Try to add the set in a random position
        added = False
        tries = 0
        while not added and tries < nMaxTries:
            center = np.mean(posSets[i],axis=0)

            # Generate a random position
            mp = newPosGenerator()

            transVec = mp - center

            tentativePos = np.asarray([p + transVec for p in posSets[i]])

            # Find the closest particles
            pairs = tree.search_tree(np.asarray(tentativePos,dtype=np.float32),maxRadius*2.0)

            toAdd = True
            for i1,i2 in pairs:

                p1 = newPositions[i2]
                p2 = tentativePos[i1]

                r1 = addedRads[i2]
                r2 = radSets[i][i1]

                toAdd = distanceChecker(p1,p2,r1,r2)
                if not toAdd:
                    break
            if toAdd:
                newPositions += [list(p) for p in tentativePos]
                addedRads    += radSets[i]
                added = True
                logger.debug(f"Added particle {i+1}/{len(posSets)} at try {tries}/{nMaxTries}")
            else:
                tries += 1

        if not added:
            logger.error("The number of tries to avoid clashes has been reached.")
            raise Exception("Clash avoidance failed")

    return newPositions.copy()

