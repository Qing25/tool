"""Query agent implementation."""
from typing import List, Dict, Any, Tuple, Optional
import openai
from loguru import logger
from omegaconf import DictConfig
import json
import os
from copy import deepcopy

from src_refactored.core.tools import KoPLTools
from src_refactored.core.vq_model import DecisionVQVAE
from src_refactored.utils.prompts import get_system_prompt
from qdls.data import save_json, load_json

class QueryAgent:
    """Agent for executing knowledge base queries."""
    
    def __init__(
        self,
        tools: List[Any],
        model_name: str,
        api_config: DictConfig,
        vq_config: Optional[DictConfig] = None
    ):
        """Initialize query agent.
        
        Args:
            tools: List of KoPL tools
            model_name: Name of the LLM model to use
            api_config: OpenAI API configuration
            vq_config: Optional VQ model configuration
        """
        self.tools = tools
        self.name2tool = {t.name: t for t in tools}
        self.model = model_name
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(
            api_key=api_config.api_key_env,
            base_url=api_config.base_url
        )
        
        # Initialize VQ model if enabled
        self.vq_model = None
        if vq_config:
            self.vq_model = DecisionVQVAE(
                input_dim=vq_config.input_dim,
                codebook_dim=vq_config.codebook_dim,
                codebook_size=vq_config.codebook_size,
                embedding_model=vq_config.embedding_model,
                bart_model=vq_config.bart_model
            )
            
    def execute_query(self, query: str) -> Tuple[List[Dict], str]:
        """Execute a query using the tools.
        
        Args:
            query: Query string
            
        Returns:
            Tuple of execution history and final response
        """
        history = []
        messages = [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": query}
        ]
        
        while True:
            # Format current state
            current_state = self._format_state(query, history)
            messages.append({"role": "user", "content": current_state})
            
            # Get next action from LLM
            response = self._call_llm(messages)
            
            # Check for final answer
            if "final_answer" in response:
                history.append(response)
                return history, f"Final Answer: {response['final_answer']}\n\nReasoning:\n" + \
                       "\n".join(f"Step {i+1}: {step['thought']}" 
                                for i, step in enumerate(history))
                                
            # Execute next tool action
            try:
                tool_name = response["action"]["tool"]
                result = self._execute_tool(tool_name, response["action"]["args"])
                
                history.append({
                    "thought": response["thought"],
                    "action": response["action"],
                    "result": str(result)
                })
                
                messages.append({
                    "role": "assistant",
                    "content": f"Executed {tool_name}, result: {result}"
                })
                
            except Exception as e:
                logger.error(f"Error executing tool {response['action']['tool']}: {str(e)}")
                result = f"Error: {str(e)}"
                
            if len(history) > 12:
                return history, "Too many steps, ending query."

    def _format_state(self, query: str, history: List[Dict]) -> str:
        """Format the current state for LLM input.
        
        Args:
            query: Original query string
            history: List of execution history steps
            
        Returns:
            Formatted state string
        """
        state = f"Question: {query}\n\nExecution history:\n"
        
        for i, step in enumerate(history, 1):
            state += f"\nStep {i}:\n"
            state += f"Thought: {step['thought']}\n"
            if "action" in step:
                state += f"Action: {step['action']['tool']}\n"
                try:
                    state += f"Arguments: {json.dumps(step['action']['args'])}\n"
                except:
                    state += f"Arguments: {step['action']} does not match the tool schema\n"
                state += f"Result: {step['result']}\n"
        
        state += "\nWhat should be the next step?"
        return state

    def _call_llm(self, messages: List[Dict[str, str]]) -> Dict:
        """Call LLM and parse response.
        
        Args:
            messages: List of conversation messages
            
        Returns:
            Parsed response dictionary
        """
        # Load tool schemas
        if not os.path.exists("tools_schema.json"):
            tools_schema = [t.schema for t in self.tools]
            tools_schema = [{'type': "function", 'function': t} for t in tools_schema]
            save_json(tools_schema, "tools_schema.json")
        else:
            tools_schema = load_json("tools_schema.json")

        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            tools=tools_schema
        )
        message = response.choices[0].message

        # Parse tool calls
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            return {
                "thought": message.content or "Executing next step",
                "action": {
                    "tool": tool_call.function.name,
                    "args": json.loads(tool_call.function.arguments)
                }
            }
        
        # Parse final answer
        try:
            final_answer = message.content.split("Final Answer: ")[1]
        except:
            logger.error(f"Error parsing final answer: {message.content}")
            final_answer = message.content
        
        return {
            "thought": "Providing final answer",
            "final_answer": final_answer
        }

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a single tool with given arguments.
        
        Args:
            tool_name: Name of tool to execute
            args: Tool arguments
            
        Returns:
            Tool execution result
        """
        try:
            # Process arguments
            processed_args = {}
            if args:
                for key, value in args.items():
                    if isinstance(value, dict) and "ids" in value and "triples" in value:
                        processed_args[key] = value
                    elif isinstance(value, tuple) and len(value) == 2:
                        processed_args[key] = {"ids": value[0], "triples": value[1]}
                    else:
                        processed_args[key] = value

            # Execute tool
            result = self.name2tool[tool_name]._func(**processed_args)
            last_step_result = deepcopy(result)
            
            # Format long results
            if len(str(result)) > 500:
                result = (
                    f"Result is too long, {len(result[0])} items returned. "
                    f"Preceding examples: {(result[0][:5], result[1][:5] if result[1] is not None else result[1])}."
                )
            
            logger.info(f"Executed {tool_name} with args {args}, result: {result}")
            return last_step_result, result
            
        except Exception as e:
            error_msg = f"Error executing tool {tool_name}: {str(e)}"
            logger.error(error_msg)
            return error_msg, error_msg 