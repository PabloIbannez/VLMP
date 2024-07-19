Model extensions modify models, but unlike model operations, they do not alter the position of the particles; 
rather, they add interactions. An example of this type of interactions could be external potentials. 
Imagine that we have added a set of models as for example the models needed to simulate a protein virus. 
As we add it this virus will be in a vacuum but it is likely that we want to add a surface. 
This can be done by means of a model extension:

.. code-block:: python

   # Surface Example
   "modelExtensions":[{
     "type":"surface",
     "parameters":{"epsilon":1.0,
                   "sigma":1.0,
                   "surfacePosition":0.0,
                   "selection":"all"}}
                  ]

Other external potentials that can be added are the many body bonds. 
By adding these types of interactions we can perform pulling experiments. 
By combining this extension with a protein model or a DNA model we can simulate what would be an optical tweezers experiment:

.. code-block:: python

   # Force Example
   "modelExtensions":[{
                     "type":"constantForceBetweenCentersOfMass",
                     "parameters":{
                         "force":150.0,
                         "selection1":"dna basePairIndex  2",
                         "selection2":"dna basePairIndex -2"
                     }}
                  ]

Similar to how it happens with model operations, when we add model extensions, 
we can also (sometimes it's mandatory, depending on the extension) add a selection so that the extension 
only applies to a subset of the particles. 
In the previous example, we applied a constant force between the centers of mass of two sets of particles. 
Therefore, the model extension requires declaring two sets. 
This is done by indicating two selections, in both of which we select the model named "dna" 
and the selection type called "basePairIndex". In one case, we indicate the base pair 2, and in the other, the -2. 
This means that the sets will be composed of the particles that make up the second-to-last base pair of the model 
called "dna" and another set with the penultimate base pair. It's important to mention that for this to not produce an error, 
it's necessary to effectively add a model called "dna" which allows a selection called "basePairIndex". 
In other words, we need the model to define this selection and take the appropriate parameters. 
If this is not done, the VLMP will emit an error and terminate the execution.

Another type of extension would be those that add interaction models among the entities in the simulation. 
In particular, VLMP offers models for interactions: protein-protein, DNA-protein, and protein-lipids for protein, 
DNA, and lipid models with C_α resolution. 

The full list of model extensions is as follows:

