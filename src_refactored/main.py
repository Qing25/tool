import os 
import sys 
os.environ["TOKENIZERS_PARALLELISM"] = "true"
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FILE_DIR)
print(FILE_DIR)
print(PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)

import random
random.seed(3407)
import fire
from omegaconf import OmegaConf, ValidationError
from qdls.utils import print_config, print_string

from loguru import logger

from src_refactored.core.agent import QueryAgent
from src_refactored.core.tools import KoPLTools
from src_refactored.core.kb_engine import KBEngine



def main(config=None, version='default_version', **kwargs):
    if config is None:
        raise Exception(f"must specify a configuration file to start!")
    
    config = OmegaConf.load(config)
    config.version = version 
    
    cli_str = [ f"{k}={v}" for k,v in kwargs.items() ]
    config = OmegaConf.unsafe_merge(config, OmegaConf.from_cli(cli_str))
    print_config(config)
    
    kb_engine = KBEngine(
        kb_path=config.knowledge_base.kb_path,
        pickle_path=config.knowledge_base.pickle_path
    )
    
    # Create tools
    tools = KoPLTools(kb_engine.engine).tools
    
    # Initialize agent
    agent = QueryAgent(
        tools=tools,
        model_name=config.model.name,
        api_config=config.model.api,
        vq_config=config.vq_model if config.vq_model.enabled else None
    )
    
    # Example query
    query = "Is there less area in DeKalb County or Boulder County?"
    history, response = agent.execute_query(query)
    
    logger.info(f"Query: {query}")
    logger.info(f"Response: {response}")


if __name__ == '__main__':
    
    fire.Fire(main)