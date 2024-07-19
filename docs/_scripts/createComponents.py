import pkgutil
import importlib
import inspect
import json
import copy

base = "VLMP.components"
available_components = ["systems",
                        "units", "types",
                        "ensembles",
                        "models", "modelOperations", "modelExtensions",
                        "integrators", "simulationSteps"]

def json_to_rst(js,availableParameters,requiredParameters):

    rst = ""

    if "author" in js:
        rst += f"\t:author: {js['author']}\n\n"
    if "description" in js:
        description = js["description"]
        rst += f"{description}\n\n"

    # Parameters info: name description type default

    for param in js["parameters"]:
        if "default" not in js["parameters"][param]:
            js["parameters"][param]["default"] = ""

    if len(requiredParameters) > 0:

        rst += f".. list-table:: Required Parameters\n"
        rst += f"\t:header-rows: 1\n"
        rst += f"\t:widths: 20 20 20 20\n"
        rst += f"\t:stub-columns: 1\n\n"
        rst += f"\t* - Name\n"
        rst += f"\t  - Description\n"
        rst += f"\t  - Type\n"
        rst += f"\t  - Default\n"

    for param in requiredParameters:

        if param in js["parameters"]:
            paramInfo = js["parameters"][param]
            rst += f"\t* - {param}\n"
            rst += f"\t  - {paramInfo['description']}\n"
            rst += f"\t  - {paramInfo['type']}\n"
            rst += f"\t  - {paramInfo['default']}\n"
        else:
            print(f"Warning: {param} not found in docstring")

    if len(availableParameters) - len(requiredParameters) > 0:
        rst += f".. list-table:: Optional Parameters\n"
        rst += f"\t:header-rows: 1\n"
        rst += f"\t:widths: 20 20 20 20\n"
        rst += f"\t:stub-columns: 1\n\n"
        rst += f"\t* - Name\n"
        rst += f"\t  - Description\n"
        rst += f"\t  - Type\n"
        rst += f"\t  - Default\n"

    for param in availableParameters:
        if param in requiredParameters:
            continue
        if param in js["parameters"]:
            paramInfo = js["parameters"][param]
            rst += f"\t* - {param}\n"
            rst += f"\t  - {paramInfo['description']}\n"
            rst += f"\t  - {paramInfo['type']}\n"
            rst += f"\t  - {paramInfo['default']}\n"
        else:
            print(f"Warning: {param} not found in docstring")

    if "example" in js:
        # Add an example inside a code block
        rst += f"\nExample:\n\n"
        rst += f".. code-block:: python\n\n"
        rst += "\t{"
        for param in js["example"]:
            if type(js["example"][param]) == str:
                rst += f"\n\t\t\"{param}\": \"{js['example'][param]}\","
            else:
                rst += f"\n\t\t\"{param}\": {js['example'][param]},"
        rst = rst[:-1] + "\n\t}\n\n"

    return rst

def process_string_value(key,value):

    if key not in value:
        raise ValueError(f"Key {key} not found")

    value_tmp = value

    string_pos = value_tmp.find(key) + len(key)

    string_start = value_tmp.find(":", string_pos) + 1

    char = value_tmp[string_start]
    quotes_count = 0

    pos = string_start
    open_dict_count = 0
    while quotes_count < 2:
        char = value_tmp[pos]
        if char == "\\":
            pos += 2
        elif char == "\"":
            if open_dict_count == 0:
                quotes_count += 1
            pos += 1
        elif char == "{":
            open_dict_count += 1
            pos += 1
        elif char == "}":
            open_dict_count -= 1
            pos += 1
        else:
            pos += 1
    string_end = pos

    string = value_tmp[string_start:string_end]
    value_tmp = value_tmp.replace(string, "\"\"")

    # Clean up the string
    # Remove all tabs and single newlines (double newlines are substituted with a single newline)
    string = string.strip()
    # Substitute all consecutive spaces with a single space
    string = " ".join(string.split())

    string = string.replace("\t", "")
    string = string.replace("\n\n", "SINGLE_NEWLINE")
    string = string.replace("\n", "")
    string = string.replace("SINGLE_NEWLINE", "\n")

    # Remove " from the beginning and end of the string
    string = string[1:-1]

    return value_tmp, string

def format_docstring(name,obj):

    print(f"Processing {name}")

    docstring = obj.__doc__

    try:
        availableParameters = obj.availableParameters
        requiredParameters  = obj.requiredParameters

        # Try to parse the docstring as JSON
        # If the description key exists, extract before parsing and replace it with an empty string
        if "description" in docstring:
            docstring,description = process_string_value("description",docstring)
            docstring,example     = process_string_value("example",docstring)
            doc = json.loads(docstring)
            doc["description"] = description
            doc["example"]     = json.loads(example)
        else:
            doc = json.loads(docstring)

        # Convert the JSON to rst
        rst = json_to_rst(doc,availableParameters,requiredParameters)
    except json.JSONDecodeError as e:
        print(f"Error parsing docstring for {name}, parsing as plain text.\nError message:\n    {e}")
        rst = docstring
    except:
        print(f"Error parsing docstring for {name}, parsing as plain text.")
        rst = docstring

    return name, rst

def iterate_classes_in_module(module):
    doc = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:

                if "Base" in name:
                    continue
                name,ds = format_docstring(name,obj)
                doc[name] = ds

    return doc

def iterate_submodules(package_name):
    doc = {}
    package = importlib.import_module(package_name)
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{modname}"
        if ispkg:
            iterate_submodules(full_module_name)  # Recursive call for subpackages
        else:
            module = importlib.import_module(full_module_name)
            doc.update(iterate_classes_in_module(module))  # Call the function to iterate over classes

    return doc

# Start the iteration from the root package

for component_type in available_components:

    doc = iterate_submodules(f"{base}.{component_type}")

    component_name = component_type[0].upper() + component_type[1:]
    fileName       = component_name + ".rst"

    with open(fileName, "w") as f:
        f.write(f"{component_name}\n")
        f.write("=" * len(component_name) + "\n\n")

        f.write(f".. include:: {component_name}Intro.rst\n\n")

        for name, docstring in doc.items():
            f.write(f"{name}\n")
            f.write("-" * len(name) + "\n\n")
            f.write(f"{docstring}\n\n")
