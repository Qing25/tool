from typing import Any, Dict, List, Union
from smolagents.agents import ToolCallingAgent, populate_template
from smolagents.memory import ActionStep, AgentMemory, PlanningStep, SystemPromptStep, TaskStep, ToolCall
from smolagents.models import ChatMessage
from rich.panel import Panel
from rich.text import Text
from smolagents.utils import AgentGenerationError
from smolagents.agent_types import AgentAudio, AgentImage, AgentText, handle_agent_output_types
from smolagents.monitoring import (
    YELLOW_HEX,
    AgentLogger,
    LogLevel,
)
import datetime 

from qdls.kopl.util import ValueClass

def shorten_result(result) -> str:
    """
    Truncate long results showing only first element
    
    """
    if result is None:
        return None

    if isinstance(result[0], str):
        first_item = f"'{result[0]}'" 
    elif isinstance(result[0], dict):
        """ TODO 这里是否会导致 valueClass 的值无法区分 字符串 和 数值 """
        first_item = {k: str(v) if isinstance(v, ValueClass) else v for k, v in result[0].items()}
        # print_string(first_item)
    else:
        first_item = str(result[0])
    return f"[{first_item}, ... ]"


def craft_observation_simple(result, display_max=10) -> str:
    """
    the observation is the result of the tool execution (over 10 items will be shortened to 1)
    
    Args:
        result (list): The result of the tool execution
    """
    
    if type(result) == str or type(result) == int: # 直接返回结果
        return result 
    elif type(result) == list:      # 处理一下太长的
        if len(result) > display_max:
            return shorten_result(result)
        else:
            return str(result)
    elif type(result) == tuple:     # 处理一下太长的，ids, facts 分别
        ids, facts = result
        if len(ids) > display_max:
            return f"({shorten_result(ids)}, {shorten_result(facts)})" + f"\t(showing first of {len(result)} items)"
        return result 


class CachedToolCallingAgent(ToolCallingAgent):
    """A ToolCallingAgent with result caching to shorten input length in subsequent steps.
    The actual execution will use the full result from cache."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tool_result_cache = []  # 保存 tool call 的结果
        self._tool_call_history = []  # 保存 tool call 的历史记录


    def initialize_system_prompt(self) -> str:
        """ 
            在这里加入自己任务的调用示例，以及更多说明

            增加 varibles 中的 task_examples

        """
        origin_system_prompt_template = self.prompt_templates["system_prompt"]
        task_examples: List[str] = [
            """Question: Seymour Cassel got nominated for Academy Award for best supporting actor, tell me the subject of this statement.
