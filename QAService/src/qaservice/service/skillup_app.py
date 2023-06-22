import uvicorn
from fastapi import FastAPI
import pandas as pd
from qaservice.bizlogic import SearchLogic
from qaservice.common import Query, SearchResult
from qaservice.service.searchindex import SearchIndex

SEARCH_INDEX_PATH = "../DevAssets/preprocessed.parquet"

app = FastAPI()


@app.on_event("startup")
def initialize():
    dataset = pd.read_parquet(SEARCH_INDEX_PATH)
    dataset = dataset.reset_index(inplace=False)
    dataset = dataset.rename(columns={"index": "row_id"})
    SearchIndex.get().configure(dataset)


@app.post(path="/answer", response_model=SearchResult)
def find_answer(query: Query) -> SearchResult:
    search_logic = SearchLogic(dataset=SearchIndex.get().dataset)
    results = search_logic.find(query)
    return results


if __name__ == '__main__':
    uvicorn.run("qaservice.service.skillup_app:app", host="0.0.0.0", port=8080, reload=True)
