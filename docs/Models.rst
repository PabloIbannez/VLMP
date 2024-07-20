Models
======

.. include:: ModelsIntro.rst

CORONAVIRUS
-----------

	:author: Pablo Ibáñez-Freire

	.. figure:: _images/virus_bottom.png
		:align: center
		:width: 80%

 CORONAVIRUS model for simulating virus-like particles. This model combines two coarse-grained approaches to represent the complex structure of coronaviruses: 

 1. Shape-Based Coarse-Grained (SBCG) model for proteins: Used to represent the viral proteins, particularly the spike proteins. This approach maintains the overall shape and essential features of proteins while reducing computational complexity [Arkhipov2006]_. 

 2. One-particle-thick, solvent-free, coarse-grained model for lipid membranes: Employed to simulate the viral envelope. This model represents lipids as single particles, allowing for efficient simulation of membrane dynamics without explicit solvent [Yuan2010]_. 

 The combination of these models enables the simulation of large-scale viral structures and their interactions with the environment, balancing computational efficiency with biological accuracy. 

 The model allows customization of various parameters including the number of lipids, vesicle radius, and number of spike proteins. It also incorporates different interaction potentials for lipid-lipid, protein-protein, and lipid-protein interactions, as well as the option to include a simulated surface for studying virus-surface interactions. 

 This model is particularly useful for studying the structural dynamics of coronaviruses and interactions with cellular membranes or other surfaces.

.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - inputModelData
	  - Path to the JSON file containing model parameters.
	  - str
	  - ./data/CORONAVIRUS.json
	* - nLipids
	  - Number of lipid particles in the vesicle.
	  - int
	  - 1501
	* - muLipids
	  - Shape parameter for lipid-lipid interactions.
	  - float
	  - 3.0
	* - nSpikes
	  - Number of spike proteins to add to the vesicle surface.
	  - int
	  - 0
	* - chiLipids
	  - Another shape parameter for lipid-lipid interactions.
	  - float
	  - 7.0
	* - thetaLipids
	  - Angle parameter for lipid-lipid interactions.
	  - float
	  - 0.0
	* - surfacePosition
	  - Z-coordinate of the simulated surface.
	  - float
	  - 0.0
	* - center
	  - Center coordinates of the vesicle.
	  - list of float
	  - [0.0, 0.0, 0.0]
	* - lipidRadius
	  - Radius of each lipid particle.
	  - float
	  - 18.0
	* - vesicleRadius
	  - Radius of the vesicle.
	  - float
	  - 400.0
	* - surface
	  - Whether to include a simulated surface.
	  - bool
	  - False

Example:

.. code-block:: python

	{
		"type": "CORONAVIRUS",
		"parameters": {'nLipids': 2000, 'vesicleRadius': 500.0, 'nSpikes': 50, 'epsilonLipids': 5.5, 'surface': True, 'surfacePosition': -400.0}
	}

References:

	.. [Yuan2010] Yuan, H., Huang, C., Li, J., Lykotrafitis, G., & Zhang, S. (2010). One-particle-thick, solvent-free, coarse-grained model for biological and biomimetic fluid membranes. Physical Review E, 82(1), 011905.

	.. [Arkhipov2006] Arkhipov, A., Freddolino, P. L., & Schulten, K. (2006). Stability and dynamics of virus capsids described by coarse-grained modeling. Structure, 14(12), 1767-1777.



ENM
---

	:author: Pablo Ibáñez-Freire

 Elastic Network Model (ENM) for protein simulations. This model implements a coarse-grained representation of proteins, typically using one bead per residue (usually the alpha-carbon). ENM is based on the assumption that protein dynamics can be described by harmonic potentials between nearby residues. 

 The model constructs a network of springs between residues within a certain cutoff distance. This approach allows for efficient simulation of large-scale protein motions and normal modes, making it particularly useful for studying protein flexibility and conformational changes. 

 The model can be customized through various parameters, including the spring constant (K) and the cutoff distance for interactions (enmCut). These parameters control the strength of the harmonic interactions and the connectivity of the network, respectively. 

 The protein structure is input via a PDB file, which can be either a local file or downloaded from the RCSB PDB database if a valid PDB ID is provided. 

 This implementation also includes options for centering the input structure and handling multiple chains, making it versatile for various protein simulation scenarios. 

 This model uses the [pyGrained]_ library to create the ENM representation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - PDB
	  - Path to a local PDB file or a valid PDB ID for download.
	  - str
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - aggregateChains
	  - If True, treats multiple chains as a single entity.
	  - bool
	  - True
	* - K
	  - Spring constant for the harmonic interactions.
	  - float
	  - 
	* - enmCut
	  - Cutoff distance for including spring connections between residues.
	  - float
	  - 
	* - SASA
	  - If True, calculates the Solvent Accessible Surface Area.
	  - bool
	  - False
	* - centerInput
	  - If True, centers the input structure.
	  - bool
	  - True

