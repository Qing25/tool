from typing import List, Dict, Any, Tuple
import openai
import json
from loguru import logger
import os 
# from kopl_tools import KoPLTools, EntityTuple
from autogen_tools import KoPLTools
from autogen_core import CancellationToken

from copy import deepcopy
from qdls.data import save_json, load_json

import torch
from vector_quantize_pytorch import VectorQuantize
from transformers import BartForConditionalGeneration, BartTokenizer
from vq_decision import DecisionVQVAE, BartActionDecoder

class QueryAgent:
    def __init__(self, client: openai.OpenAI, tools: KoPLTools, model: str, use_vq=False):
        self.tools = tools
        self.name2tool = {t.name: t for t in self.tools}
        self.client = client 
        self.model = model
        self.use_vq = use_vq
        if use_vq:
            self.vq_model = DecisionVQVAE()
            self.bart_decoder = BartActionDecoder()
            self.load_decision_models()
        
    def _get_system_prompt(self) -> str:
        return """You are a helpful AI assistant that answers questions by using KoPL tools to query a knowledge base.

Your task is to:
1. Analyze the current state and question
2. Decide the next step to take
3. Use one tool at a time to gather information
4. Continue until you can answer the question

For example:
Question: how many former French regions were replaced by the region of France with the SIREN number 200053403?
Solving steps: FindAll().FilterStr(entities,SIREN number,200053403).FilterConcept(entities,region of France).Relate(entities,replaced by,backward).FilterConcept(entities,former French region).Count(entities)

You should first call FindAll() to get all entities.
Then call FilterStr(entities,SIREN number,200053403) to filter the entities with the property SIREN number equals 200053403. entities is the output of last tool usage.
Then call FilterConcept(entities,region of France) to filter the entities that is instance of the concept "region of France".
Then call Relate(entities,replaced by,backward) to find the entities that are replaced by the region of France. For Relate, the first argument is the relation name, the second argument is the direction of the relation, backward or forward.
Then call FilterConcept(entities,former French region) to filter the entities that is instance of the concept "former French region".
Finally, call Count(entities) to count the number of entities.

If you have the final answer, output the answer directly with the format:
"Final Answer: {answer}"

Tips:
If the result is too long and truncated, it is ok. As all results are returned by FindAll, you should consider next tool usage and set its first argument `entities` to a string "Last step result" as the input of the next step.
For example, FindAll() -> FilterStr("Last step result", SIREN number,200053403)

"""

    def _format_state(self, query: str, history: List[Dict]) -> str:
        """Format the current state for LLM"""
        state = f"Question: {query}\n\nExecution history:\n"
        
        for step in history:
            state += f"\nStep {len(history)}:\n"
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
        """Call LLM and parse response"""
        if not os.path.exists("tools_schema.json"):
            tools_schema = [t.schema for t in self.tools] 
            # for tool in tools_schema:
            #     tool['strict'] = True
                # tool['parameters']['additionalProperties'] = False
            tools_schema = [{'type':"function", 'function': t } for t in tools_schema]
            save_json(tools_schema, "tools_schema.json")
        else:
            tools_schema = load_json("tools_schema.json")
  
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            tools=tools_schema
        )
        message = response.choices[0].message

        # 处理工具调用响应
        if message.tool_calls:
            # 获取第一个工具调用（因为我们的格式只需要一个动作）
            tool_call = message.tool_calls[0]
            return {
                "thought": message.content or "Executing next step",
                "action": {
                    "tool": tool_call.function.name,
                    "args": json.loads(tool_call.function.arguments)
                }
            }
        else:
            # 如果没有工具调用，则认为是最终答案
            # try:
            #     # 尝试解析 JSON 格式的响应
            #     json_str = message.content.replace("```json", "").replace("```", "").strip()
            #     return json.loads(json_str)
            # except json.JSONDecodeError as e:
            #     # 如果不是 JSON 格式，假设这是一个最终答案
            #     return {
            #         "thought": "Providing final answer",
            #         "final_answer": message.content
            #     }
            try:
                final_answer = message.content.split("Final Answer: ")[1]
            except:
                logger.error(f"Error parsing final answer: {message.content}")
                final_answer = message.content
            return {"thought": "Providing final answer", "final_answer": final_answer}

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a single tool with given arguments"""
        try:
            # Process arguments that are results from previous steps
            processed_args = {}
            if args is not None or len(args) > 0:
                for key, value in args.items():
                    if isinstance(value, dict) and "ids" in value and "triples" in value:
                        processed_args[key] = value
                    elif isinstance(value, tuple) and len(value) == 2:
                        processed_args[key] = {"ids": value[0], "triples": value[1]}
                    else:
                        processed_args[key] = value
            else:
                pass 

            result = self.name2tool[tool_name]._func(**processed_args)
            last_step_result = deepcopy(result)
            if len(str(result)) > 500:
                # input("result is too long, press enter to continue")
                result = f"Result is too long, {len(result[0])} items returned. Preceding examples: {(result[0][:5], result[1][:5] if result[1] is not None else result[1])}."
            logger.info(f"Executed {tool_name} with args {args}, result: {result}")
            return last_step_result,result
        except Exception as e:
            error_msg = f"Error executing tool {tool_name}: {str(e)}"
            logger.error(error_msg)
            return error_msg, error_msg

    def load_decision_models(self, vq_path="models/vq_vae.pt"):
        if os.path.exists(vq_path):
            self.vq_model.load_state_dict(torch.load(vq_path))

    def _encode_observation(self, history: list) -> torch.Tensor:
        observations = " ".join([f"{step['thought']} {step.get('result','')}" 
                               for step in history[-3:]])
        return self._text_to_embedding(observations)
    
    def _text_to_embedding(self, text: str) -> torch.Tensor:
        inputs = self.client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return torch.tensor(inputs.data[0].embedding)
    
    def _vq_based_decision(self, observation: torch.Tensor, context: str) -> dict:
        with torch.no_grad():
            _, indices, _ = self.vq_model(observation.unsqueeze(0))
        action_str = self.bart_decoder.decode_action(indices[0], context)
        try:
            return json.loads(action_str.replace("'", '"'))
        except:
            return {"tool": "FinalAnswer", "args": {"answer": action_str}}

    def execute_query(self, query: str) -> str:
        history = []
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": query}
        ]
        
        while True:
            if self.use_vq and len(history) >= 2:
                observation = self._encode_observation(history)
                action = self._vq_based_decision(observation, query)
                # 解析action并执行工具...
            else:
                # Get next step from LLM
                current_state = self._format_state(query, history)
                messages.append({"role": "user", "content": current_state})
                
                response = self._call_llm(messages)
                
                # Check if we have a final answer
                if "final_answer" in response:
                    history.append(response)
                    return history, f"Final Answer: {response['final_answer']}\n\nReasoning:\n" + \
                           "\n".join(f"Step {i+1}: {step['thought']}" 
                                    for i, step in enumerate(history))
                elif len(history) > 12:
                    return history, "Too many steps, end the query."
                
                # Execute the next step
                # logger.info(f"Executing step: {response['thought']}")
                logger.info(f"Raw response: {response}")
                try:        
                    tool_name = response["action"]["tool"].replace("functions.", "")   # Error executing tool functions.FilterStr: 'functions.FilterStr' 非常常见
                    
                    # 使用上一轮的结果作为输入 entities
                    if "entities" in response["action"]["args"] and response["action"]["args"]["entities"] == "Last step result":
                        response["action"]["args"]["entities"] = last_step_result

                    last_step_result, result = self._execute_tool(
                        tool_name=tool_name,
                        args=response["action"]["args"]
                    )
                except Exception as e:
                    logger.error(f"Error executing tool {response['action']['tool']}: {str(e)}")
                    # input("Error executing tool, press enter to continue")
                    result = f"Error executing tool {response['action']['tool']}: {str(e)}"
                
                # Record the step and its result
                history.append({
                    "thought": response["thought"],
                    "action": response["action"],
                    "result": str(result)
                })
                
                # Add the result to the conversation
                messages.append({
                    "role": "assistant",
                    "content": f"Executed {response['action']['tool']}, result: {result}"
                }) 



    def execute_query_with_depart(self, query: str, depart: str) -> str:
        history = []
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": query}
        ]
        
        while True:

            pass 

        return  
    
    
if __name__ == '__main__':
    from qdls.kopl.kopl import KoPLEngine
    import pickle
    def load_or_create_engine(kb_path: str, pickle_path: str) -> KoPLEngine:
        """Load KB from pickle if exists, otherwise create and save"""
        if os.path.exists(pickle_path):
            with open(pickle_path, "rb") as f:
                engine = pickle.load(f)
            logger.info(f"Loaded KB from pickle file")
        else:
            engine = KoPLEngine(load_json(kb_path))
            with open(pickle_path, "wb") as f:
                pickle.dump(engine, f)
            logger.info(f"Saved KB to pickle file")
        return engine
    
    KB_PATH = "/home/qing/raid/paperwork/kgtool/data/kqa/kb_fixed.json"
    PICKLE_PATH = "/home/qing/raid/paperwork/kgtool/data/kqa/kb_fixed.pkl"
    
    engine = load_or_create_engine(KB_PATH, PICKLE_PATH)

    tools = KoPLTools(engine)
    client = None
    model = "gpt-4o-mini"
    agent = QueryAgent(client, tools.tools, model)
    # agent._execute_tool("FindAll", {})
    agent._execute_tool("FilterConcept", {'entities': {'ids': ['Q113029', '5037043580'], 'triples': None}, 'concept_name': 'County'})