from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer
import numpy as np
from skillup.bizlogic.searchlogic import EPSearchLogic
from skillup.schema import SearchResult, Query
import os

from skillup.service.embeddingindex import EmbeddingIndex
from skillup.service.translator import nn_mlp_512_x_n_translator_prg1, nn_mlp_512_x_n_translator_prg2
from skillup.service.utils import clean
import pandas as pd


DATAFRAME_PATH = "../DevAssets/preprocessed.parquet"

# This is a long and annoying comment that tells you that
# the property below is the name of the sentence encoder
# model that is used for embedding
# If you name the property properly, you don't have
# to document it!
SBERT_MODEL_NAME = "diptanuc/all-mpnet-base-v2"

# ***** Cache Directory ******
# This directory will be used to cache models
CACHE_DIRECTORY = "../Models/sentence_transformers"

# Create the Models directory. It's ok if it already exists
os.makedirs(CACHE_DIRECTORY, exist_ok=True)

# Load the embedding model
embedding_model = SentenceTransformer(cache_folder=CACHE_DIRECTORY, model_name_or_path=SBERT_MODEL_NAME)

try:
    DF_DATAFRAME = pd.read_parquet(DATAFRAME_PATH)
except Exception as e:
    print(f"That didn't work: {e}")


def load_index(partition_id):
    df = DF_DATAFRAME.reset_index(inplace=False)
    df = df.rename(columns={"index": "row_id"})
    part_data = df.loc[df["partition_id"] == partition_id]
    embedding_index = EmbeddingIndex(
        part_data["answer_embedding"],
        part_data[["partition_id", "row_id"]]
    )
    return embedding_index


EMBEDDING_INDEX_FOR_PROGRAM_1 = load_index(partition_id=1)

EMBEDDING_INDEX_FOR_PROGRAM_2 = load_index(partition_id=2)

# Create the FastAPI app
app = FastAPI()


def get_embedding(txt: str) -> np.ndarray:
    '''
    Embed the provided text
    :param txt: The text to embed
    :return: The embedding
    '''
    sanitized_text = clean(txt)
    embedding = embedding_model.encode([sanitized_text])[0]
    return embedding


def get_nn_translated_embedding(
        embedding_to_translate: List[float],
        prg_typ_id: int
) -> List[float]:
    """Submit a 'raw' embedding vector to the NN translation model, and return result

    Note: We are currently using HTTP REST. Using gRPC can significantly
    decrease the latency of the model call.

    Parameters
    ----------
    input_embedding: List[float]
        Embedding vector (from basic embedding service)

    prg_typ_id: int
        The program id

    Returns
    -------
    List[float]
        The "translated" embedding vector

    Raises
    ------
    HTTPException
        Basic validation of the embedding vector
    """
    if 1 == prg_typ_id:
        translated_embedding = nn_mlp_512_x_n_translator_prg1(embedding_to_translate)
    elif 2 == prg_typ_id:
        translated_embedding = nn_mlp_512_x_n_translator_prg2(embedding_to_translate)
    else:
        raise HTTPException(status_code=500, detail=f"Unknown program id {prg_typ_id}")

    if translated_embedding is None:
        raise HTTPException(status_code=500, detail=f"Something went wrong")

    return translated_embedding


def find_the_answers_that_closest_answers_the_query(query_embedding: List[float], partition_id: int, k: int) -> List:
    '''
    Find the answer to the question
    :param query_embedding: query embedding
    :param partition_id: partition id
    :param k: number of resutls to return
    :return: results
    '''
    if 1 == partition_id:
        matches = EMBEDDING_INDEX_FOR_PROGRAM_1.find_closest(np.asarray(query_embedding), k)
    elif 2 == partition_id:
        matches = EMBEDDING_INDEX_FOR_PROGRAM_2.find_closest(np.asarray(query_embedding), k)
    else:
        raise Exception(f"Partition {partition_id} is invalid")

    result = matches[0:k]
    return result


@app.post(path="/find_ep", response_model=SearchResult)
def find_ep(query: Query) -> SearchResult:
    embedding = get_embedding(query.query)
    translated_embedding = get_nn_translated_embedding(embedding.tolist(), query.partition_id)
    matches =find_the_answers_that_closest_answers_the_query(
        translated_embedding,
        partition_id=query.partition_id,
        k=query.max_results
    )

    keys = matches[1]
    row_ids = keys[:, 1]
    answers = DF_DATAFRAME.iloc[row_ids]
    answers["similarity"] = matches[0]
    answers = answers.reset_index(inplace=False)
    answers = answers.rename(columns={"index": "row_id"})
    answers = answers.rename(columns={"Answer": "answer_tx"})
    answers = answers[["row_id", "partition_id", "similarity", "answer_tx"]]

    result = SearchResult(answers=answers.to_dict("records"))
    return result




# @app.post(path="/find_ep", response_model=EPSearchResult)
# def find_ep(query: EPQuery) -> EPSearchResult:
#     searchlogic = EPSearchLogic()
#     result_list = searchlogic.find(query)
#     result = EPSearchResult(eps=result_list)
#     return result
#

if __name__ == '__main__':
    uvicorn.run("skillup.service.skillup_app:app", host="0.0.0.0", port=8080, reload=True)
