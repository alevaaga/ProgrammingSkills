import numpy as np


class TranslatorService:

    def translate(self, embedding: np.ndarray) -> np.ndarray:
        translated_emb = embedding * np.sqrt(2)
        return translated_emb

