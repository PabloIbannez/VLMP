Components
==========

The central element of VLMP is the component. These components are akin to the building blocks of a construction set. 
By combining these blocks, various types of simulations can be configured. 
These simulations are then added to a simulation pool, which is ultimately processed and prepared for execution.

VLMP exploits the idea that any simulation, no matter how complex, can be broken down into a series of small interacting components. 
These components form the basis of the simulation and range from 
purely computational aspects like backup management to strictly physical elements such as the employed potentials. 
These components are versatile, capable of constructing more than one type of simulation. 
For example, if blocks add a model for a protein, one can construct a simulation for pulling experiments 
or incorporate this protein into a system to study protein-protein interaction phenomena. 
VLMP provides a set of blocks that can be combined in numerous ways to create a wide variety of simulations.

Developing these blocks can be relatively complex, but once created, they can be reused in other scenarios. 
This makes the modular design of these components extremely beneficial for sharing and collaboration. 
The fact that VLMP is programmed in a high-level language like Python significantly reduces the cost of developing new components. 
For instance, one can use libraries such as NumPy for system initialization or tools like Biopython and MDAnalysis 
for constructing coarse-grained models for proteins.

The implementation of components in VLMP is structured using dictionaries. 
Each component is defined with up to three entries: two mandatory fields, 'type' and 'name', and an optional 'parameters' field. 
The 'type' field is essential as it specifies the nature of the component.

.. code-block:: python

   # Component Example 1
    {
        "name":"componentName"
        "type":"componentType",
        "parameters":{
            "param1":"...",
            "param2": 1234,
            "param3": {"A":[1,2,3],"B":[4,5,6]},
            ...
        }
    }

Although the 'name' field is mandatory, it can be omitted. 
In such cases, the component assumes the 'type' as its name. 
This simplifies scenarios where the distinction between types and names is not critical. 
For example, in the following case, the name of the component would be "componentType".

.. code-block:: python

   # Component Example 2
   {
        "type":"componentType",
        "parameters":{
            "param1":"...",
            "param2": 1234,
            "param3": {"A":[1,2,3],"B":[4,5,6]},
            ...
        }
    }

Each component added to a simulation must have a unique name to ensure proper identification and handling within VLMP. 
The 'parameters' field, also structured as a dictionary, allows specification of the required data by the component to work properly.


.. code-block:: python

   # Component Example 3
   models:[{
         "type":"SOP",
         "parameters":{
            "PDB":"2CV5"
            }
        },{
         "type":"MADna",
         "parameters":{
            "sequence":"ATCAACGGCTGTCTAGCAGT"
            }
        }]
