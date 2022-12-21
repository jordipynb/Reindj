import re
import json
from config import Configuration
from typing import Generator
from . import Document
from abc import ABC, abstractmethod


class Parser(ABC):
    __type__ = "default"

    @abstractmethod
    def __call__(self, text: str) -> list[Document]:
        pass

    @classmethod
    def search_parser_type(self, _type: str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Parser Type")
        return cls[_type]()


class CranfieldParser(Parser):
    __type__ = "cranfield"

    def __init__(self):
        self.__typedoc__: type[Document] = Document.search_document_type(CranfieldParser.__type__)
        self.__match_Title__ = re.compile('\.T')
        self.__match_Author__ = re.compile('\.A')
        self.__match_Editorial__ = re.compile('\.B')
        self.__match_Text__ = re.compile('\.W')

    def __call__(self, text: str) -> list[Document]:
        tuple_docs = self.__tokenize_docs__(text)
        list_docs: list[Document] = []
        for i, docs in enumerate(tuple_docs): list_docs.append(
            self.__typedoc__(str(i + 1), docs[0], docs[1], docs[2], docs[3]))
        return list_docs

    def __tokenize_docs__(self, text: str) -> Generator[tuple[str, str, str, str], None, None]:
        docs_splitted = re.split(f"\.I [0-9]*", text)
        docs_splitted.pop(0)
        for doc in docs_splitted:
            doc = re.split(self.__match_Title__, doc)[1]
            title, doc = re.split(self.__match_Author__, doc, 1)
            title = title.replace("\n", " ")[1:-1]
            author, doc = re.split(self.__match_Editorial__, doc, 1)
            author = author.replace("\n", " ")[1:-1]
            editorial, textdoc = re.split(self.__match_Text__, doc, 1)
            editorial = editorial.replace("\n", " ")[1:-1]
            textdoc = textdoc.replace("\n", " ")
            yield title, textdoc, author, editorial


class TrecCovidParser(Parser):
    __type__ = "trec-covid"

    def __init__(self):
        self.__typedoc__: type[Document] = Document.search_document_type(TrecCovidParser.__type__)

    def __call__(self, text: str) -> list[Document]:
        list_docs: list[Document] = []
        # db_path = Configuration.db_path(Configuration, _type="trec-covid")
        db_path = 'db/trec-covid/corpus.jsonl'

        with open(db_path, 'r') as json_file:
            json_list = list(json_file)

        for json_lines in json_list:
            doc = json.loads(json_lines)
            list_docs.append(self.__typedoc__(doc['_id'], doc['title'], doc['text'], doc['metadata']))
        return list_docs


class VaswaniParser(Parser):
    __type__ = "vaswani"

    def __init__(self):
        self.__typedoc__: type[Document] = Document.search_document_type(VaswaniParser.__type__)

    def __call__(self, text: str) -> list[Document]:
        tuple_docs = self.__tokenize_docs__(text)
        list_docs: list[Document] = []
        for i, docs in enumerate(tuple_docs):
            list_docs.append(self.__typedoc__(str(i + 1), docs))
        return list_docs

    def __tokenize_docs__(self, text: str) -> Generator[tuple[str, str, str, str], None, None]:
        docs_splitted = re.split(f"/", text)
        first = re.split(f"\n", docs_splitted.pop(0), maxsplit=1)
        yield first[1]
        docs_splitted.pop(len(docs_splitted) - 1)
        for doc in docs_splitted:
            current = re.split(f"\n", doc, maxsplit=2)
            yield current[2].replace("\n", " ")
