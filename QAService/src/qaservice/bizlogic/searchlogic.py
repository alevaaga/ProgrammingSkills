import pandas as pd
from qaservice.domain import EmbeddingService, TranslatorService, SearchIndexLocator
from qaservice.common.schema import Query
from skillup.search.schema import SearchResult


class SearchLogic:
    SBERT_MODEL_NAME = "diptanuc/all-mpnet-base-v2"
    CACHE_DIRECTORY = "../Models/sentence_transformers"

    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.embedding_service = EmbeddingService(
            model_name=SearchLogic.SBERT_MODEL_NAME,
            cache_dir=SearchLogic.CACHE_DIRECTORY
        )
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
        return results
