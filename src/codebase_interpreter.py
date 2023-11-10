import openai
import os
from os import path
import json
import yaml
from utils import *
import sys
# from colorama import Fore

setup_opena_AI_key()

GPT_MODEL = "gpt-4-1106-preview"

describe_class_function = {
    "name": "describe_code_base_classes",
    "description": "Stores SPRs of objects of the codebase.",
    "parameters": {
        "type": "object",
        "properties": {
            # Will be programatically filled.
        },
        "required": ["codebase_summary"],
    },
}

# Setup messages conversation
# Add preprompt
PREPROMPT = """ 
            # MISSION
            You are a Sparse Priming Representation (SPR) writer. An SPR is a particular kind of use of language for advanced NLP, NLU, and NLG tasks, particularly useful for the latest generation of Large Language Models (LLMs). You will be given information by the USER which you are to render as an SPR.

            # THEORY
            LLMs are a kind of deep neural network. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind. These are called latent abilities and latent content, collectively referred to as latent space. The latent space of an LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network. This is not unlike how the right shorthand cues can prime a human mind to think in a certain way. Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way.

            # METHODOLOGY
            Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human. Use complete sentences.
        """
messages = [
    {
        "role": "system", 
        "content": PREPROMPT,
    }
]

# Add raw code base to conversation
CB_DIR = "/home/mauro/projects/Local-Code-Interpreter/src"
python_files = [file for file in os.listdir(CB_DIR) if file.endswith(".py")]
cb_files_dict = {}
for file_name in python_files:
    with open(path.join(CB_DIR, file_name), 'r') as file:
        file_content = file.read()
        cb_files_dict[file_name] = file_content
        messages.append({"role": "system", "content": f"# {file_name}:\nfile_content"})

cb_description = ""

# Compress codebase into SPRs
MAX_DESCRIPTIONS_IN_ONE_SHOT = 5
for file_name, file_content in cb_files_dict.items():
    classes_names, _, _ = extract_classes_and_functions(path.join(CB_DIR, file_name))
    for class_name_i in range(0, len(classes_names), MAX_DESCRIPTIONS_IN_ONE_SHOT):
        classes_names_slice = classes_names[class_name_i:class_name_i + MAX_DESCRIPTIONS_IN_ONE_SHOT]

        # Create function call description
        for class_name in classes_names_slice:
            describe_class_function["parameters"]["properties"][class_name] = {
                "type": "object", 
                "properties" : {
                    "represents": {"type": "string", "description": f"description of what the {class_name} represents in the context of the codebase."},
                    "use_for": {"type": "string", "description": f"List of the case(s) and context(s) (can be just one case and context) in which the coder should use the class {class_name}."},
                }
            }
            
        # Debug
        # print(Fore.BLUE + "CB description function:" )
        # print(json.dumps(describe_class_function, indent=1))
        
        # Get completion
        response_completion = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=messages,
            functions=[describe_class_function],
            function_call={"name": "describe_code_base_classes"}
            )
            
        # convert completion into json object
        response_msg = response_completion.choices[0].message
        str_arguments = response_msg.function_call.arguments
        json_classes_descriptions = json.loads(str_arguments)

        # Check if the number of descriptions matches the number of class names in the slice
        nb_descriptions = len(json_classes_descriptions.items())
        if nb_descriptions != len(classes_names_slice):
            print("Erorr, nb_descriptions != len(classes_names_slice).", file=sys.stderr)
            print(f"nb_descriptions: {nb_descriptions}, len(classes_names_slice): {len(classes_names_slice)}.", file=sys.stderr)

        # convert json object into yaml string
        yaml_classes_descriptions = yaml.dump(json_classes_descriptions)
        
        # Debug
        # print(Fore.GREEN + "Assistant completion:")
        # print(json_classes_descriptions)
        print(yaml_classes_descriptions)

        # clean function description
        for class_name in classes_names_slice:
            describe_class_function["parameters"]["properties"].pop(class_name)
        
        # Store class description
        cb_description += (yaml_classes_descriptions)

#Logging
LOG_FILES_DIR = "/home/mauro/projects/codebase_interpreter/log_files"
log_file_name = f"SPR_class_descriptions_" + GPT_MODEL.replace('.','_') + "_log.yaml"
unique_log_file_name = generate_unique_filename(log_file_name, LOG_FILES_DIR)
with open(unique_log_file_name, 'w') as log_file:
    log_file.write(cb_description)