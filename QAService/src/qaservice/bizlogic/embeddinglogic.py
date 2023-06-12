from qaservice.domain import EmbeddingServiceFactory
from qaservice.common import TextInput, Embedding


class EmbeddingLogic:
    instance = None

    def __init__(self):
        self.embedding_service = EmbeddingServiceFactory.get()

    @staticmethod
    def get():
        if EmbeddingLogic.instance is None:
            EmbeddingLogic.instance = EmbeddingLogic()
        return EmbeddingLogic.instance

    def embed(self, query_str: TextInput) -> Embedding:
        text = query_str.text
        emb = self.embedding_service.embed(text)
        result = Embedding(embedding=emb.tolist())
        return result
