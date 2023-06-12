import uvicorn
from fastapi import FastAPI
import pandas as pd
from qaservice.bizlogic import SearchLogic
from qaservice.common.schemas import Query, SearchResult
from qaservice.domain import EmbeddingServiceFactory, ServiceType
import os

# QASERVICE_STAGE should be one of: [local, dev, uat, prod]
QASERVICE_STAGE = os.getenv("QASERVICE_STAGE", "local")

SEARCH_INDEX_PATH = "../DevAssets/preprocessed.parquet"

# For local embedding service.
SBERT_MODEL_NAME = "diptanuc/all-mpnet-base-v2"
CACHE_DIRECTORY = "../Models/sentence_transformers"

# For remote embedding service.
EMBEDDING_SERVICE_URL = "http://localhost:8081/embed"

app = FastAPI()


@app.on_event("startup")
def initialize():
    global dataset

    dataset = pd.read_parquet(SEARCH_INDEX_PATH)
    dataset = dataset.reset_index(inplace=False)
    dataset = dataset.rename(columns={"index": "row_id"})

    if QASERVICE_STAGE == "local":
        EmbeddingServiceFactory.select_service(ServiceType.TYPE_LOCAL, model_name=SBERT_MODEL_NAME, cache_dir=CACHE_DIRECTORY)
    else:
        EmbeddingServiceFactory.select_service(ServiceType.TYPE_REMOTE, service_url=EMBEDDING_SERVICE_URL)


@app.post(path="/answer", response_model=SearchResult)
def find_answer(query: Query) -> SearchResult:
    search_logic = SearchLogic(dataset=dataset)
    results = search_logic.find(query)
    return results


if __name__ == '__main__':
    uvicorn.run("qaservice.service.skillup_app:app", host="0.0.0.0", port=8080, reload=True)
