from ..framework import Framework, Document
from config import Configuration
from .rankindexer import RankIndexer

class Rank:
    def __init__(self, framework:Framework):
        self.top = Configuration().get_top()
        self.umbral = Configuration().get_umbral()
        self.__framework__= framework
        self.__typemodel__ = self.__framework__.__typemodel__
    
    def get_top_list(self, w_queryterms:list[float]) -> list[Document]:
        w_docterms = self.__framework__.__weight__
        corpus = self.__framework__.__corpus__
        return RankIndexer.search_rank_indexer_type(self.__typemodel__)(self.top,self.umbral,w_docterms,w_queryterms,corpus)