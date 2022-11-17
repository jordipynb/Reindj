from ..framework import Framework
from . import Qrydb
from .qryindexer import QryIndexer
from .qryparser import QryParser
from config import Configuration

class Query:
    def __init__(self, framework:Framework):
        self.__framework__ = framework
        self.__terms__ = self.__framework__.terms
        self.__idf__ = self.__framework__.__idf__
        self.__typedb__ = self.__framework__.__typedb__
        self.__typeqry__ = Qrydb.search_qry_type(self.__typedb__)
        self.__typemodel__ = self.__framework__.__typemodel__
        self.__path__ = Configuration().qry_path(self.__typedb__)

    def __get_queries__(self) -> list[Qrydb]:
        if not self.__path__.exists() or not self.__path__.is_file(): raise Exception("Queries Path is not exist")
        queries = ""
        with open(self.__path__, "r", encoding='utf8') as queriespath: queries = queriespath.read()
        return QryParser.search_qry_parser_type(self.__typedb__)(queries)

    def __call__(self, text:str) -> tuple[Qrydb, list[float]]:
        qry:Qrydb = self.__typeqry__(0,text)
        return QryIndexer.search_qry_indexer_type(self.__typemodel__)(qry,self.__terms__,self.__idf__)