In the "Types" category, we set the format for particle types. 
This means we fix the information available for each type. 
It is crucial to understand that we do not add the types themselves; 
this is handled by the models. 

.. code-block:: python

   # Types Example
   "types":[{"type":"basic","parameters":{"mass":1.0}}]

In this example, the "basic" component is added, allowing particle types to define three properties: mass, radius, and charge. 
By specifying mass = 1.0, it means that if not indicated when creating the type, the default mass will be 1.0.

The types are created by the models. For example, 
if we use a coarse-grained protein model where each amino acid is represented by a bead, 
it is expected that the type "ARG" (corresponding to Arginine) will be defined, specifying parameters such as mass, radius, and charge. 
Note that this assumes a selected unit system (in this case, "Kcal/mol)/A"); otherwise, an error might occur when processing the model. 
In summary, when selecting a type, we do not fix the types present in the simulation but their format. 
The model(s) we choose to use will add the types.

The list of available types is as follows:

