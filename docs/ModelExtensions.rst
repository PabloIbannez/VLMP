ModelExtensions
===============

.. include:: ModelExtensionsIntro.rst

ACMagneticField
---------------


    Component name: ACMagneticField
    Component type: modelExtension

    Author: P. Palacios-Alonso
    Date: 16/10/2023

    Alternating current (AC) magnetic field applied to a selection of magnetic particles

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param force: Force applied to the particles
    :type force: list of floats

    ...
    

AFM
---


    Component name: AFM
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    AFM model extension.

    :param epsilon: epsilon parameter for tip-particle interaction
    :type epsilon: float
    :param sigma: sigma parameter for tip-particle interaction
    :type sigma: float
    :param K: spring constant
    :type K: float
    :param Kxy: xy spring constant
    :type Kxy: float
    :param tipVelocity: tip velocity
    :type tipVelocity: float
    :param startChipPosition: initial position of the chip
    :type startChipPosition: list of float [x,y,z]
    

LennardJones
------------


    Component name: LennardJones
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 21/09/2023

    Lennard Jones potential between particles.

    :param condition: Condition for the interaction. Options: "inter", "intra" ...
    :type condition: str, default="inter"
    :param interactionMatrix: Matrix of interaction parameters between different types of particles.
    :type interactionMatrix: list of lists. Each list is a row of the matrix. Format type1,type2,epsilon,sigma
    :param cutOffFactor: Factor to multiply the sigma parameter to obtain the cut-off distance.
    :type cutOffFactor: float
    :param addVerletList: If True, a Verlet list will be created for the interactions.
    :type addVerletList: bool, optional, default=True

    ...
    

WCA
---


    Component name: WCA
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 02/01/2024

    WCA potential between particles.

    :param condition: Condition for the interaction. Options: "inter", "intra" ...
    :type condition: str, default="inter"
    :param epsilon: epsilon parameter of the WCA potential
    :type epsilon: float
    :param cutOffFactor: Factor to multiply the sigma parameter to obtain the cut-off distance.
    :type cutOffFactor: float
    :param addVerletList: If True, a Verlet list will be created for the interactions.
    :type addVerletList: bool, optional, default=True

    ...
    

absortionSurface
----------------


    Component name: absortionSurface
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 30/08/2023

    ...
    

addBond
-------


    Component name: addBond
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire and Pablo Palacios
    Date: 19/06/2023

    Elastic Network Model (ENM).

    :param K: Spring constant.
    :type K: float
    :param r0: Equilibrium distance.
    :type r0: float

    

constantForce
-------------


    Component name: constantForce
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 14/03/2023

    Constant force applied to a set of particles

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param force: Force applied to the particles
    :type force: list of floats

    ...
    

constantForceBetweenCentersOfMass
---------------------------------


    Component name: constantForceBetweenCentersOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Constant force between centers of mass of selected particles

    :param selection1: Selection for the first particle group
    :type selection1: list of dictionaries
    :param selection2: Selection for the second particle group
    :type selection2: list of dictionaries
    :param force: Force applied to the particles
    :type force: float

    ...
    

constantForceOverCenterOfMass
-----------------------------


    Component name: constantForceOverCenterOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Applies a constant force over the center of mass of a selection of particles.

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param force: Force applied to the particles
    :type force: list of floats

    ...
    

constantTorqueBetweenCentersOfMass
----------------------------------


    Component name: constantTorqueBetweenCentersOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Constant torque between centers of mass of selected particles

    :param selection1: Selection for the first particle group
    :type selection1: list of dictionaries
    :param selection2: Selection for the second particle group
    :type selection2: list of dictionaries
    :param torque: torque applied to the particles
    :type torque: float

    ...
    

constantTorqueOverCenterOfMass
------------------------------


    Component name: constantTorqueOverCenterOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Constant torque over center of mass

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param torque: Torque applied to the center of mass
    :type torque: list of floats

    ...
    

constraintCenterOfMassPosition
------------------------------


    Component name: constraintCenterOfMassPosition
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 14/03/2023

    Apply a constraint to the center of mass of a selection of particles

    :param selection: Selection of particles where the constraint will be applied
    :type selection: list of dictionaries
    :param K: Stiffness of the constraint
    :type K: float
    :param r0: Distance between the center of mass and the constraint position
    :type r0: float
    :param position: Position of the center of mass of the selection
    :type position: list of floats

    ...
    

constraintParticlesListPositionLambda
-------------------------------------


    Component name: constraintParticlesListPositionLambda
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 5/12/2023

    Apply a lambda constraint to the position of a set of particles.
    Particles are given by two lists, one with the ids and the other one with the positions

    :param K: Stiffness of the constraint
    :type K: float
    :param n: Exponent of the constraint
    :type n: int
    :param ids: List of particle ids
    :type ids: list of int
    :param positions: List of particle positions
    :type positions: list of list of float

    ...
    

