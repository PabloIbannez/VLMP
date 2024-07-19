Only one component is allowed in this category, as having more than one ensemble does not make sense. 

.. code-block:: python

   # Ensemble Example
   "ensemble":[{
            "type":"NVT",
            "parameters":{
                          "box":[100.0,100.0,100.0],
                          "temperature":300.0}
            }]

The units of the box and temperature are those given by the selected units. 
For example, if we have chosen "(Kcal/mol)/A" units, then the box size will be interpreted in angstroms and the temperature in Kelvin. 
Once the ensemble is set, the parameters defined are accessible to all subsequent components. 
For example, if we set the NVT ensemble, the rest of the components will be able to access both the box size and the temperature.

The list of available ensembles is:

