"""Prompt templates."""

def get_system_prompt() -> str:
    """Get the system prompt for the agent."""
    return """You are a helpful AI assistant that answers questions by using KoPL tools to query a knowledge base.

Your task is to:
1. Analyze the current state and question
2. Decide the next step to take
3. Use one tool at a time to gather information
4. Continue until you can answer the question

For example:
Question: how many former French regions were replaced by the region of France with the SIREN number 200053403?
Solving steps: FindAll().FilterStr(entities,SIREN number,200053403).FilterConcept(entities,region of France).Relate(entities,replaced by,backward).FilterConcept(entities,former French region).Count(entities)

[Rest of the prompt...]
""" 


def get_system_prompt() -> str:
    """Get the system prompt for the agent."""
    return """Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be three types: 
(1) Search[entity], which searches the exact entity on Wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.
(2) Lookup[keyword], which returns the next sentence containing keyword in the current passage.
(3) Finish[answer], which returns the answer and finishes the task.
Here are some examples."""


TOOL_CALLING_EXAMPLES = """
Question:
"""