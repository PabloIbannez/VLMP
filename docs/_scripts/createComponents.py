import pkgutil
import importlib
import inspect
import json
import copy
import re
from collections import OrderedDict

base = "VLMP.components"
available_components = ["systems",
                        "units", "types",
                        "ensembles",
                        "models", "modelOperations", "modelExtensions",
                        "integrators", "simulationSteps"]

def fix_multiline_json(json_string):
    # Fix multiline strings
    json_string = re.sub(r'"\s*(\S[^"]*?\S)\s*"', lambda m: '"{}"'.format(m.group(1).replace('\n', ' ')), json_string, flags=re.DOTALL)

    # Remove trailing commas
    json_string = re.sub(r',\s*}', '}', json_string)
    json_string = re.sub(r',\s*]', ']', json_string)

    return json_string

def json_to_rst(js,availableParameters,requiredParameters,
                   availableSelections,requiredSelections):

    rst = ""

    if "author" in js:
        rst += f"\t:author: {js['author']}\n\n"
    if "image" in js:
        path2image = "_images/" + js["image"]
        rst += f"\t.. figure:: {path2image}\n"
        rst += f"\t\t:align: center\n"
        rst += "\t\t:width: 80%\n"
        # Add empty caption
        rst += "\n"


    if "description" in js:
        description = js["description"]
        # Substitute tag <p> with a newline
        description = description.replace("<p>", "\n\n")
        rst += f" {description}\n\n"

    # Parameters info: name description type default

    if "parameters" in js:
        for param in js["parameters"]:
            if "default" not in js["parameters"][param]:
                js["parameters"][param]["default"] = ""
            else:
                defaultParam = js["parameters"][param]["default"]
                if defaultParam == None or defaultParam == "null":
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
                # Use yellow color for warnings
                print(f"\033[93mWarning\033[0m: {param} not found in docstring")

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
                print(f"\033[93mWarning\033[0m: {param} not found in docstring")

    if "selections" in js:

        if len(requiredSelections) > 0:
            rst += f".. list-table:: Required Selections\n"
            rst += f"\t:header-rows: 1\n"
            rst += f"\t:widths: 20 20 20\n"
            rst += f"\t:stub-columns: 1\n\n"
            rst += f"\t* - Name\n"
            rst += f"\t  - Description\n"
            rst += f"\t  - Type\n"

        for selection in requiredSelections:
            if selection in js["selections"]:
                selectionInfo = js["selections"][selection]
                rst += f"\t* - {selection}\n"
                rst += f"\t  - {selectionInfo['description']}\n"
                rst += f"\t  - {selectionInfo['type']}\n"
            else:
                print(f"\033[93mWarning\033[0m: {param} not found in docstring")

        if len(availableSelections) - len(requiredSelections) > 0:
            rst += f".. list-table:: Optional Selections\n"
            rst += f"\t:header-rows: 1\n"
            rst += f"\t:widths: 20 20 20\n"
            rst += f"\t:stub-columns: 1\n\n"
            rst += f"\t* - Name\n"
            rst += f"\t  - Description\n"
            rst += f"\t  - Type\n"

        for selection in availableSelections:
            if selection in requiredSelections:
                continue
            if selection in js["selections"]:
                selectionInfo = js["selections"][selection]
                rst += f"\t* - {selection}\n"
                rst += f"\t  - {selectionInfo['description']}\n"
                rst += f"\t  - {selectionInfo['type']}\n"

    if "example" in js:
        # Add an example inside a code block
        rst += f"\nExample:\n\n"
        rst += f".. code-block:: python\n\n"
        rst += "\t{"
        for param in js["example"]:
            if type(js["example"][param]) == str:
                rst += f"\n\t\t\"{param}\": \"{js['example'][param]}\","
            else:
                if param == "parameters":
                    rst += f"\n\t\t\"parameters\":{{"
                    for p in js["example"][param]:
                        if type(js["example"][param][p]) == str:
                            rst += f"\n\t\t\t\"{p}\": \"{js['example'][param][p]}\","
                        else:
                            rst += f"\n\t\t\t\"{p}\": {js['example'][param][p]},"
                    rst = rst[:-1] + "\n\t\t},"
                else:
                    rst += f"\n\t\t\"{param}\": {js['example'][param]},"
        rst = rst[:-1] + "\n\t}\n\n"

    if "references" in js:
        rst += f"References:\n\n"
        for ref in js["references"]:
            rst += f"\t{ref}\n\n"

    # Special boxes
    if "note" in js:
        rst += f".. note::\n\n"
        rst += f"\t{js['note']}\n\n"

    if "warning" in js:
        rst += f".. warning::\n\n"
        rst += f"\t{js['warning']}\n\n"

    if "tip" in js:
        rst += f".. tip::\n\n"
        rst += f"\t{js['tip']}\n\n"

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
    #print("start",string)
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

    #print("final",string)

    return value_tmp, string

def format_docstring(name,obj):

    docstring = obj.__doc__

    try:
        availableParameters = obj.availableParameters
        requiredParameters  = obj.requiredParameters

        try:
            availableSelections = obj.availableSelections
            requiredSelections  = obj.requiredSelections
        except:
            availableSelections = None
            requiredSelections  = None

        docstring = fix_multiline_json(docstring)

        ## Try to parse the docstring as JSON
        ## If the description key exists, extract before parsing and replace it with an empty string
        if "description" in docstring:
            docstring,description = process_string_value("description",docstring)
            docstring,example     = process_string_value("example",docstring)
            doc = json.loads(docstring)
            doc["description"] = description
            doc["example"]     = json.loads(example)
        else:
            doc = json.loads(docstring)

        # Convert the JSON to rst
        rst = json_to_rst(doc,availableParameters,requiredParameters,
                              availableSelections,requiredSelections)
        #Print Success using green color
        print(f"\033[92mSuccess\033[0m -> {name}")
    except Exception as e:
        print(f"\033[91mError\033[0m -> {name}. \nError message:\n    {e}")
        print(f"Docstring:\n{docstring}")
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
    doc = OrderedDict()
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

    #Sort the dictionary in alphabetical order
    doc = OrderedDict(sorted(doc.items()))

    component_name = component_type[0].upper() + component_type[1:]
    fileName       = component_name + ".rst"

    ref_list = []
    for name in doc:
        ref_list.append(f"{name}")

    with open(fileName, "w") as f:
        f.write(f"{component_name}\n")
        f.write("=" * len(component_name) + "\n\n")

        f.write(f".. include:: {component_name}Intro.rst\n\n")

        for ref in ref_list:
            f.write(f"- :ref:`{ref}`\n\n")

        f.write("\n\n")

        for name, docstring in doc.items():
            f.write(f"----\n\n")
            f.write(f"{name}\n")
            f.write("-" * len(name) + "\n\n")
            f.write(f"{docstring}\n\n")
