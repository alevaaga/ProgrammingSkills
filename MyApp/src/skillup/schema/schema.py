from typing import List
from pydantic import BaseModel


class Query(BaseModel):
    partition_id: int
    query: str
    max_results: int


class AnswerInfo(BaseModel):
    row_id: int
    partition_id: int
    similarity: float
    answer_tx: str


class SearchResult(BaseModel):
    answers: List[AnswerInfo]
