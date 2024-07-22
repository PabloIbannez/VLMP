Backend
=======

Currently, all the execution of VLMP code is performed using UAMMD-structured. In other words, VLMP constructs the input, 
and UAMMD-structured executes it. However, this does not necessarily have to be the case. 
VLMP is, in principle, agnostic with respect to the execution. 
VLMP essentially provides a series of tools to combine the components, which are relatively simple elements, 
to create complex simulations. The generated input is managed using pyUAMMD, but although it may seem counterintuitive due to its name, 
pyUAMMD, in terms of input management, is also agnostic with respect to UAMMD-structured. 

In this way, we can understand VLMP as a tool for constructing input for simulations. 
Once the input is constructed, pyUAMMD stores it in the UAMMD-structured format. 
This format is easily translatable to other formats such as the one used by Gromacs or Charmm . 
Currently, pyUAMMD does not have this capability, but implementing it is feasible. 
Doing so, VLMP would become a much more far-reaching tool since it could be used for creating input 
for multiple simulation software applications.
