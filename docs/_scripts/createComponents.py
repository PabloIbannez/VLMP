import pkgutil
import importlib
import inspect

base = "VLMP.components"
available_components = ["systems", "units", "types", "ensembles", "models", "modelOperations", "modelExtensions", "integrators", "simulationSteps"]

def format_docstring(name,docstring):
    print(f"{name}:\n{docstring}\n")

def iterate_classes_in_module(module):
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                doc_string = obj.__doc__
                if "Base" in name:
                    continue
                format_docstring(name,doc_string)

def iterate_submodules(package_name):
    package = importlib.import_module(package_name)
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{modname}"
        if ispkg:
            iterate_submodules(full_module_name)  # Recursive call for subpackages
        else:
            module = importlib.import_module(full_module_name)
            iterate_classes_in_module(module)  # Call the function to iterate over classes

# Start the iteration from the root package

for component in available_components:
    iterate_submodules(f"{base}.{component}")
