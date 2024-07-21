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
	* - surface
	  - Whether to include a simulated surface.
	  - bool
	  - False
	* - nLipids
	  - Number of lipid particles in the vesicle.
	  - int
	  - 1501
	* - lipidRadius
	  - Radius of each lipid particle.
	  - float
	  - 18.0
	* - surfacePosition
	  - Z-coordinate of the simulated surface.
	  - float
	  - 0.0
	* - inputModelData
	  - Path to the JSON file containing model parameters.
	  - str
	  - ./data/CORONAVIRUS.json
	* - center
	  - Center coordinates of the vesicle.
	  - list of float
	  - [0.0, 0.0, 0.0]
	* - chiLipids
	  - Another shape parameter for lipid-lipid interactions.
	  - float
	  - 7.0
	* - thetaLipids
	  - Angle parameter for lipid-lipid interactions.
	  - float
	  - 0.0
	* - vesicleRadius
	  - Radius of the vesicle.
	  - float
	  - 400.0
	* - muLipids
	  - Shape parameter for lipid-lipid interactions.
	  - float
	  - 3.0
	* - nSpikes
	  - Number of spike proteins to add to the vesicle surface.
	  - int
	  - 0

Example:

.. code-block:: python

	{
		"type": "CORONAVIRUS",
		"parameters":{
			"nLipids": 2000,
			"vesicleRadius": 500.0,
			"nSpikes": 50,
			"epsilonLipids": 5.5,
			"surface": True,
			"surfacePosition": -400.0
		}
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
	* - SASA
	  - If True, calculates the Solvent Accessible Surface Area.
	  - bool
	  - False
	* - centerInput
	  - If True, centers the input structure.
	  - bool
	  - True
	* - enmCut
	  - Cutoff distance for including spring connections between residues.
	  - float
	  - 
	* - K
	  - Spring constant for the harmonic interactions.
	  - float
	  - 
	* - aggregateChains
	  - If True, treats multiple chains as a single entity.
	  - bool
	  - True

Example:

.. code-block:: python

	{
		"type": "ENM",
		"parameters":{
			"PDB": "1ABC",
			"centerInput": True,
			"K": 1.0,
			"enmCut": 10.0
		}
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
		"parameters":{
			"inputFilePath": "path/to/simulation.json",
			"removeInteractionsByType": ['Bond2', 'NonBonded']
		}
	}



HELIX
-----

	:author: Pablo Ibáñez-Freire

 HELIX model for simulating helical polymer structures. This model is designed to create and simulate helical polymers, with a particular focus on representing the structures which emerge from the self-assembly of helical monomers. The model uses a patchy-particle approach to represent the monomers, with each monomer having two patches which represent the interaction sites on the monomer surface. An additional patch is used to represent the surface interaction, this additional patch interacts only with the surface and not with other monomers. 

 The helical shape is achived fixing the relative orientation of the monomers, when patches are close enough. 

 The model generates a helical structure based on specified parameters such as the number of monomers, helix radius, pitch, and helicity. It can be used to study various properties and behaviors of helical polymers, including their dynamics, and the effectos of several polymer interactions. 

 Key features of the HELIX model include: 

 - Flexible control over helical geometry (radius, pitch, helicity) 

 - Various initialization options (random, line, or pre-formed helix) 

 - Customizable monomer properties and interactions 

 - Support for different variants of the model, including fixed and dynamic versions 

 - Options for simulating interactions with surfaces or other environmental factors

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - helixRadius
	  - Radius of the helix.
	  - float
	  - 
	* - helixPitch
	  - Pitch of the helix.
	  - float
	  - 
	* - epsilon_mm
	  - Energy parameter for monomer-monomer interactions.
	  - float
	  - 
	* - nMonomers
	  - Number of monomers in the helix.
	  - int
	  - 
	* - variant
	  - Variant of the model to use ('fixedCosine', 'fixedExponential', 'dynamicCosine', 'dynamicExponential', 'twoStatesCosine', 'twoStatesExponential').
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
	* - helicity
	  - Helicity of the structure (1.0 for right-handed, -1.0 for left-handed).
	  - float
	  - 1.0
	* - mode
	  - Simulation mode ('bulk' or 'surface').
	  - str
	  - bulk
	* - monomerRadius
	  - Radius of each monomer.
	  - float
	  - 0.5
	* - init
	  - Initialization method ('random', 'line', or 'helix').
	  - str
	  - random

Example:

.. code-block:: python

	{
		"type": "HELIX",
		"parameters":{
			"mode": "bulk",
			"init": "helix",
			"nMonomers": 100,
			"helixRadius": 10.0,
			"helixPitch": 34.0,
			"epsilon_mm": 1.0,
			"variant": "dynamicCosine"
		}
	}

.. warning::

	This model is under development and may not be fully functional or optimized.



ICOSPHERE
---------

	:author: Pablo Ibáñez-Freire

 ICOSPHERE model for creating spherical structures based on icosahedron subdivision. This model generates a highly uniform spherical distribution of particles, which is particularly useful for simulating spherical objects or creating starting configurations for various spherical systems. 

 The model uses the icosphere algorithm, which starts with a regular icosahedron and repeatedly subdivides its faces to create a more refined spherical approximation. This approach ensures a nearly uniform distribution of vertices on the sphere's surface. 

 Key features of the model include: 

 - Adjustable resolution through subdivision levels 

 - Customizable particle properties (name, mass, radius, charge) 

 - Ability to add bonds between neighboring vertices 

 - Optional steric interactions between particles 



.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - particleName
	  - Name identifier for the particles.
	  - str
	  - A
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - particleRadius
	  - Radius of each particle.
	  - float
	  - 1.0
	* - radius
	  - Radius of the icosphere.
	  - float
	  - 1.0
	* - particleCharge
	  - Charge of each particle.
	  - float
	  - 0.0
	* - Kb
	  - Spring constant for bonds between neighboring vertices.
	  - float
	  - 
	* - position
	  - Center position of the icosphere.
	  - list of float
	  - [0.0, 0.0, 0.0]
	* - steric
	  - Whether to include steric interactions between particles.
	  - bool
	  - False
	* - resolution
	  - Subdivision level for icosphere.
	  - int
	  - 1
	* - particleMass
	  - Mass of each particle.
	  - float
	  - 1.0
	* - Kd
	  - Spring constant for dihedral angles (if applicable).
	  - float
	  - 0.0

Example:

.. code-block:: python

	{
		"type": "ICOSPHERE",
		"parameters":{
			"resolution": 3,
			"radius": 10.0,
			"particleName": "S",
			"particleRadius": 0.5,
			"K": 100.0,
			"steric": True
		}
	}



IDP
---

.. warning::

	This model is currently under development. Please, use it with caution.



KB
--

	:author: Pablo Ibáñez-Freire

 KB (Karanicolas Brooks) model for protein folding simulations. This model implements a structure-based coarse-grained representation of proteins, based on the work of Karanicolas and Brooks. It is particularly effective for studying protein folding mechanisms and dynamics. 

 The KB model represents each amino acid by a single bead located at the alpha-carbon position. The potential energy function is derived from the native structure of the protein and includes terms for bonds, angles, dihedrals, and non-bonded interactions. This approach allows for efficient simulations while maintaining the essential features of protein folding landscapes. 

 Key features of the model include: 

 - Coarse-grained representation with one bead per residue 

 - Native-structure-based potential energy function 

 - Efficient simulation of large proteins and long timescales 

 - Option to include solvent-accessible surface area (SASA) calculations 

 - Ability to handle multi-chain proteins and protein complexes 

 The model reads protein structures from PDB files and can handle both local files and PDB IDs for direct download from the RCSB PDB database. 

 This model uses the [pyGrained]_ library to create the coarse-grained representation of the protein.

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
	* - SASA
	  - If true, calculates the Solvent Accessible Surface Area.
	  - bool
	  - False
	* - centerInput
	  - If true, centers the input structure.
	  - bool
	  - True
	* - aggregateChains
	  - If true, treats multiple chains as a single entity.
	  - bool
	  - True

Example:

.. code-block:: python

	{
		"type": "KB",
		"parameters":{
			"PDB": "1UBQ",
			"centerInput": True,
			"SASA": True,
			"aggregateChains": False
		}
	}

References:

	.. [Karanicolas2002] Karanicolas, J., & Brooks, C. L. (2002). The origins of asymmetry in the folding transition states of protein L and protein G. Protein Science, 11(10), 2351-2361.

	.. [Karanicolas2003] Karanicolas, J., & Brooks, C. L. (2003). Improved Gō-like models demonstrate the robustness of protein folding mechanisms towards non-native interactions. Journal of Molecular Biology, 334(2), 309-325.

	.. [Karanicolas2003b] Karanicolas, J., & Brooks, C. L. (2003). The structural basis for biphasic kinetics in the folding of the WW domain from a formin-binding protein: Lessons for protein design? Proceedings of the National Academy of Sciences, 100(7), 3954-3959.

	.. [pyGrained] https://github.com/PabloIbannez/pyGrained



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
	* - debyeFactor
	  - Factor to scale the Debye length. Used to set the cutoff distance for electrostatic interactions.
	  - float
	  - 4.0
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

Example:

.. code-block:: python

	{
		"type": "MADna",
		"parameters":{
			"sequence": "ATCGGATCCGAT",
			"debyeLength": 10.8,
			"dielectricConstant": 78.3,
			"debyeFactor": 4.0,
			"variant": "fast"
		}
	}

References:

	.. [Assenza2022] Assenza, S., & Pérez, R. (2022). Accurate Sequence-Dependent Coarse-Grained Model for Conformational and Elastic Properties of Double-Stranded DNA. Journal of Chemical Theory and Computation, 18(5), 3239-3256.



MAGNETICNP
----------

	:author: P. Palacios-Alonso

 MAGNETICNP model for simulating magnetic nanoparticles. This model implements a coarse-grained representation of magnetic nanoparticles, allowing for the simulation of their behavior under various conditions, including the application of external magnetic fields. 

 The model represents each nanoparticle as a single entity with properties such as size (hydrodynamic radius), magnetic moment, and anisotropy. This coarse-grained approach enables efficient simulations of large systems of magnetic nanoparticles, making it suitable for studying collective behaviors and responses to external stimuli. 

 Key features of the model include: - Customizable particle properties (size distribution, magnetic moment, anisotropy) 

 - Options for initial particle orientations (random or aligned) 

 - Flexibility in defining the number of particles and simulation box size 

 The model allows for easy integration with external field models and can be extended to include various inter-particle interactions.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - msat
	  - Saturation magnetization of the nanoparticles.
	  - float
	  - 
	* - nParticles
	  - Number of magnetic nanoparticles in the simulation.
	  - int
	  - 
	* - coreRadius
	  - Radius of the magnetic core of the nanoparticles.
	  - float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - initAxis
	  - Axis for initial alignment if 'aligned' orientation is chosen.
	  - list of float
	  - [0, 0, 1]
	* - coatingWidth
	  - Width of the coating layer on the nanoparticles.
	  - float
	  - 0.0
	* - coreRadiusStd
	  - Standard deviation of the core radius for size distribution.
	  - float
	  - 0.0
	* - coatingWidthStd
	  - Standard deviation of the coating width.
	  - float
	  - 0.0
	* - initOrientation
	  - Initial orientation of magnetic moments. Options: 'aligned' or 'random'.
	  - str
	  - aligned
	* - anisotropyStd
	  - Standard deviation of the anisotropy constant for particle-to-particle variation.
	  - float
	  - 0.0
	* - particleName
	  - Name identifier for the particle type.
	  - str
	  - A
	* - anisotropy
	  - Magnetic anisotropy constant of the nanoparticles.
	  - float
	  - 

Example:

.. code-block:: python

	{
		"type": "MAGNETICNP",
		"parameters":{
			"nParticles": 1000,
			"msat": 480000.0,
			"coreRadius": 5e-09,
			"coreRadiusStd": 1e-10,
			"anisotropy": 23000.0,
			"initOrientation": "random"
		}
	}



MEMBRANE
--------

.. warning::

	This model is currently under development. Please, use it with caution.



PARTICLE
--------

	:author: Pablo Ibáñez-Freire

 PARTICLE model for creating a single particle in a simulation. This simple model allows users to add a single particle with specified properties to the simulation environment. It's particularly useful for creating reference points, probes, or simple objects within a larger simulation context. 

 The model allows customization of various particle properties including: 

 - Name (type) of the particle 

 - Mass 

 - Radius 

 - Charge 

 - Initial position 

 This model can be used in conjunction with other models to create more complex systems. It's especially useful for testing and debugging purposes, or for creating simple scenarios to study specific interactions or behaviors.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - particleName
	  - Name or type of the particle.
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
	* - particleCharge
	  - Charge of the particle.
	  - float
	  - 0.0
	* - position
	  - Initial position of the particle in 3D space.
	  - list of float
	  - [0.0, 0.0, 0.0]
	* - particleRadius
	  - Radius of the particle.
	  - float
	  - 1.0
	* - particleMass
	  - Mass of the particle.
	  - float
	  - 1.0

Example:

.. code-block:: python

	{
		"type": "PARTICLE",
		"parameters":{
			"particleName": "probe",
			"particleMass": 2.5,
			"particleRadius": 0.5,
			"particleCharge": -1.0,
			"position": [10.0, 0.0, 5.0]
		}
	}



PROTEIN_IDP_PROTEIN
-------------------

.. warning::

	This model is currently under development. Please, use it with caution.



SBCG
----

	:author: Pablo Ibáñez-Freire

 SBCG (Shape-Based Coarse-Grained) model for protein simulations. This model implements a coarse-grained representation of proteins that maintains the overall shape and essential features while reducing computational complexity. 

 The SBCG approach represents proteins using a reduced number of beads, typically one bead for hundreds of atoms, capturing the protein. This reduction in degrees of freedom allows for simulations of larger systems and longer timescales compared to all-atom models. 

 Key features of the SBCG model include: 

 - Shape-preserving coarse-graining based on the input protein structure 

 - Flexible parameterization of the coarse-graining process 

 - Automatic generation of bonded and non-bonded interactions 

 - Support for multi-chain proteins and protein complexes 

 The model takes a PDB file as input and generates the coarse-grained representation based on the specified parameters. It can handle various levels of coarse-graining and allows for customization of the interaction potentials. 

 This model uses the [pyGrained]_ library to create the SBCG representation.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - steps
	  - Number of steps in the coarse-graining refinement process.
	  - int
	  - 
	* - bondsModel
	  - Model used for bonded interactions.(ENM or count)
	  - str
	  - 
	* - resolution
	  - Resolution of the coarse-graining, number of atoms per bead.
	  - float
	  - 
	* - nativeContactsModel
	  - Model used for native contact interactions (CA).
	  - str
	  - 
	* - PDB
	  - Path to the input PDB file or a valid PDB ID for download.
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
	* - SASA
	  - If true, calculates the Solvent Accessible Surface Area.
	  - bool
	  - False
	* - centerInput
	  - If true, centers the input structure.
	  - bool
	  - True
	* - aggregateChains
	  - If true, treats multiple chains as a single entity.
	  - bool
	  - True

Example:

.. code-block:: python

	{
		"type": "SBCG",
		"parameters":{
			"PDB": "1ABC",
			"resolution": 200,
			"steps": 1000,
			"bondsModel": "ENM",
			"nativeContactsModel": "CA",
			"SASA": True
		}
	}

References:

	.. [Arkhipov2006] Arkhipov, A., Freddolino, P. L., & Schulten, K. (2006). Stability and dynamics of virus capsids described by coarse-grained modeling. Structure, 14(12), 1767-1777.

	.. [pyGrained] https://github.com/PabloIbannez/pyGrained



SIMULATION
----------

	:author: Pablo Ibáñez-Freire

 SIMULATION model for loading pre-existing simulation configurations. This model allows users to import a complete simulation setup from a pyUAMMD simulation object, including particle positions, types, and force field parameters. It's particularly useful for continuing simulations from a previous state or for setting up complex initial configurations. 

 The model takes all necessary information from imported simulation object, including: - Particle types and their properties 

 - Particle positions and other state variables 

 - Structure information (particle IDs, types, etc.) 

 - Force field parameters and interactions 

 The SIMULATION model includes an option to selectively remove certain types of interactions from the imported simualtion.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - inputSimulation
	  - Simulation object to import. This object should contain all necessary information to set up the simulation.
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
	  - List of interaction types to remove from the imported simulation.
	  - list of str
	  - 

Example:

.. code-block:: python

	{
		"type": "SIMULATION",
		"parameters":{
			"inputSimulation": "simulationObject",
			"removeInteractionsByType": ['Bond2', 'NonBonded']
		}
	}



SOP
---

	:author: Pablo Ibáñez-Freire

 SOP (Self-Organized Polymer) model for protein folding and dynamics simulations. This model implements a coarse-grained representation of proteins based on the self-organized polymer concept, which captures the essential features of protein structure and dynamics while allowing for efficient simulations of large systems and long time scales. 

 The SOP model represents each amino acid by a single bead, located at the alpha-carbon position. The potential energy function includes terms for native contacts, chain connectivity, and excluded volume interactions. This approach allows for the study of protein folding, unfolding, and large-scale conformational changes. 

 Key features of the model include: - Coarse-grained representation with one bead per residue 

 - Native-contact-based potential energy function 

 - Efficient simulation of large proteins and long timescales 

 - Ability to handle multi-domain proteins and protein complexes 

 - Option to include solvent-accessible surface area (SASA) calculations 

 - Flexibility for customizing the energy scale of native contacts 

 The model reads protein structures from PDB files and can handle both local files and PDB IDs for direct download from the RCSB PDB database. 

 This model uses the [pyGrained]_ library to create the coarse-grained representation of the protein.

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
	* - SASA
	  - If true, calculates the Solvent Accessible Surface Area.
	  - bool
	  - False
	* - centerInput
	  - If true, centers the input structure.
	  - bool
	  - True
	* - epsilonNC
	  - Energy scale for native contacts.
	  - float
	  - 1.0
	* - aggregateChains
	  - If true, treats multiple chains as a single entity.
	  - bool
	  - True

Example:

.. code-block:: python

	{
		"type": "SOP",
		"parameters":{
			"PDB": "1AON",
			"centerInput": True,
			"SASA": False,
			"aggregateChains": True
		}
	}

References:

	.. [Hyeon2006] Hyeon, C., & Thirumalai, D. (2006). Forced-unfolding and force-quench refolding of RNA hairpins. Biophysical Journal, 90(10), 3410-3427.

	.. [Zhmurov2010] Zhmurov, A., Dima, R. I., Kholodov, Y., & Barsegov, V. (2010). SOP-GPU: Accelerating biomolecular simulations in the centisecond timescale using graphics processors. Proteins: Structure, Function, and Bioinformatics, 78(14), 2984-2999.

	.. [Hyeon2011] Hyeon, C., & Thirumalai, D. (2011). Capturing the essence of folding and functions of biomolecules using coarse-grained models. Nature Communications, 2(1), 1-11.

	.. [pyGrained] https://github.com/PabloIbannez/pyGrained



SPHEREMULTIBLOB
---------------

	:author: Pablo Ibáñez-Freire and Pablo Palacios-Alonso

 SPHEREMULTIBLOB model for creating spherical multiblob structures. This model generates a spherical particle represented by multiple smaller particles (blobs) arranged on its surface. The spherical particle can be created using either icosphere (a sphere placing blobs on the vertices of an icosahedron, or icosahedron iteratively subdivided) or icododecahedral (a sphere placing blobs on the vertices of an icosidodecahedron) geometry. 

 The model allows for the creation of spherical structures with varying levels of detail, making it useful for representing large spherical objects in coarse-grained simulations, such as colloidal particles, nanoparticles, or simplified representations of complex biological structures like virus capsids. 

 Key features of the SPHEREMULTIBLOB model include: 

 - Flexible control over the number of particles representing the sphere 

 - Option to use either icododecahedral or icosphere geometry 

 - Customizable particle properties (mass, radius, charge) 

 - Automatic generation of bonds between particles to maintain the spherical structure 

 - Optional steric interactions between particles 

 This model is particularly useful for studying the behavior of large spherical objects in various environments, their interactions with other particles or surfaces, and for simulations where the internal structure of the sphere needs to be represented explicitly.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - K
	  - Spring constant for bonds between particles.
	  - float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - heightStd
	  - Standard deviation of height for sphere placement.
	  - float
	  - 0.0
	* - sphereType
	  - Type of sphere geometry to use ('icosidodecahedron' or 'icosphere').
	  - str
	  - icosidodecahedron
	* - radiusOfSphere
	  - Radius of the overall spherical structure.
	  - float
	  - 1.0
	* - heightReference
	  - Reference height for sphere placement.
	  - float
	  - 0.0
	* - heightMean
	  - Mean height for sphere placement.
	  - float
	  - 0.0
	* - particlesPerSphere
	  - Number of particles per sphere.
	  - int
	  - 31
	* - numberOfSpheres
	  - Number of spheres to create.
	  - int
	  - 1
	* - particleCharge
	  - Charge of each particle.
	  - float
	  - 0.0
	* - particleRadius
	  - Radius of each particle.
	  - float
	  - 
	* - particleName
	  - Name or type of the particles making up the sphere.
	  - str
	  - 
	* - particleMass
	  - Mass of each particle.
	  - float
	  - 1.0

Example:

.. code-block:: python

	{
		"type": "SPHEREMULTIBLOB",
		"parameters":{
			"sphereType": "icosphere",
			"particleName": "blob",
			"particleRadius": 0.1,
			"numberOfSpheres": 5,
			"particlesPerSphere": 42,
			"radiusOfSphere": 2.0,
			"K": 100.0,
			"steric": True
		}
	}



STERIC_LAMBDA_SOLVATION
-----------------------

	:author: Pablo Ibáñez-Freire

 STERIC_LAMBDA_SOLVATION model for simulating solvation effects with steric interactions and lambda coupling. This model implements a coarse-grained representation of solvent particles interacting with solute molecules, incorporating both steric repulsion and a lambda parameter for coupling strength. 

 The model uses a soft-core potential to represent steric interactions, which allows for smooth transitions in free energy calculations. The lambda parameter can be used to gradually turn on or off the interactions, making this model particularly useful for free energy perturbation and thermodynamic integration studies. 

 Key features of the model include: 

 - Customizable concentration of solvent particles 

 - Adjustable steric interaction parameters (epsilon, cutoff) 

 - Lambda coupling for smooth free energy calculations 

 - Option to add a Verlet list for efficient neighbor searching 

 - Flexible boundary conditions with customizable box padding 

 The lambda coupling can be also used to create the inital conditions, starting from lambda=0 and gradually increasing the value to 1.

.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - concentration
	  - Concentration of the solute in the solvent (in N/V units).
	  - float
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - particleCharge
	  - Charge of the particle to be added to the system.
	  - float
	  - 0.0
	* - cutOffFactor
	  - Factor to multiply the sigma parameter to obtain the cut-off distance.
	  - float
	  - 1.5
	* - epsilon
	  - Epsilon parameter of the steric potential.
	  - float
	  - 1.0
	* - padding
	  - Padding to be added to the box to place the particle.
	  - list of two lists of three floats
	  - [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
	* - condition
	  - Condition for the interaction. Options: 'inter', 'intra', etc.
	  - str
	  - inter
	* - alpha
	  - Alpha parameter of the steric potential for soft-core behavior.
	  - float
	  - 0.5
	* - addVerletList
	  - If True, a Verlet list will be created for the interactions.
	  - bool
	  - True
	* - particleRadius
	  - Radius of the particle to be added to the system.
	  - float
	  - 1.0
	* - particleName
	  - Name of the particle to be added to the system.
	  - str
	  - W
	* - particleMass
	  - Mass of the particle to be added to the system.
	  - float
	  - 1.0

Example:

.. code-block:: python

	{
		"type": "STERIC_LAMBDA_SOLVATION",
		"parameters":{
			"concentration": 0.1,
			"epsilon": 1.0,
			"cutOffFactor": 2.0,
			"alpha": 0.5,
			"particleRadius": 0.5,
			"padding": [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
		}
	}

.. note::

	The model requires a ensemble with a lambda parameter. Otherwise, the simulation will fail.



WLC
---

	:author: Pablo Ibáñez-Freire

 WLC (Worm-Like Chain, [WLC]_) model for simulating polymer chains, particularly suitable for modeling DNA or other semi-flexible biopolymers. This model implements a discretized version of the continuous worm-like chain, representing the polymer as a series of connected beads with bending rigidity. 

 The WLC model captures the essential physics of semi-flexible polymers, including their entropic elasticity and persistence length. 

 Key features of the model include: 

 - Customizable number of beads to represent the polymer chain 

 - Adjustable bond length and bending rigidity 

 - Option to add excluded volume interactions (not included by default) 



.. list-table:: Required Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - N
	  - Number of particles (beads) in the chain.
	  - int
	  - 
.. list-table:: Optional Parameters
	:header-rows: 1
	:widths: 20 20 20 20
	:stub-columns: 1

	* - Name
	  - Description
	  - Type
	  - Default
	* - Kb
	  - Spring constant for bonds.
	  - float
	  - 1.0
	* - mass
	  - Mass of each particle.
	  - float
	  - 1.0
	* - Ka
	  - Spring constant for angles (bending rigidity).
	  - float
	  - 1.0
	* - typeName
	  - Name identifier for the particle type.
	  - str
	  - A
	* - b
	  - Equilibrium distance between consecutive particles.
	  - float
	  - 1.0

Example:

.. code-block:: python

	{
		"type": "WLC",
		"parameters":{
			"N": 100,
			"b": 0.34,
			"Kb": 100.0,
			"Ka": 2.0,
			"typeName": "DNA"
		}
	}

References:

	.. [WLC] https://en.wikipedia.org/wiki/Worm-like_chain



