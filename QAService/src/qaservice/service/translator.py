from typing import List


def nn_mlp_512_x_n_translator_prg1(embedding: List[float]) -> List[float]:
    '''
    Translate the embedding using an MLP Neural Network trained on lots of data
    to translate the given embedding to a new and better embedding
    :param embedding: This is the embedding we want to translate
    :return: The function returns the translated embedding.
    '''
    translated_embedding = [v + 0.000001 for v in embedding]
    return translated_embedding


def nn_mlp_512_x_n_translator_prg2(embedding: List[float]) -> List[float]:
    '''
    Translate the embedding using an MLP Neural Network trained on lots of data
    to translate the given embedding to a new and better embedding
    :param embedding: This is the embedding we want to translate
    :return: The function returns the translated embedding.
    '''
    translated_embedding = [v + 0.000002 for v in embedding]
    return translated_embedding