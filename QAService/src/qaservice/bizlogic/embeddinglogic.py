from qaservice.domain import EmbeddingService
from qaservice.common import TextInput, Embedding


class EmbeddingLogic:
    SBERT_MODEL_NAME = "diptanuc/all-mpnet-base-v2"
    CACHE_DIRECTORY = "../Models/sentence_transformers"
    instance = None

    def __init__(self):
        self.embedding_service = EmbeddingService(
            model_name=EmbeddingLogic.SBERT_MODEL_NAME,
            cache_dir=EmbeddingLogic.CACHE_DIRECTORY
        )

    def configure(self, model_name: str, cache_directory="../Models/sentence_transformers"):
        self.embedding_service = EmbeddingService(
            model_name=model_name,
            cache_dir=cache_directory
        )

    @staticmethod
    def get():
        if EmbeddingLogic.instance is None:
            EmbeddingLogic.instance = EmbeddingLogic()
        return EmbeddingLogic.instance

    def embed(self, query_str: TextInput):
        text = query_str.text
        emb = self.embedding_service.embed(text)
        result = Embedding(embedding=emb.tolist())
        return result
