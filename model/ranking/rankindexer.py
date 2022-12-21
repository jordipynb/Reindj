from abc import ABC, abstractmethod
from model.framework import Document
from model.framework.corpus import Corpus
from heapq import nlargest
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RankIndexer(ABC):
    __type__ = "default"

    @abstractmethod
    def __call__(self, top: int, umbral: float, w_docterms: np.ndarray, w_queryterms: list[float], corpus: Corpus) -> \
            list[Document]:
        pass

    @classmethod
    def search_rank_indexer_type(self, _type: str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Rank Indexer Type")
        return cls[_type]()


class VectorRankIndexer(RankIndexer):
    __type__ = "vector"

    def __call__(self, top: int, umbral: float, w_docterms: np.ndarray, w_queryterms: list[float], corpus: Corpus) -> \
            list[Document]:
        cos = cosine_similarity(w_docterms, w_queryterms.reshape(1, -1))
        doc_sim = []
        for i in range(len(corpus)):
            doc = corpus[i]
            sim = cos[i]
            doc_sim.append((doc, sim))
        top_sim = nlargest(top, doc_sim, key=lambda docsim: docsim[1])
        top_umbral = list(filter(lambda topsim: topsim[1] > umbral, top_sim))
        if len(top_umbral) == 0: top_umbral.append(top_sim[0])
        top_umbral = list(map(lambda topumbral: topumbral[0], top_umbral))
        return top_umbral


class Latent_Semantic_Rank_Indexer(RankIndexer):
    __type__ = "latent_semantic"

    def __call__(self, top: int, umbral: float, w_docterms: np.ndarray, w_queryterms: list[float], corpus: Corpus) ->\
            list[Document]:
        cos = cosine_similarity(w_docterms, w_queryterms.reshape(1, -1))
        doc_sim = []
        for i in range(len(corpus)):
            doc = corpus[i]
            sim = cos[i]
            doc_sim.append((doc, sim))
        top_sim = nlargest(top, doc_sim, key=lambda docsim: docsim[1])
        top_umbral = list(filter(lambda topsim: topsim[1] > umbral, top_sim))
        if len(top_umbral) == 0: top_umbral.append(top_sim[0])
        top_umbral = list(map(lambda topumbral: topumbral[0], top_umbral))
        return top_umbral


class BooleanRankIndexer(RankIndexer):
    __type__ = "boolean"

    def __call__(self, top: int, umbral: float, w_docterms: np.ndarray, w_queryterms: list[float], corpus: Corpus) -> \
            list[Document]:
        terms: list[np.ndarray] = []
        for q_term in w_queryterms:
            pos = w_docterms[q_term]
            if self.__is_equal__(pos, np.zeros(len(corpus), dtype=int)):
                return []
            if len(terms) <= top:
                terms.append(pos)

        return self.__verify_docs__(terms, corpus)

    def __verify_docs__(self, terms: list[np.ndarray], corpus: Corpus):
        docs: list[Document] = []
        for i in range(0, len(corpus)):
            for j, term in enumerate(terms):
                if term[i] == 0:
                    break
                if term[i] == 1 and j == len(terms) - 1:
                    docs.append(corpus.__getitem__(i))
        return docs

    def __is_equal__(self, array1: np.ndarray, array2: np.ndarray):
        if len(array1) != len(array2):
            return False
        for i in range(0, len(array1)):
            if array1[i] != array2[i]:
                return False
        return True
