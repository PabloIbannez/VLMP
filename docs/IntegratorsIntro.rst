Integrators are crucial components in VLMP, responsible for the temporal evolution of the system. 
VLMP offers a large number of integrators. 

.. code-block:: python

    "integrators":[{
        "type":"BBK",
        "parameters":{"timeStep":0.02,
                      "frictionConstant":1.0,
                      "integrationSteps":1000000}}
    ],


Multiple integrators can be added to a single simulation. They will activate sequentially, 
following their order in the category list. 
This feature is particularly useful for processes like thermalization or avoiding steric clashes at the beginning of a simulation.

The list of integrators available in VLMP is:

