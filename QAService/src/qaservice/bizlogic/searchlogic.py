import pandas as pd
from qaservice.domain import TranslatorService, SearchIndexLocator
from qaservice.common import Query, SearchResult
from qaservice.common import clean
from qaservice.domain.embedding_service import LocalEmbeddingService, RemoteEmbeddingService, ServiceType
import os


class SearchLogic:
    SBERT_MODEL_NAME = "diptanuc/all-mpnet-base-v2"
    CACHE_DIRECTORY = "../Models/sentence_transformers"

    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        service_type = os.getenv("RUNTIME_ENVIRONMENT", "local")
        embedding_url = os.getenv("EMBEDDING_URL", "http://localhost:8080/")

        match service_type:
            case ServiceType.TYPE_LOCAL:
                self.embedding_service = LocalEmbeddingService()
            case ServiceType.TYPE_REMOTE:
                self.embedding_service = RemoteEmbeddingService(service_url=embedding_url)

        self.translator_service = TranslatorService()
        self.locator = SearchIndexLocator(
            index_loader=self._load_index,
            embedding_column="answer_embedding",
            partition=["partition_id"],
            labels_columns=["partition_id", "row_id"]
        )

    def _load_index(self) -> pd.DataFrame:
        return self.dataset

    def _build_response(self, matches) -> SearchResult:
        keys = matches[1]
        row_ids = keys[:, 1]
        answers = self.dataset.iloc[row_ids]
        answers["similarity"] = matches[0]
        answers = answers.reset_index(inplace=False)
        answers = answers.rename(columns={"index": "row_id"})
        answers = answers.rename(columns={"Answer": "answer_tx"})
        answers = answers[["row_id", "partition_id", "similarity", "answer_tx"]]
        result = SearchResult(answers=answers.to_dict("records"))
        return result

    def find(self, query: Query) -> SearchResult:
        partition_id = query.partition_id
        query_str = clean(query.query)
        max_results = query.max_results

        emb = self.embedding_service.embed(query_str)
        trans_emb = self.translator_service.translate(emb)

        index_service = self.locator[partition_id]
        answers = index_service.find_closest(trans_emb, k=max_results)

        results = self._build_response(answers)
        return results
