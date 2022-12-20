from config import Configuration
from . import Document
from .corpus import Corpus
from .indexer import Indexer
from .parser import Parser


class Framework:
    def __init__(self, typedb: str, typemodel: str):
        self.__typedb__ = typedb
        self.__path__ = Configuration().db_path(self.__typedb__)
        self.__typemodel__ = typemodel
        doc = self.__documents__()
        self.__corpus__ = Corpus(doc)
        self.__weight__, self.__idf__, self.terms, self.__T__ = Indexer.search_indexer_type(self.__typemodel__)(
            self.__corpus__.bodies)

    def __documents__(self) -> list[Document]:
        if not self.__path__.exists() or not self.__path__.is_file(): raise Exception("Corpus Path does not exist")
        collection = ""
        with open(self.__path__, "r", encoding='utf8') as collpath:
            collection = collpath.read()
        return Parser.search_parser_type(self.__typedb__)(collection)
