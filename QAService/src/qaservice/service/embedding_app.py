import uvicorn
from fastapi import FastAPI
from qaservice.bizlogic import EmbeddingLogic
from qaservice.common import TextInput, Embedding

SBERT_MODEL_NAME = "diptanuc/all-mpnet-base-v2"
CACHE_DIRECTORY = "../Models/sentence_transformers"

app = FastAPI()


def initialize():
    embedding_service = EmbeddingLogic.get()
    embedding_service.configure()


@app.post(path="/embed", response_model=Embedding)
def find_answer(query: TextInput) -> Embedding:
    embedding_service = EmbeddingLogic.get()
    results = embedding_service.embed(query)
    return results


if __name__ == '__main__':
    uvicorn.run("qaservice.service.embedding_app:app", host="0.0.0.0", port=8081, reload=True)
