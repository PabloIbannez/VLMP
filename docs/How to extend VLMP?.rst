How to Extend VLMP
==================

VLMP can be extended by creating a Python file that defines a new component. These components can be of various types: **Systems**, **Units**, **Types**, **Ensembles**, **Models**, **ModelOperations**, **ModelExtensions**, **Integrators**, and **SimulationSteps**.


To extend VLMP, you need to create a Python file in the appropriate folder, based on the component type (e.g., `Systems`, `Models`). The file should define a class with the same name as the extension you are creating.


While each component type has its own specific requirements, which will be explained in later sections, all components generally follow the same structure. 

The class for the new module must include an `__init__` function that typically accepts the following parameters:

1. **type** (optional): The component type, which is inferred from the class name.
2. **name** (optional): A name for the component.
3. **availableParameters** (optional): A set of strings listing all the parameters that the module accepts.
4. **requiredParameters** (optional): A set of strings specifying the mandatory parameters needed when initializing the class.
5. **params**: A dictionary that includes any additional parameters listed in **availableParameters**.

Here’s an example of how to structure the `__init__` function for a component:

.. code-block:: python

   availableParameters = {"viscosity", "density", ...}
   requiredParameters  = {"viscosity"}

   def __init__(self, name, **params):
       super().__init__(_type = self.__class__.__name__,
                        _name = name,
                        availableParameters = self.availableParameters,
                        requiredParameters  = self.requiredParameters,
                        **params)


For developers who want to contribute to VLMP, the recommended approach is to fork the repository and develop the extension in your fork. Once the extension is fully developed and tested, you can submit a Pull Request (PR) to merge your changes into the main repository.
