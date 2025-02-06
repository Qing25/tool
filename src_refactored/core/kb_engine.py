"""Knowledge base engine module."""
from pathlib import Path
import pickle
from typing import Optional
from loguru import logger
from qdls.kopl.kopl import KoPLEngine
from qdls.data import load_json

class KBEngine:
    """Knowledge base engine wrapper."""
    
    def __init__(self, kb_path: str, pickle_path: str):
        """Initialize KB engine.
        
        Args:
            kb_path: Path to knowledge base JSON file
            pickle_path: Path to pickle cache file
        """
        self.kb_path = Path(kb_path)
        self.pickle_path = Path(pickle_path)
        self.engine = self._load_or_create_engine()
        
    def _load_or_create_engine(self) -> KoPLEngine:
        """Load KB from pickle if exists, otherwise create and save."""
        if self.pickle_path.exists():
            with open(self.pickle_path, "rb") as f:
                engine = pickle.load(f)
            logger.info("Loaded KB from pickle file")
        else:
            engine = KoPLEngine(load_json(self.kb_path))
            with open(self.pickle_path, "wb") as f:
                pickle.dump(engine, f)
            logger.info("Saved KB to pickle file")
        return engine 