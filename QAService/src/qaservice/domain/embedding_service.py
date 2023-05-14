import numpy as np
import os

from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name, cache_dir="../Models/sentence_transformers"):
        os.makedirs(cache_dir, exist_ok=True)
        self.embedding_model = SentenceTransformer(cache_folder=cache_dir, model_name_or_path=model_name)

    def embed(self, text: str) -> np.ndarray:
        embedding = self.embedding_model.encode([text])[0]
        return embedding
