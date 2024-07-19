System components handle more technical aspects of the simulation. The mandatory System component in VLMP is "simulationName," 
which must always be present as it names the simulation. An optional component is "backup," which, if added, 
performs a simulation backup at specified intervals. Here is an example of the System category with two components, 
the mandatory "simulationName" and "backup":

.. code-block:: python

    "system":[
        {"type":"simulationName",
         "parameters":{"simulationName":"exampleName"}},
        {"type":"backup",
         "parameters":{"backupIntervalStep":1000,
                       "backupFilePath":"backup"}}
    ]

This example shows how, besides the simulation name, a backup component is added. 
This component will perform a backup every 1000 steps and save it in the file named "backup". 
When this component is added, it not only enables backup at certain intervals but also allows for rebooting the simulation 
if an error occurs.

The complete list of System components is as follows:

