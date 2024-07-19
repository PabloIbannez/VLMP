Models are one of the central elements in VLMP. These components add particles to the simulation and 
can also include potentials and new particle types.

VLMP offers a wide range of models, from simple polymer models like WLC to coarse-grained models for large protein complexes like viruses.

Let's take the MADna model for coarse-grained DNA as an example:

.. code-block:: python

    "models":[{
               "name":"dna",
               "type":"MADna",
               "parameters":{"sequence":"GATACA",
                             "debyeLength":debyeLength}
               }]

As observed, this component takes the data necessary to generate the particles and the required potentials of the MADna model, 
such as the sequence or Debye length. However, it's important to note what is happening underneath. 
The model defines the types. In this case, it adds the types of the beads in the model. 
If the "basic" type is selected, the model will add the corresponding information for each bead, such as mass, radius, and charge. 
Subsequently, it will add the particles, first their position and then the definition of the topology. 
Each particle is assigned a type and structural information such as the base pair to which it belongs or the strand. 
Once this is done, the model will add the potentials. 
In this case, bonds for pairs, angular and dihedral potentials, and non-bonded interactions like the WCA or Debye-Huckel interaction. 
All this information is necessary to conduct the simulation with the model.

An important feature of models is that they can define selections. 
Selections can be used by other categories of components (modelOperations, modelExtensions, or simulationStep) 
to apply transformations or measure properties of certain particle groups. 
The MADna model defines several selections. For example, one of them is the "basePairIndex" selection that allows selecting 
base pairs according to their pair indices. For instance, the basePairIndex 2 will be the particles belonging to the second base pair.

It is important to note that different models can be combined. We can even place the same model several times:

.. code-block:: python

    "models":[
          {"name":"dna1",
           "type":"MADna",
           "parameters":{"sequence":"GATACA",
                         "debyeLength":debyeLength}
          },
          {"name":"dna2",
           "type":"MADna",
           "parameters":{"sequence":"ACATAG",
                         "debyeLength":debyeLength}
          }]

In this case, we simulate two DNA sequences. By adding a potential for their interaction, we could study DNA-DNA interaction phenomena.

VLMP incorporates a large number of models:

