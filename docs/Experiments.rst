Experiments
===========

VLMP has a higher layer of abstraction, the experiments. 
In certain occasions, certain types of simulations have elements in common. 
To understand this, let's present an example, the simulation of an AFM indentation. 
To construct an AFM simulation with VLMP, we must add several common elements such as a surface, the AFM tip, 
and the interaction between the AFM tip and the sample, but these types of elements are common in all simulations of this kind. 
Among simulations, what changes is the sample. 

With this idea in mind, we can construct certain procedures in such a way that when we want to simulate an AFM, 
we only need to indicate the specific parameters of the sample. 
These types of generalizations are what motivate the experiments. 

The list fo currently available experiments is:

.. include:: AvailableExperiments.rst
