# Code base interpreter
*A code interpreter for an entire code base.*

## Goal
The goal is to have an assistant that can interact with a code base the same way code interpreter can interact with a dataset.  

## Solution
Feeding an entire codebase is possible with GPT4-turbo... but it would cost a lot to feed the entire CB for every run.  
To feed in the entire code base we first summarize it as a list of key-values.  
Keys can be 