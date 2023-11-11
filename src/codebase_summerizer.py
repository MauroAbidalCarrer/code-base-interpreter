import openai
import os
from os import path
import json
import yaml
from utils import *
import sys
from constants import *
import copy

def get_classes_description(classes_names, messages):
    # Initialize description object 
    json_classes_descriptions = {}

    # As long as their are classes to describe, call the API to get the descriptions.
    while len(classes_names) != 0:
        # Create function call description
        describe_classes_obj = copy.deepcopy(DESCRIBE_CLASS_OBJ)
        for class_name in classes_names:
            describe_classes_obj["parameters"]["properties"][class_name] = {
                "type": "object", 
                "properties" : {
                    "represents": {"type": "string", "description": f"description of what the {class_name} represents in the context of the codebase."},
                    "use_for": {"type": "string", "description": f"List of the case(s) and context(s) (can be just one case and context) in which the coder should use the class {class_name}."},
                }
            }
            
        # Get completion
        response_completion = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=messages,
            functions=[describe_classes_obj],
            function_call={"name": "describe_code_base_classes"}
            )
            
        # convert completion into json object
        response_msg = response_completion.choices[0].message
        str_arguments = response_msg.function_call.arguments
        json_classes_descriptions.update(json.loads(str_arguments))

        # Remove all the classes that have been described
        classes_names = [elem for elem in classes_names if elem not in list(json_classes_descriptions.keys())]

        # Debug
        print(yaml.dump(json_classes_descriptions, Dumper=CustomDumper))
        if len(classes_names) != 0:
            print(f"Warning, the classes {classes_names} have not been described.", file=sys.stderr)
            print("Rerunning the ChatCompletion...", file=sys.stderr)

    return json_classes_descriptions


if __name__ == "__main__":
    setup_opena_AI_key()

    # Setup messages conversation with preprompt
    messages = [{"role": "system", "content": PREPROMPT}]
    modules = get_modules_contents(CB_DIR)
    classes_to_module_dict = {}
    functions_to_module_dict = {}
    main_code_to_module_dict = {}
    for module_name, module_content in modules.items():
        classes_names, functions, main_code = extract_classes_and_functions(module_content)
        for class_name in classes_names:
            classes_to_module_dict[class_name] = module_name
        for function in functions:
            functions_to_module_dict[function] = module_name
        if main_code:
            main_code_to_module_dict[class_name] = module_name
        messages.append({"role": "system", "content": f"# {module_name}:\n{module_content}"})

    # Initialize code base description object
    cb_description = {}
    for file_name in list(modules.keys()):
        cb_description[file_name] = {}

    # Compress codebase into SPRs
    classes_names = list(classes_to_module_dict.keys())
    for class_name_i in range(0, len(classes_names), MAX_DESCRIPTIONS_IN_ONE_SHOT):
        # Obtain classes desciptions
        classes_names_slice = classes_names[class_name_i:class_name_i + MAX_DESCRIPTIONS_IN_ONE_SHOT]
        classes_descriptions = get_classes_description(classes_names_slice, messages)
        
        # Store classes descriptions
        for class_name in classes_names_slice:
            module_name = classes_to_module_dict[class_name]
            cb_description[module_name][class_name] = classes_descriptions[class_name]

    # Convert cb description object to YAML formatted string    
    cb_description = yaml.dump(cb_description, Dumper=CustomDumper)
    print(cb_description)

    #Logging
    log_file_name = f"SPR_class_descriptions_" + GPT_MODEL.replace('.','_') + "_log.yaml"
    unique_log_file_name = generate_unique_filename(log_file_name, LOG_FILES_DIR)
    with open(unique_log_file_name, 'w') as log_file:
        log_file.write(cb_description)