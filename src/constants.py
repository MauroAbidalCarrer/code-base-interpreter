OPENAI_SEED=21345
CB_DIR = "/home/mauro/projects/Local-Code-Interpreter/src"
LOG_FILES_DIR = "/home/mauro/projects/codebase_interpreter/log_files"
MAX_DESCRIPTIONS_IN_ONE_SHOT = 6
GPT_3_5_MODEL = "gpt-3.5-turbo-1106"
GPT_4_TURBO_MODEL = "gpt-4-1106-preview"
CALLABLE_NAME = "python callables"
# PREPROMPT = """
#             You are an expert python code documenter, your goal is to generate documentation that are as token efficent as possible.
#             Use expert level terms, python and computer science vocabulary as much as possible.
#             Document the python callables as relations to each other.
#             Your documentation will be read by an expert.

            

#             example_code:
#             ```python
#             def fit(self, x, y):
#                 \"\"\"
#                 Args:
#                     x ndarray, shape(n_epochs, n_channels, n_samples/times): epochs
#                     y ndarray, shape(n_epochs): event labels there must be 2 unique values
#                 Returns:
#                     self
#                 \"\"\"
#                 unique_labels = np.unique(y)
#                 n_unique_labels = len(unique_labels)
#                 if n_unique_labels != 2: 
#                     raise ValueError(f"Could not fit CSP, there are \{n_unique_labels\} unique labels. Two were expected.")

#                 def mean_cov_of_class(class_index):
#                     class_label = unique_labels[class_index]
#                     class_epochs_mask = np.where(y==class_label)
#                     class_epochs = x[class_epochs_mask]
#                     return np.mean([covarianceMatrix(epoch) for epoch in class_epochs], axis=0)

#                 self.filters_ = spatialFilter(mean_cov_of_class(1), mean_cov_of_class(0))
#                 self.patterns_ = pinv(self.filters_)
                
#                 return self

#             ```

#             example_description:

# """
PREPROMPT = f""" 
            # MISSION
            You are a code base Sparse Priming Representation (SPR) write.
            An SPR is a particular kind of use of language for advanced NLP, NLU, and NLG tasks, particularly useful for the latest generation of Large Language Models (LLMs).
            You will be given python code by the SYSTEM which you are to render as an SPR.

            # THEORY
            LLMs are a kind of deep neural network. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind.
            These are called latent abilities and latent content, collectively referred to as latent space.
            The latent space of an LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network.
            This is like how the right shorthand cues can prime a human mind to think in a certain way.
            Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way.

            # METHODOLOGY
            You will be tasked to write SPR descriptions of {CALLABLE_NAME}.
            Describe those {CALLABLE_NAME} as a distilled list of succinct statements, assertions, associations, concepts, analogies to computer science terms, metaphors and relations with other {CALLABLE_NAME}.
            The idea is to capture as much, conceptually, as possible but with as few words as possible.    
            Write it in a way that makes sense to you, as the future audience will be another language model, not a human.
            When describing {CALLABLE_NAME}, make sure to explain how they relate to the others: what classes a function uses, what functions the main block uses, ect.
            Use python vocabulary in your descriptions.
        """
FUNCTION_CALLING_TEMPLATES_PATH = "/home/mauro/projects/codebase_interpreter/src/function_calling_object_templates.yaml"
TEMPERATURE = 0