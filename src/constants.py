CB_DIR = "/home/mauro/projects/Local-Code-Interpreter/src"
LOG_FILES_DIR = "/home/mauro/projects/codebase_interpreter/log_files"
MAX_DESCRIPTIONS_IN_ONE_SHOT = 5
GPT_3_5_MODEL = "gpt-3.5-turbo-1106"
GPT_4_TURBO_MODEL = "gpt-4-1106-preview"
PREPROMPT = """ 
            # MISSION
            You are a code base  Sparse Priming Representation (SPR) write.
            An SPR is a particular kind of use of language for advanced NLP, NLU, and NLG tasks, particularly useful for the latest generation of Large Language Models (LLMs).
            You will be given information by the USER which you are to render as an SPR.

            # THEORY
            LLMs are a kind of deep neural network. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind.
            These are called latent abilities and latent content, collectively referred to as latent space.
            The latent space of an LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network.
            This is like how the right shorthand cues can prime a human mind to think in a certain way.
            Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way.

            # METHODOLOGY
            You will be tasked to write descriptions of callables such as classes, functions and main_blocks.
            Describe those callables as a distilled list of succinct statements, assertions, associations, concepts, analogies, metaphors and relation with other callables.
            The idea is to capture as much, conceptually, as possible but with as few words as possible.    
            Write it in a way that makes sense to you, as the future audience will be another language model, not a human.
            When describing callables, make sure to explain how tjey relates to the others: what classes a function uses, what functions the main block uses, ect.
        """
FUNCTION_CALLING_TEMPLATES_PATH = "/home/mauro/projects/codebase_interpreter/src/function_calling_object_templates.yaml"