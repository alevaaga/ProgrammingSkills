from typing import List
from pydantic import BaseModel


class EPQuery(BaseModel):
    prg_typ_id: int
    query: str
    max_results: int


class EPInfo(BaseModel):
    ep_tx_id: int
    prg_typ_id: int
    ep_tx: str


class EPSearchResult(BaseModel):
    eps: List[EPInfo]