Thought: ...
Action: {"tool": "Find", "args": {"name": "Seymour Cassel"}}
Observation: Output: (['Q708153'], None)\n Seymour Cassel is found, note as $0.
Thought: ... 
Action: {"tool": "Find", "args": {"name": "Academy Award for best supporting actor"}}
Observation: Output:(['Q106291'], None)\n Academy Award for best supporting actor is found, note as $1.
Thought: ...
Action: {"tool": "QueryRelationQualifier", "args": {"s_entities": "$0", "t_entities": "$1", "relation": "nominated for", "qkey": "statement is subject of"}}
Observation: Output: '41st Academy Awards'\nThe subject of the statement is 41st Academy Awards.
Final Answer: 41st Academy Awards""",
"""
Question: Does My Neighbor Totoro or Hannah Arendt, originally in German, possess the longer run-time?
Thought: I need to compare the run-time lengths of two films: My Neighbor Totoro and Hannah Arendt (in German) to determine which one is longer.  I will find entity "My Neighbor Totoro" first.
Action: {"tool": "Find", "args": {"name": "My Neighbor Totoro"}}
Observation: Output: (['Q39571'], None)\n My Neighbor Totoro is found, note as $0.
Thought: The second file "Hannah Arendt" is restricted to be a German film. Next, I will look up "German" to search for information on films originally in the German language.
Action: {"tool": "Find", "args": {"name": "German"}}
Observation: Output: (['Q188'], None)\n German is found, note as $1.
Thought: Now, I need to relate the German language to films that have German as their original language.  
Action: {"tool": "Relate", "args": {"entities": $1, "relation": "original language of film or TV show", "direction": "backward"}}
Observation: Output: (['Q150804', ...], [{'object': 'Q150804', 'direction':'backward', 'qualifiers': [], 'relation': 'original language of film or TV show'}, ...])\n All German films are returned, note as $2.
Thought: Then I need to locate the entity "Hannah Arendt" so that I can get the desired entity by intersecting the two sets. 
Action: {"tool": "Find", "args": {"name": "Hannah Arendt"}}
Observation: Output: (['Q60025', 'Q1575773'], None)\n There are two films named Hannah Arendt, note as $3.
Thought: A simple intersection of the two sets can result the film originally in German. 
Action: {"tool": "And", "args": {"entities": $2, "entities": $3}}
Observation: Output: (['Q1575773'], None)\n The film in the question is filtered out.
Thought: Now I can compare the duration of My Neighbor Totoro and the German-language Hannah Arendt.  
Action: {"tool": "SelectBetween", "args": {"l_entities": $0, "r_entities": $4, "key": "duration", "op": "greater"}}
Observation: Output: 'Hannah Arendt'\n The answer is found.
Final Answer: Hannah Arendt
"""
        ] 
        task_template = """{%- for eg in task_examples %}
  - {{ eg }}
  {%- endfor %}"""

        # 添加 kqa 的 tool call 示例
        system_prompt_template = origin_system_prompt_template.replace("Here are the rules you should always follow to solve your task:",
            f"Here are some usage examples of current accessible tools:\n{task_template}\n\nHere are the rules you should always follow to solve your task:")
        
        # 修改规则 2 
        system_prompt_template = system_prompt_template.replace("2. Always use the right arguments for the tools. Never use variable names as the action arguments, use the value instead.",
            "2. Always use the right arguments for the tools. Never use variable names as the action arguments, use the value instead.")
        # 添加规则 5、6
        system_prompt_template = system_prompt_template.replace("4. Never re-do a tool call that you previously did with the exact same parameters.",
            """4. Never re-do a tool call that you previously did with the exact same parameters.
