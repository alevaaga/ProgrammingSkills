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