Example:

.. code-block:: python

	{
		"type": "ENM",
		"parameters": {'PDB': '1ABC', 'centerInput': True, 'K': 1.0, 'enmCut': 10.0}
	}

References:

	.. [Tirion1996] Tirion, M. M. (1996). Large Amplitude Elastic Motions in Proteins from a Single-Parameter, Atomic Analysis. Physical Review Letters, 77(9), 1905–1908.

	.. [Atilgan2001] Atilgan, A. R., Durell, S. R., Jernigan, R. L., Demirel, M. C., Keskin, O., & Bahar, I. (2001). Anisotropy of Fluctuation Dynamics of Proteins with an Elastic Network Model. Biophysical Journal, 80(1), 505–515.

	.. [pyGrained] https://github.com/PabloIbannez/pyGrained



FILE
----

	:author: Pablo Ibáñez-Freire

 FILE model for loading pre-existing simulation configurations. This model allows users to import a complete simulation setup from a JSON file, including particle positions, types, and force field parameters. It's particularly useful for continuing simulations from a previous state or for setting up complex initial configurations. 

 The model reads all necessary information from the input file, including: - Particle types and their properties 

 - Particle positions and other state variables 

 - Structure information (particle IDs, types, etc.) 

 - Force field parameters and interactions 

 This approach provides flexibility in setting up simulations, as users can manually create or modify the input files to achieve specific initial conditions or system configurations. It also allows for easy sharing and reproduction of simulation setups. 

 The FILE model includes an option to selectively remove certain types of interactions from the imported force field.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - inputFilePath
	  - Path to the JSON file containing the complete simulation setup.
	  - str
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - removeInteractionsByType
	  - List of interaction types to remove from the imported force field.
	  - list of str
	  - 

Example:

.. code-block:: python

	{
		"type": "FILE",
		"parameters": {'inputFilePath': 'path/to/simulation.json', 'removeInteractionsByType': ['Bond2', 'NonBonded']}
	}



HELIX
-----


    Component name: HELIX
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 25/04/2023

    Polimerization model for a helix.

    

ICOSPHERE
---------


    Component name: ICOSPHERE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 18/06/2023

    Icosphere model
    

IDP
---


    Component name: IDP
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 25/03/2023

    Intrinsic disorder protein model.

    Reference: https://journals.aps.org/pre/pdf/10.1103/PhysRevE.90.042709

    

KB
--


    Component name: KB
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 25/03/2023

    Karanicolas Brooks.

    

MADna
-----

	:author: Pablo Ibáñez-Freire

 MADna model for DNA simulation. This model implements a coarse-grained representation of DNA based on the MADna force field, which provides accurate sequence-dependent conformational and elastic properties of double-stranded DNA. The model offers a balance between computational efficiency and accuracy in representing DNA structure and dynamics. 

 The model allows for customization of electrostatic interactions through the Debye length and dielectric constant parameters. The debyeFactor can be used to adjust the cutoff distance for these interactions. 

 A 'fast' variant of the model is available, which can be used to speed up simulations at the cost of some accuracy. This variant modifies how non-bonded interactions are computed. Non bonded interactions (WCA and Debye-Hückel) are using bonds. This means that the neighbor list is not used and the interactions pairs are precomputed. Thus, this approach is valid when beads far away in the sequence are kept separated during the simulation. For example, when pulling a DNA strand. 

 The model reads its core parameters from a JSON file, which can be specified using the inputModelData parameter. This allows for easy modification and extension of the model's base parameters. 

 For more details on the underlying force field, see [Assenza2022]_.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - sequence
	  - DNA sequence to be modeled. Must be a string of valid DNA bases (A, T, C, G).
	  - str
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - dielectricConstant
	  - Dielectric constant of the medium. Affects the strength of electrostatic interactions.
	  - float
	  - 78.3
	* - inputModelData
	  - Path to the JSON file containing model parameters. Allows for customization of base model parameters.
	  - str
	  - ./data/MADna.json
	* - variant
	  - Variant of the model to use. 'fast' option available for improved computational speed.
	  - str
	  - 
	* - debyeLength
	  - Debye length for electrostatic interactions. Controls the range of electrostatic forces.
	  - float
	  - 10.8
	* - debyeFactor
	  - Factor to scale the Debye length. Used to set the cutoff distance for electrostatic interactions.
	  - float
	  - 4.0

