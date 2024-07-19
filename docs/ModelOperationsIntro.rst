Model operations are processed after the models are added. 
These components apply transformations to the coordinates of the particles. 
VLMP has both simple transformations, like rotation or fixing the position of the particle, and more complex ones, 
such as distributing models within a volume:

.. code-block:: python

   # Model Operations
   "modelOperations":[{
    "type":"rotation",
    "parameters":{"axis":[1.0,0.0,0.0],
                  "angle":3.14,
                  "selection":"all"}},{
    "type":"distributeRandomly",
    "parameters":{"mode":{
                       "sphere":{
                           "radius":40.0,
                           "center":[0.0,0.0,0.0]
                       }
                   },
                  "avoidClashes":True,
                  "selection":"all"}}
                 ]

As seen, in most cases, model operations require specifying a selection of particles to apply them. 
In the above example, the keyword "all" is used, which selects all particles added to the simulation. 
As mentioned, models can also define selections:

.. code-block:: python

   # Model Operations Selection
   "modelOperations":[{
     "type":"setCenterOfMassPosition",
     "parameters":{"position":[0.0,0.0,0.0],
                   "selection":"dna basePairIndex 2"}}
                   ]

In this case, we would fix the position of the center of mass formed by the particles of the model named 
"dna" that belong to the second base pair. Model operations can be combined, and like the rest of the components, 
their processing order is ensured.

The full list of model operations is as follows:


