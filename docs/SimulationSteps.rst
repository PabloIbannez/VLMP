SimulationSteps
===============

AFMMaxForce
-----------


    Component name: AFMMaxForce
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 31/08/2023

    

afmMeasurement
--------------


    Component name: afmMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    

anglesMeasurement
-----------------


    Component name: anglesMeasurement
    Component type: simulationStep

    

centerOfMassMeasurement
-----------------------


    Component name: centerOfMassMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 09/04/2023

    This component measures the center of mass of the particles in the simulation.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str

    

gyrationRadius
--------------


    Component name: gyrationRadius
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 30/11/2023

    :param outputFilePath: Path to the output file
    :type outputFilePath: str

    

heightMeasurement
-----------------


    Component name: heightMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 09/04/2023

    This component measures the height of the particles selected.
    The height is the average of the N particles with the highest z coordinate.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param particleNumberAverage: Number of particles to average the height
    :type particleNumberAverage: int

    

info
----


    Component name: saveState
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    Simple info step, it shows the current step,
    an estimation of the remaining time and the mean FPS.

    

lambdaActivation
----------------


    Component name: lambdaActivation
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 03/01/2023

    Lambda activation.

    :param activationStep: Activation step.
    :type activationStep: int
    :param measureStep: Measure step.
    :type measureStep: int
    :param pauseStep: Pause step.
    :type pauseStep: int
    :param lambdaValues: Lambda values.
    :type lambdaValues: list

    

lambdaCycle
-----------


    Component name: lambdaCycle
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 03/01/2023

    Lambda cycle.

    :param activationStep: Activation step.
    :type activationStep: int
    :param measureStep: Measure step.
    :type measureStep: int
    :param pauseStep: Pause step.
    :type pauseStep: int
    :param lambdaValues: Lambda values.
    :type lambdaValues: list

    

meanMagnetizationMeasurement
----------------------------


    Component name: meanMagnetizationMeasurement
    Component type: simulationStep

    Author: P. Palacios Alonso
    Date: 18/10/2023

    This component writes the mean magnetization of the system to a file.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str

    

meanRadius
----------


    Component name: meanRadius
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 24/10/2023

    :param outputFilePath: Path to the output file
    :type outputFilePath: str

    

nativeContactsMeasurement
-------------------------


    Component name: nativeContactsMeasurement
    Component type: simulationStep

    

patchPolymersMeasurement
------------------------


    Component name: patchPolymers
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 7/05/2023

    This step is used to measure properties of the
    polymers created by dynamic bonded patchy particles.
    It computes size of the polymers and if they are
    bonded to the surface or not.

    :param startStep: First step to apply the simulationStep
    :type startStep: int, optional
    :param endStep: Last step to apply the simulationStep
    :type endStep: int, optional

    

potentialEnergyMeasurement
--------------------------


    Component name: potentialEnergyMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 18/10/2023

    

potentialMeasurement
--------------------


    Component name: potentialMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 09/04/2023

    

savePatchyParticlesState
------------------------


    Component name: savePatchyParticlesState
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 25/04/2023

    This component is used to save the state of the simulation incliding the
    patchy particles.

    Avalible formats are:
        * .coord
        * .sp
        * .xyz
        * .pdb
        * .itpv
        * .itpd
        * .dcd
        * .lammpstrj
        * .vel

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param outputFormat: Format of the output file
    :type outputFormat: str
    

saveState
---------


    Component name: saveState
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    This component is used to save the state of the simulation.

    Avalible formats are:
        * .coord
        * .sp
        * .xyz
        * .pdb
        * .itpv
        * .itpd
        * .dcd
        * .lammpstrj
        * .vel

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param outputFormat: Format of the output file
    :type outputFormat: str

    

stressMeasurement
-----------------


    Component name: stressMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 29/09/2020

    This component writes the stress tensor of the system to a file.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str
    :param radiusCutOff: Radius cutoff for the calculation of atom volumes
    :type radiusCutOff: float

    

thermodynamicIntegration
------------------------


    Component name: thermodynamicIntegration
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 06/11/2023

    

thermodynamicMeasurement
------------------------


    Component name: thermodynamicMeasurement
    Component type: simulationStep

    Author: Pablo Ibáñez-Freire
    Date: 17/06/2023

    This component performs a thermodynamic measurement of the system.
    It measures the particle number, volume,
    energy (per interaction), kinetic energy, total potential energy, total energy,
    temperature, and virial.

    :param outputFilePath: Path to the output file
    :type outputFilePath: str

    

vqcmMeasurement
---------------


    Component name: vqcmMeasurement
    Component type: simulationStep

    Author: Pablo Palacios-Alonso and Pablo Ibáñez-Freire
    Date: 2/11/2023

    

