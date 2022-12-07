from abc import ABC, abstractmethod
from model.framework import Document
from model.framework.corpus import Corpus
from heapq import  nlargest
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RankIndexer(ABC):
    __type__ = "default"
    
    @abstractmethod
    def __call__(self,top:int,umbral:float,w_docterms:np.ndarray,w_queryterms:list[float],corpus:Corpus) -> list[Document]:pass

    @classmethod
    def search_rank_indexer_type(self, _type:str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Rank Indexer Type")
        return cls[_type]()

class VectorRankIndexer(RankIndexer):
    __type__ = "vector"
    
    def __call__(self,top:int,umbral:float,w_docterms:np.ndarray,w_queryterms:list[float],corpus:Corpus) -> list[Document]:
        cos = cosine_similarity(w_docterms, w_queryterms.reshape(1, -1))
        doc_sim = []
        for i in range(len(corpus)):
            doc = corpus[i]
            sim = cos[i]
            doc_sim.append((doc, sim))
        top_sim = nlargest(top, doc_sim, key=lambda docsim:docsim[1])
        top_umbral = list(filter(lambda topsim:topsim[1]>umbral,top_sim))
        if len(top_umbral) == 0: top_umbral.append(top_sim[0])
        top_umbral = list(map(lambda topumbral:topumbral[0],top_umbral))
        return top_umbral

    
class Latent_Semantic_Rank_Indexer(RankIndexer):
    __type__="latent_semantic"
    def __call__(self,top:int,umbral:float,w_docterms:np.ndarray,w_queryterms:list[float],corpus:Corpus) -> list[Document]:
        cos = cosine_similarity(w_docterms, w_queryterms.reshape(1, -1))
        doc_sim = []
        for i in range(len(corpus)):
            doc = corpus[i]
            sim = cos[i]
            doc_sim.append((doc, sim))
        top_sim = nlargest(top, doc_sim, key=lambda docsim:docsim[1])
        top_umbral = list(filter(lambda topsim:topsim[1]>umbral,top_sim))
        if len(top_umbral) == 0: top_umbral.append(top_sim[0])
        top_umbral = list(map(lambda topumbral:topumbral[0],top_umbral))
        return top_umbral