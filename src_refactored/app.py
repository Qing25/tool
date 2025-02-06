"""Main application entry point."""
from pathlib import Path
import hydra
from omegaconf import DictConfig
from loguru import logger

from src_refactored.core.agent import QueryAgent
from src_refactored.core.kb_engine import KBEngine
from src_refactored.core.tools import KoPLTools
from src_refactored.utils.config import setup_environment

@hydra.main(config_path="config", config_name="default")
def main(cfg: DictConfig) -> None:
    """Main application entry point.
    
    Args:
        cfg: Hydra configuration object
    """
    # Setup environment
    setup_environment(cfg)
    
    # Initialize knowledge base engine
    kb_engine = KBEngine(
        kb_path=cfg.knowledge_base.kb_path,
        pickle_path=cfg.knowledge_base.pickle_path
    )
    
    # Create tools
    tools = KoPLTools(kb_engine.engine).tools
    
    # Initialize agent
    agent = QueryAgent(
        tools=tools,
        model_name=cfg.model.name,
        api_config=cfg.model.api,
        vq_config=cfg.vq_model if cfg.vq_model.enabled else None
    )
    
    # Example query
    query = "Is there less area in DeKalb County or Boulder County?"
    history, response = agent.execute_query(query)
    
    logger.info(f"Query: {query}")
    logger.info(f"Response: {response}")

if __name__ == "__main__":
    main() 