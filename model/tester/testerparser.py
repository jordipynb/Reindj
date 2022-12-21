from abc import ABC, abstractmethod
from collections import defaultdict

import re


class TesterParser(ABC):
    __type__ = "default"

    @abstractmethod
    def __call__(self, qry_doc: list[str], docs=None) -> dict[str, list[str]]:
        pass

    @classmethod
    def search_tester_parser_type(self, _type: str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Tester Parser Type")
        return cls[_type]()


class CranfieldTesterParser(TesterParser):
    __type__ = "cranfield"

    def __call__(self, path: str, docs=None) -> dict[str, list[str]]:
        with open(path, "r", encoding='utf8') as qry_doc_path: qry_doc = qry_doc_path.readlines()
        result: defaultdict[str, list] = defaultdict(list)
        for rel in qry_doc:
            rel_split = rel.split()
            qry, doc = rel_split[0], rel_split[1]
            result[qry].append(doc)
        return result

    class TrecCovidTesterParser(TesterParser):
        __type__ = "trec-covid"

        def __call__(self, qry_doc: list[str], docs =None) -> dict[str, list[str]]:
            result: defaultdict[str, list] = defaultdict(list)
            qry_doc.pop(0)
            for rel in qry_doc:
                rel_split = rel.split()
                qry, doc = rel_split[0], rel_split[1]
                result[qry].append(doc)
            return result


class VaswaniTesterParser(TesterParser):
    __type__ = "vaswani"

    def __call__(self, path: str, docs=None) -> dict[str, list[str]]:
        with open(path, "r", encoding='utf8') as qry_doc_path: qry_doc = qry_doc_path.read()
        querys = qry_doc.split('/')
        querys.pop(len(querys) - 1)
        result: defaultdict[str, list[str]] = defaultdict(lambda: [])
        querys[0] = "\n" + querys[0]
        for item in querys:
            temp = item.split("\n", maxsplit=2)
            qry = temp[1]
            docs = re.split(' ', temp[2].replace("\n", " ").replace("  ", " "))
            result[qry] = list(filter(lambda x: not (x == ''), docs))
        return result
