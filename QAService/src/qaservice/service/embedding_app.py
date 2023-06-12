import uvicorn
from fastapi import FastAPI
from qaservice.bizlogic import EmbeddingLogic
from qaservice.common.schemas import Embedding, TextInput
from qaservice.domain import EmbeddingServiceFactory, ServiceType

SBERT_MODEL_NAME = "diptanuc/all-mpnet-base-v2"
CACHE_DIRECTORY = "../Models/sentence_transformers"
app = FastAPI()


@app.on_event("startup")
def initialize():
    EmbeddingServiceFactory.select_service(
        ServiceType.TYPE_LOCAL,
        model_name=SBERT_MODEL_NAME,
        cache_directory=CACHE_DIRECTORY
    )


@app.post(path="/embed", response_model=Embedding)
def find_answer(query: TextInput) -> Embedding:
    embedding_service = EmbeddingLogic.get()
    results = embedding_service.embed(query)
    return results


if __name__ == '__main__':
    uvicorn.run("qaservice.service.embedding_app:app", host="0.0.0.0", port=8081, reload=True)
