from abc import ABC, abstractmethod
from enum import Enum

import numpy as np
import os
from sentence_transformers import SentenceTransformer
from qaservice.common.schemas import TextInput, Embedding
import requests


class ServiceType(Enum):
    TYPE_REMOTE = "remote"
    TYPE_LOCAL = "local"


class EmbeddingService(ABC):
    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        pass


class LocalEmbeddingService(EmbeddingService):

    def __init__(self, model_name=None, cache_dir="../Models/sentence_transformers", **kwargs):
        os.makedirs(cache_dir, exist_ok=True)
        self.embedding_model = SentenceTransformer(cache_folder=cache_dir, model_name_or_path=model_name)

    def embed(self, text: str) -> np.ndarray:
        embedding = self.embedding_model.encode([text])[0]
        return embedding


class RemoteEmbeddingService(EmbeddingService):

    def __init__(self, service_url: str = None, **kwargs):
        if service_url is None:
            raise ValueError(f"You have not provided a valid service_url: {service_url}")
        self.service_url = service_url

    def embed(self, text: str) -> np.ndarray:
        query = TextInput(text=text)
        response = requests.post(url=self.service_url, data=query.json())
        data = response.json()
        embedding = Embedding(**data)
        return np.asarray(embedding.embedding)
