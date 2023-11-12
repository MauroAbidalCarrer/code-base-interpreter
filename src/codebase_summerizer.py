import openai
import os
from os import path
import json
import yaml
from utils import *
import sys
from constants import *
import copy

def generate_function_call_oject(values, function_call_template):
    function_call_object = {
        "name": function_call_template["name"],
        "description": function_call_template["description"],
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }

    for value in values:
        fill_placeholders = lambda str: str.replace(function_call_template["placeholder"], value)
        object_properties = copy.deepcopy(function_call_template["properties_template"])
        object_name = value #fill_placeholders(function_call_template["property_name_template"])
        apply_to_strings_in_place(object_properties, fill_placeholders)
        function_call_object["parameters"]["properties"][object_name] = object_properties
        function_call_object["parameters"]["required"].append(object_name)

    return function_call_object

def get_callables_description(callables_names, describe_callable_FC_template, messages):
    # Initialize description object 
    callables_descriptions = {}

    # As long as their are classes to describe, call the API to get the descriptions.
    while len(callables_names) != 0:
        callables_names_slice = callables_names[:MAX_DESCRIPTIONS_IN_ONE_SHOT]
        describe_callables_FC = generate_function_call_oject(
            callables_names_slice,
            describe_callable_FC_template
        )
            
        # Get completion
        response_completion = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=messages,
            functions=[describe_callables_FC],
            function_call={"name": describe_callable_FC_template["name"]}
            )
            
        # convert completion into json object
        response_msg = response_completion.choices[0].message
        str_arguments = response_msg.function_call.arguments
        callables_descriptions.update(json.loads(str_arguments))

        # Remove all the classes that have been described
        callables_names = [elem for elem in callables_names if elem not in list(callables_descriptions.keys())]

        # Debug
        print("===========================================CLASSES DESCRIPTIONS")
        print(yaml.dump(json.loads(str_arguments), Dumper=CustomDumper))

    return callables_descriptions


if __name__ == "__main__":
    setup_opena_AI_key()

    # Setup messages conversation with preprompt
    messages = [{"role": "system", "content": PREPROMPT}]
    modules = get_modules_contents(CB_DIR)
    classes_to_module_dict = {}
    functions_to_module_dict = {}
    main_code_to_module_dict = {}
    for module_name, module_content in modules.items():
        classes_names, functions, main_block = extract_classes_and_functions(module_content)
        for class_name in classes_names:
            classes_to_module_dict[class_name] = module_name
        for function in functions:
            functions_to_module_dict[function] = module_name
        if main_block:
            main_code_to_module_dict[class_name] = module_name
        messages.append({"role": "system", "content": f"# {module_name}:\n{module_content}"})

    # Initialize code base description object
    cb_description = {}
    for file_name in list(modules.keys()):
        cb_description[file_name] = {}

    # Get function calling object templates
    with open(FUNCTION_CALLING_TEMPLATES_PATH, 'r') as funciton_calling_templates_file:
        funciton_calling_templates = yaml.safe_load(funciton_calling_templates_file)
        
    # Get callables summerazitions
    def summarize_callables(callables_to_module, describe_callable_FC_template):
        callables_names = list(callables_to_module.keys())
        callables_descriptions = get_callables_description(callables_names, describe_callable_FC_template, messages)
            
        # Store callables descriptions
        for callable_name in callables_descriptions:
            module_name = callables_to_module[callable_name]
            cb_description[module_name][callable_name] = callables_descriptions[callable_name]
    
    # summarize_callables(classes_to_module_dict, funciton_calling_templates["describe_classes"])
    summarize_callables(functions_to_module_dict, funciton_calling_templates["describe_functions"])

    # Convert cb description object to YAML formatted string    
    cb_description = yaml.dump(cb_description, Dumper=CustomDumper)
    print(cb_description)

    #Logging
    log_file_name = f"SPR_class_descriptions_" + GPT_MODEL.replace('.','_') + "_log.yaml"
    unique_log_file_name = generate_unique_filename(log_file_name, LOG_FILES_DIR)
    with open(unique_log_file_name, 'w') as log_file:
        log_file.write(cb_description)