Simulation Steps are a diverse class of components. By adding simulation steps, we introduce specific operations or calculations 
to be performed at intervals during the simulation. Through this type of operation, 
we can perform a wide variety of calculations, such as measuring temperature or pressure. 
We can also calculate properties of the particles like stress or the forces acting on them. 
One of the most important uses is to save the state of the simulation at certain intervals. 
This can be done using the "saveState" component, where we can choose from several formats for the data output:

   .. code-block:: python

    "simulationSteps":[{
                        "type":"saveState",
                        "parameters":{"intervalStep":10000,
                                      "outputFilePath":"output",
                                      "outputFormat":"dcd"}
                                      }
                       ]

The complete list of available simulation steps is as follows:
