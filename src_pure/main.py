import os
import pickle
from loguru import logger
from qdls.kopl.kopl import KoPLEngine
from qdls.data import load_json, save_json
from qdls.utils import print_string
from tqdm import tqdm

import openai

# from kopl_tools import KoPLTools
from autogen_tools import KoPLTools
from query_agent import QueryAgent

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


def extract_relation_entities(program: str):
    # Extract entities from program
    R = [] # relations
    for step in program:
        inputs = step['inputs']
        R.extend(inputs)
    return  [x for x in R if type(x) == str]



def main():
    # Initialize KoPL engine
    KB_PATH = "/home/qing/raid/paperwork/kgtool/data/kqa/kb.json"
    PICKLE_PATH = "/home/qing/raid/paperwork/kgtool/data/kqa/kb.pkl"
    
    engine = load_or_create_engine(KB_PATH, PICKLE_PATH)
    logger.info(f"Engine initialized: {engine}")
    
    # Create tools and agent
    tools = KoPLTools(engine).tools
    client = openai.OpenAI(
        api_key=os.environ.get('CHATANY_API_KEY'),
        base_url="https://api.chatanywhere.tech/v1",
    )
    model = "gpt-4o-mini"
    # model = "gpt-4o"
    agent = QueryAgent(
        client=client,
        tools=tools,
        model=model
    )
    
    # Test query
    # query = "Is there less area in DeKalb County (the one whose PermID is 5037043580) or Boulder County?"
    # query = "How many bowed string instruments do we know Hornbostel-Sachs classification is 321.322-71 or that are the instrument used by John Hartford?"
    # history, response = agent.execute_query(query)
    
    # logger.info(f"Query: {query}")
    # logger.info(f"Response: {response}")

    data = load_json("/home/qing/raid/paperwork/kgtool/data/kqa/sampled/sampled_50.json")
    cnt = 0 
    for sample in tqdm(data):
        query = sample["question"]
        linked_prompt = f"Related relations and entities are {extract_relation_entities(sample['program'])}"
        history, response = agent.execute_query(query + f"\n{linked_prompt}")
        logger.info(f"Query: {query}")
        logger.info(f"Response: {response}")
        sample["history"] = history
        sample["response"] = response
        print_string(f'{history[-1]["final_answer"]} || {sample["answer"]}')
        if history[-1]["final_answer"] == sample["answer"]:
            cnt += 1
    logger.info(f"Accuracy: {cnt/len(data)}")
    save_json(data, f"./results/sampled_50_{model}_v1_linked_prompt.json")



if __name__ == "__main__":
    main()


