import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np


def main():
    df = pd.read_csv("../DevAssets/questioning.csv", delimiter=",")
    embedding_model = SentenceTransformer(cache_folder="../Models/sentence_transformers", model_name_or_path="diptanuc/all-mpnet-base-v2")

    df["partition_id"] = df.apply(lambda ans: 1 if np.random.rand() < 0.5 else 2, axis=1)
    df["answer_embedding"] = df.apply(lambda ans: embedding_model.encode([ans["Answer"]])[0], axis=1)

    df.to_parquet("../DevAssets/preprocessed.parquet")


if __name__ == '__main__':
    main()