from typing import List
import numpy as np
from .data import EP


class IndexService:

    def find_similar(self, embedding: np.ndarray, prg_typ_id: int, k: int) -> List[EP]:
        eps = []
        for i in range(np.random.randint(k)):
            moc_ep = EP()
            moc_ep.ep_tx = "blah"
            moc_ep.std_tx = "For bla"
            moc_ep.ep_tx_id = np.random.randint(42, 42*42, 1)
            moc_ep.prg_typ_id = prg_typ_id
            eps.append(moc_ep)
        return eps
