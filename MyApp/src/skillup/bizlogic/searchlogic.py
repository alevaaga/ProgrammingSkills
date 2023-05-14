from typing import List

from skillup.schema import Query, AnswerInfo
from skillup.domain import IndexService, TranslatorService, EmbeddingService


class EPSearchLogic:
    def find(self, query: Query) -> List[AnswerInfo]:
        embedding_service = EmbeddingService()
        translator_service = TranslatorService()
        index_service = IndexService()

        query_str = query.query
        prg_type_id = query.partition_id
        emb = embedding_service.embed(query_str)
        trans_emb = translator_service.translate(emb)
        eps = index_service.find_similar(trans_emb, prg_type_id, k=query.max_results)

        results = []
        for ep in eps:
            ep_info = AnswerInfo(prg_typ_id=ep.prg_typ_id, ep_tx_id=ep.ep_tx_id, ep_tx=ep.ep_tx)
            results.append(ep_info)

        return results

