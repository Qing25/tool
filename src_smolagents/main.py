

# -*- coding: utf-8 -*-
# @File    :   main.py
# @Time    :   2025/02/13 16:01:08
# @Author  :   Qing 
# @Email   :   aqsz2526@outlook.com
######################### docstring ########################
'''
    使用 smolagents 框架
'''

import os,sys 

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FILE_DIR)
print(FILE_DIR)
print(PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)



import pickle
from qdls.data import save_json,load_json
from qdls.utils import print_string
from loguru import logger   
from src_smolagents.tools import tools 
from src_smolagents.cached_agent import CachedToolCallingAgent

from smolagents.agents import CodeAgent, MultiStepAgent
from smolagents.models import LiteLLMModel, OpenAIServerModel

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
def set_opentelementary():

    endpoint = "http://0.0.0.0:6006/v1/traces"
    trace_provider = TracerProvider()
    trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

    SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)

set_opentelementary()


glm4_plus_model = OpenAIServerModel(
        model_id="glm-4-plus", # This model is a bit weak for agentic behaviours though
        api_base="https://open.bigmodel.cn/api/paas/v4" , 
        api_key=os.environ["ZHIPU_API_KEY"] , 
        max_tokens=8192
    )
 
qwen_model = OpenAIServerModel(
        model_id="qwen-plus", # This model is a bit weak for agentic behaviours though
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1" , 
        api_key=os.environ["QWEN_API_KEY"] , 
        max_tokens=8192
    )

gpt_model = LiteLLMModel(
    model_id="gpt-4o-mini", # This model is a bit weak for agentic behaviours though
    # model_id="gpt-4o", # This model is a bit weak for agentic behaviours though
    api_base=os.environ["CHATANY_API_URL"] , 
    api_key=os.environ["CHATANY_API_KEY"] , 
    num_ctx=8192 
)


def run_tool_calling_agent():
    agent = CachedToolCallingAgent(
        tools=tools,
        model=gpt_model,
        max_steps=15,
        # planning_interval=5
    )

    data = load_json("/home/qing/raid/paperwork/kgtool/data/kqa/sampled/sampled_50.json")
    for sample in data[1:]:
        question = sample["question"]
        answer = sample["answer"]
        print(question)
        print(answer) 
        # print(agent.system_prompt)
        # input()
        agent.run(question) 
        print_string(answer)
        break 


def run_code_agent():
    agent = CodeAgent(
        model=gpt_model,
        tools=tools,
    )
    question = "Tell me the one with the bigger population, Florence (which has an elevation (over sea level) of 42 metres) or Raleigh."
    kopl = "Find(Florence).FilterNum(elevation above sea level,42 metre,=).Find(Raleigh).Or().Select(population,largest,1,0).What()"
    answer = "Raleigh"
    # print(agent.system_prompt)
    agent.run(question)

def main():

    run_code_agent()





if __name__ == "__main__":
    main()