5. If a argument is too long omitted using ..., you can use the cached results of previous tool calls by referring to them with the syntax $i, where i is the index of the tool call in the sequence starting from 0.
6. Answer precisely. The answer should be a name, a number, a date, or a yes/no.""")
        system_prompt = populate_template(
            system_prompt_template,
            variables={"tools": self.tools, "managed_agents": self.managed_agents, "task_examples": task_examples[1:]},
        )
        return system_prompt

    def execute_tool_call(self, tool_name: str, arguments: Union[Dict[str, str], str]) -> Any:
        """Execute tool with caching mechanism"""
            
        # Execute tool normally
        result = super().execute_tool_call(tool_name, arguments)        
        return result

    def resolve_arguments(self, arguments: Union[Dict[str, str], str]) -> Union[Dict[str, str], str]:
        """Resolve arguments by replacing placeholders with cached results
        
        for example:
        arguments: {"l_entities": "$0", "r_entities": "$4", "key": "duration", "op": "greater"}
        return: {"l_entities": self._tool_result_cache[0], "r_entities": self._tool_result_cache[4], "key": "duration", "op": "greater"}
        """
        R = None 
        if isinstance(arguments, dict):
            resolved_arguments = {}
            for key, value in arguments.items():
                if isinstance(value, str) and value.startswith('$'):
                    index = int(value[1:])
                    resolved_arguments[key] = self._tool_result_cache[index]
                else:
                    resolved_arguments[key] = value
            R = resolved_arguments
        elif isinstance(arguments, str) and arguments.startswith('$'):
            index = int(arguments[1:])
            R = self._tool_result_cache[index]
        else:
            R = arguments
        
        return {k: str(v) for k,v in R.items()}


    def step(self, memory_step: ActionStep) -> Union[None, Any]:
        """Perform one step in the ReAct framework with cached results"""
        memory_messages = self.write_memory_to_messages()
        
        # Add new step in logs
        memory_step.model_input_messages = memory_messages.copy()

        try:
            model_message: ChatMessage = self.model(
                memory_messages,
                tools_to_call_from=list(self.tools.values()),
                stop_sequences=["Observation:"],
            )
            memory_step.model_output_message = model_message
            if model_message.tool_calls is None or len(model_message.tool_calls) == 0:
                raise Exception("Model did not call any tools. Call `final_answer` tool to return a final answer.")
            tool_call = model_message.tool_calls[0]
            tool_name, tool_call_id = tool_call.function.name, tool_call.id
            tool_arguments = self.resolve_arguments(tool_call.function.arguments)

        except Exception as e:
            raise AgentGenerationError(f"Error in generating tool call with model:\n{e}", self.logger) from e

        memory_step.tool_calls = [ToolCall(name=tool_name, arguments=tool_arguments, id=tool_call_id)]
        self._tool_call_history.append((tool_name, tool_arguments))

        # Execute
        self.logger.log(
            Panel(Text(f"Calling tool: '{tool_name}' with arguments: {tool_arguments}")),
            level=LogLevel.INFO,
        )
        if tool_name == "final_answer":
            if isinstance(tool_arguments, dict):
                if "answer" in tool_arguments:
                    answer = tool_arguments["answer"]
                else:
                    answer = tool_arguments
            else:
                answer = tool_arguments
            if (
                isinstance(answer, str) and answer in self.state.keys()
            ):  # if the answer is a state variable, return the value
                final_answer = self.state[answer]
                self.logger.log(
                    f"[bold {YELLOW_HEX}]Final answer:[/bold {YELLOW_HEX}] Extracting key '{answer}' from state to return value '{final_answer}'.",
                    level=LogLevel.INFO,
                )
            else:
                final_answer = answer
                self.logger.log(
                    Text(f"Final answer: {final_answer}", style=f"bold {YELLOW_HEX}"),
                    level=LogLevel.INFO,
                )

            memory_step.action_output = final_answer
            return final_answer
        else:
            if tool_arguments is None:
                tool_arguments = {}
            observation = self.execute_tool_call(tool_name, tool_arguments)
            observation_type = type(observation)
            if observation_type in [AgentImage, AgentAudio]:
                if observation_type == AgentImage:
                    observation_name = "image.png"
                elif observation_type == AgentAudio:
                    observation_name = "audio.mp3"
                # TODO: observation naming could allow for different names of same type

                self.state[observation_name] = observation
                updated_information = f"Stored '{observation_name}' in memory."
            elif observation_type == AgentText: # mostly in current task kgtool
                if 'ValueClass: ' in observation:
                    observation = observation.replace('ValueClass: ', '')
                    observation = eval(observation) 
                    if isinstance(observation, list):       # 应该都是 list
                        result = [ValueClass(**v) for v in observation]
                    else:
                        # (['Q512699'], {'key': 'FIPS 6-4 (US counties)', 'value': {'type': 'string', 'value': '18105', 'unit': None}, 'qualifiers': {}})
                        qids, triples = observation 
                        result = (qids, 
                                  [ { k: ValueClass(**v) if type(v) is dict and 'unit' in v else v for k,v in triple.items()} 
                                    for triple in triples ]
                                )
                    
                elif observation == 'no' or observation == 'yes' or type(observation) == str:
                    result = observation
                else:
                    result = eval(observation)
                
                # Store result in cache
                self._tool_result_cache.append(result)


                updated_information = craft_observation_simple(result)
                updated_information = f"{updated_information}\nThe tool result above is stored in cache, use ${len(self._tool_result_cache)-1} to refer to it."
                
            else:
                updated_information = str(observation).strip()

            self.logger.log(
                f"Observations: {updated_information.replace('[', '|')}",  # escape potential rich-tag-like components
                level=LogLevel.INFO,
            )
            memory_step.observations = updated_information
            return None


