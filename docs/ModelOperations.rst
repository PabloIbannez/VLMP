ModelOperations
===============

.. include:: ModelOperationsIntro.rst

alignInertiaMomentAlongVector
-----------------------------


    Component name: alignInertiaMomentAlongVector
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Aling the largest inertia moment of the selected elements along a given vector.

    :param vector: Vector along which the inertia moment will be aligned.
    :type vector: list of floats

    

distributeRandomly
------------------


    Component name: distributeRandomly
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 26/08/2023

    Distribution of the selected particles in different bounds

    :param mode: Mode of distribution, the bound where the particles will be distributed, can be "box" or "sphere"
    :type mode: dict, optional, default='box'
    :param avoidClashes: If is larger than 0, the particles will be distributed avoiding clashes with other particles.
                         The value of this parameter is the number of tries to avoid the clash.
                         If the number of tries is reached, an error will be raised.
    :type avoidClashes: int, optional, default=0
    :param randomRotation: If True, the particles will be randomly rotated before being distributed
    :type randomRotation: bool, optional, default=True

    

rotation
--------


    Component name: rotation
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 01/09/2023

    

setCenterOfMassPosition
-----------------------


    Component name: setCenterOfMassPosition
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Set the center of mass of a selection of particles to a given position.

    :param position: Position to set the center of mass to.
    :type position: list of floats

    

setContactDistance
------------------


    Component name: setDistance
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 28/08/2023

    Set the contact distance between two selections of particles.

    :param distance: distance to set
    :type distance: float
    

setParticleLowestPosition
-------------------------


    Component name: setParticleLowestPosition
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Set the lowest particle position to value.

    :param position: Position to set the lowest particle to.
    :type position: z coordinate, float
    :param considerRadius: Consider particle radius when setting the lowest position.
    :type considerRadius: bool, optional

    

setParticlePositions
--------------------


    Component name: setParticlePositions
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 31/10/2023

    Set the position of a set of particles to a given a list of ids and a position.

    :param positions: Position to set the particles to.
    :type position: list of floats

    

setParticleXYPosition
---------------------


    Component name: setParticleXYPosition
    Component type: modelOperation

    Author: Pablo Ibáñez-Freire
    Date: 26/02/2024

    Set the XY particle position to value.

    :param position: Position to set the XY particle to.
    :type position: float list
    :param considerRadius: Consider particle radius when setting the XY position.
    :type considerRadius: bool, optional

    