constraintParticlesPosition
---------------------------


    Component name: constraintParticlesPosition
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 30/10/2023

    Apply a constraint to the position of a set of particles.

    :param selection: Selection of particles where the constraint will be applied
    :type selection: list of dictionaries
    :param K: Stiffness of the constraint
    :type K: float

    ...
    

constraintParticlesPositionLambda
---------------------------------


    Component name: constraintParticlesPositionLambda
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 5/12/2023

    Apply a lambda constraint to the position of a set of particles.

    :param selection: Selection of particles where the constraint will be applied
    :type selection: list of dictionaries
    :param K: Stiffness of the constraint
    :type K: float
    :param n: Exponent of the constraint
    :type n: float

    ...
    

harmonicBondBetweenCentersOfMass
--------------------------------


    Component name: harmonicBondBetweenCentersOfMass
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 04/04/2023

    Harmonic bond between centers of mass

    :param selection1: Selection for the first particle group
    :type selection1: list of dictionaries
    :param selection2: Selection for the second particle group
    :type selection2: list of dictionaries
    :param K: Spring constant
    :type K: float
    :param r0: Equilibrium distance
    :type r0: float

    ...
    

helixBoundaries
---------------


    Component name: helixBoundaries
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 03/06/2024

    :param helixPitch: pitch of the helix
    :type helixPitch: float
    :param helixRadius: radius of the helix
    :type helixRadius: float
    :param eps: helix sign, 1 for right-handed, -1 for left-handed
    :type eps: float
    :param nTurns: number of turns of the helix
    :type nTurns: int
    :param nPointsHelix: number of points to discretize the helix
    :type nPointsHelix: int
    :param helixInnerRadius: inner radius of the helix
    :type helixInnerRadius: float
    :param nx: number of points in the x direction
    :type nx: int
    :param ny: number of points in the y direction
    :type ny: int
    :param nz: number of points in the z direction
    :type nz: int
    :param K: spring constant for boundary conditions
    :type K: float

    

plates
------


    Component name: plates
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Common epsilon, sigma plates for particles in the system.

    :param platesSeparation: Distance between plates.
    :param epsilon: Energy parameter for the plates.
    :param sigma: Length parameter for the plates.
    :param compressionVelocity: Velocity at which the plates are compressed.
    :param minPlatesSeparation: Minimum distance between plates.
    :param maxPlatesSeparation: Maximum distance between plates.

    

sphericalShell
--------------


    Component name: sphericalShell
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 15/06/2023

    Spherical shell model extension for the model.

    :param shellCenter: Center of the spherical shell.
    :type shellCenter: list of floats
    :param shellRadius: Radius of the spherical shell.
    :type shellRadius: float
    :param shellEpsilon: Epsilon of the spherical shell.
    :type shellEpsilon: float, optional (default = 1.0)
    :param shellSigma: Sigma of the spherical shell.
    :type shellSigma: float, optional (default = 1.0)
    :param minShellRadius: Minimum radius of the spherical shell.
    :type minShellRadius: float, optional (default = 0.0)
    :param maxShellRadius: Maximum radius of the spherical shell.
    :type maxShellRadius: float, optional (default = inf)
    :param radiusVelocity: Velocity of the radius of the spherical shell.
    :type radiusVelocity: float, optional (default = 0.0)

    ...
    

intraSteric
-----------


    Component name: intraSteric
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 21/09/2023

    Steric interactions between particles. If molecues are bonded, the interaction is not considered.

    :param condition: Condition for the interaction. Options: "inter", "intra" ...
    :type condition: str, default="inter"
    :param epsilon: epsilon parameter for the interaction
    :type epsilon: float
    :param cutOffFactor: Factor to multiply the sigma parameter to obtain the cut-off distance.
    :type cutOffFactor: float
    :param addVerletList: If True, a Verlet list will be created for the interactions.
    :type addVerletList: bool, optional, default=True

    ...
    

surface
-------


    Component name: surface
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Common epsilon, sigma surface for particles in the system.

    :param epsilon: epsilon of the surface
    :type epsilon: float
    :param surfacePosition: position of the surface
    :type surfacePosition: float
    :param ignoredTypes: types to ignore
    :type ignoredTypes: list

    

surfaceMaxForce
---------------


    Component name: surfaceMaxForce
    Component type: modelExtension

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    Common epsilon, sigma surface for particles in the system.

    

uniformMagneticField
--------------------


    Component name: uniformMagneticField
    Component type: modelExtension

    Author: P. Palacios-Alonso
    Date: 16/10/2023

    Alternating current (Uniform) magnetic field applied to a selection of magnetic particles

    :param selection: Selection of particles where the force is applied
    :type selection: list of dictionaries
    :param force: Force applied to the particles
    :type force: list of floats

    ...
    

