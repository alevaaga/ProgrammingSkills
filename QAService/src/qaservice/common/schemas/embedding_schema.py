from typing import List
from pydantic import BaseModel


class TextInput(BaseModel):
    text: str


class Embedding(BaseModel):
    embedding: List[float]