Example:

.. code-block:: python

	{
		"type": "MADna",
		"parameters": {'sequence': 'ATCGGATCCGAT', 'debyeLength': 10.8, 'dielectricConstant': 78.3, 'debyeFactor': 4.0, 'variant': 'fast'}
	}

References:

	.. [Assenza2022] Assenza, S., & Pérez, R. (2022). Accurate Sequence-Dependent Coarse-Grained Model for Conformational and Elastic Properties of Double-Stranded DNA. Journal of Chemical Theory and Computation, 18(5), 3239-3256.



MAGNETICNP
----------


    Component name: MAGNETICNP
    Component type: model

    Author: P. Palacios-Alonso
    Date: 16/10/2023

    Model of magnetic nanoparticles
    

MEMBRANE
--------


    Component name: MEMBRANE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 22/05/2024

    Alpha carbon resolution membrane model.

    

PARTICLE
--------


    Component name: PARTILCE
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 18/06/2023

    Single particle model.

    

PROTEIN_IDP_PROTEIN
-------------------


    Component name: PROTEIN_IDP_PROTEIN
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 02/01/2024

    Intrinsic disorder protein model merged with protein model (ENM)

    Reference: https://journals.aps.org/pre/pdf/10.1103/PhysRevE.90.042709

    

SBCG
----


    Component name: SBCG
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 23/03/2023

    Shape Based Coarse Grained.

    

SIMULATION
----------


    Component name: SIMULATION
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 6/11/2023

    Load model from dictionary generated by pyUAMMD simulation

    :param inputSimulation: Input dictionary generated by pyUAMMD simulation
    :type inputSimulation: dict
    

SOP
---


    Component name: SOP
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 24/03/2023

    Self organized polymer.

    

SPHEREMULTIBLOB
---------------


    Component name: SPHEREMULTIBLOB
    Component type: model

    Author: Pablo Ibáñez-Freire and Pablo Palacios-Alonso
    Date: 18/07/2023

    Extension of Icosidodecahedron + icosphere
    

STERIC_LAMBDA_SOLVATION
-----------------------


    Component name: STERIC_LAMBDA_SOLVATION
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 02/01/2024

    steric lambda solvation model.

    :param concentration: Concentration of the solute in the solvent (in N/V units)
    :type concentration: float
    :param condition: Condition for the interaction. Options: "inter", "intra" ...
    :type condition: str, default="inter"
    :param epsilon: epsilon parameter of the steric potential
    :type epsilon: float
    :param cutOffFactor: Factor to multiply the sigma parameter to obtain the cut-off distance.
    :type cutOffFactor: float
    :alpha: alpha parameter of the steric potential
    :type alpha: float, default=0.5
    :param addVerletList: If True, a Verlet list will be created for the interactions.
    :type addVerletList: bool, optional, default=True
    :param particleName: Name of the particle to be added to the system.
    :type particleName: str, optional, default="W"
    :param particleMass: Mass of the particle to be added to the system.
    :type particleMass: float, optional, default=1.0
    :param particleRadius: Radius of the particle to be added to the system.
    :type particleRadius: float, optional, default=1.0
    :param particleCharge: Charge of the particle to be added to the system.
    :type particleCharge: float, optional, default=0.0
    :param padding: Padding to be added to the box to place the particle.
    :type padding: two lists of three floats, optional, default=[[0.0,0.0,0.0],[0.0,0.0,0.0]]

    ...
    

WLC
---


    Component name: WLC
    Component type: model

    Author: Pablo Ibáñez-Freire
    Date: 13/03/2023

    Worm-like chain model. See https://en.wikipedia.org/wiki/Worm-like_chain

    :param N: Number of particles
    :type N: int
    :param mass: Mass of the particles
    :type mass: float, optional. Default: 1.0
    :param b: Distance between two consecutive particles
    :type b: float, optional. Default: 1.0
    :param Kb: Spring constant for bonds
    :type Kb: float, optional. Default: 1.0
    :param Ka: Spring constant for angles
    :type Ka: float, optional. Default: 1.0
    

