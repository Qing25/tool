"""Configuration utilities."""
import os
from typing import Optional
from omegaconf import DictConfig
from loguru import logger

def setup_environment(cfg: DictConfig) -> None:
    """Setup environment variables and logging.
    
    Args:
        cfg: Configuration object
    """
    # Setup logging
    logger.remove()
    logger.add(
        lambda msg: print(msg),
        format=cfg.logging.format,
        level=cfg.logging.level
    )
    
    # Verify API key exists
    api_key = os.environ.get(cfg.model.api.api_key_env)
    if not api_key:
        raise ValueError(f"Missing API key in environment: {cfg.model.api.api_key_env}") 