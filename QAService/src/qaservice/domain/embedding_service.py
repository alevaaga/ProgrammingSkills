import numpy as np
import os

from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name, cache_dir="../Models/sentence_transformers"):
        pass

    def embed(self, text: str) -> np.ndarray:
        pass
