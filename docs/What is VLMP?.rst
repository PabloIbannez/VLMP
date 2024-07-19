What is VLMP?
=============

An essential aspect of any simulation is the construction of the input. 
For instance, when simulating a protein, we need to incorporate information such as the protein structure 
(which could be contained into a PDB file we have to analyze), or in the case of DNA, the specific sequence of interest. 
From this initial information, a series of processes are applied to finally obtain a representation 
of the structure to be simulated along with the interactions that occur within it. 
This process can often be complex. Consider, for example, coarse grained protein models, 
where build the simplified representation requires an in-depth analysis of the structure of the protein [Karanicolas2002]_, 
or DNA models, where parameters for different bonds (pairwise, angular, or dihedral) 
vary based on the sequence [Assenza2022]_.

To simulate these systems, we need to implement algorithms for generating the input or use tools usually developed 
by authors for this purpose. However, imagine wanting to combine these models to study interactions between proteins and DNA. 
This task is not straightforward, it involves merging inputs (which may be in different formats) and adding interactions between them. 
This final step might even require modifying the code. In some cases, this would likely require programming in C/C++, CUDA, Fortran, or other languages, 
adding considerable complexity to the process and requiring increasingly specialized skills from the user.

To deal with such situations, we have developed the Virtual Lab Modeling Platform (VLMP), 
a tool that simplifies carrying out complex simulations and is specially designed for High-Performance Computing (HPC) environments. 
VLMP is implemented in Python which simplifies its use. 

VLMP understands a simulation as a collection of blocks, as if it were a building game. 
These different blocks can be used to build various simulations. 
Adding a new feature is akin to introducing a new block to the existing stack of available blocks.

In this documentation we will go deeper into VLMP, how it is designed and how to use its capabilities. This documentation is divided
in two main sections. The first section is the User Guide, which is intended for users who want to use VLMP to perform simulations.
The second section is the Developer Guide, which is intended for users who want to contribute to the development of VLMP.

.. [Karanicolas2002] Karanicolas, J., & Brooks III, C. L. (2002). The origins of asymmetry in the folding transition states of protein L and protein G. Protein Science, 11(10), 2351-2361.

.. [Assenza2022] Assenza, S., & Pérez, R. (2022). Accurate Sequence-Dependent Coarse-Grained Model for Conformational and Elastic Properties of Double-Stranded DNA. Journal of Chemical Theory and Computation, 18(5), 3239-3256.
