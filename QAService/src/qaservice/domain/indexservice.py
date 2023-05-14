from typing import List, Tuple, Callable

import numpy as np
import pandas as pd
import faiss
import numpy as np


class EmbeddingIndex:

    def __init__(self, embeddings, labels):
        embedding_documents = np.stack(embeddings.values)
        # FAISS only accepts np.float32 precision floats
        embedding_documents = embedding_documents.astype(np.float32)
        labels = labels.values

        # embedding dimension from laser is 1024, but use is 512, therefore extract
        n, d = embedding_documents.shape

        # build an index, in this case Exact search for L2 (exhaustive)
        index = faiss.IndexFlatL2(d)

        # add our embeddings to the index
        index.add(embedding_documents)
        self.index = index
        self.labels = labels

    def find_closest(self, embedding, k=10):
        if len(embedding.shape) < 2:
            embedding = np.expand_dims(embedding, axis=0)
        # returns the distances, and the Index values
        D, I_return = self.index.search(embedding, k)

        # convert the matrix of index values to a matrix of eps
        dists = D[0]
        inds = I_return[0]

        valid_ind = np.where(inds != -1)
        valid_dists = dists[valid_ind]
        I_ep = self.labels[valid_ind]

        return valid_dists, I_ep


class SearchIndexLocator:
    def __init__(self, index_loader: Callable[..., pd.DataFrame], embedding_column: str, partition: List[str], labels_columns: List[str]):
        self.index_loader = index_loader
        self.embedding_column = embedding_column
        self.partition = partition
        self.labels_columns = labels_columns
        self.index = self._build_search_indices()

    def _build_search_indices(self):
        df = self.index_loader()
        partition = self.partition[0] if len(self.partition) == 1 else list(self.partition)
        ind_map = {
            part_key: EmbeddingIndex(
                data[self.embedding_column],
                data[self.labels_columns]
            ) for part_key, data in df.groupby(partition)}

        return ind_map

    def __getitem__(self, partition):
        if isinstance(partition, int):
            part_key = partition
        elif len(partition) > 1:
            part_key = tuple(partition)
        else:
            part_key = partition[0]

        index = self.index[part_key]
        return index

