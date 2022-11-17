from abc import ABC, abstractmethod
from collections import defaultdict

class TesterParser(ABC):
    __type__ = "default"

    @abstractmethod
    def __call__(self, qry_doc:list[str]) -> dict[str,list[str]]:pass

    @classmethod
    def search_tester_parser_type(self, _type:str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Tester Parser Type")
        return cls[_type]()

class CranfieldTesterParser(TesterParser):
    __type__ = "cranfield"

    def __call__(self, qry_doc:list[str]) -> dict[str,list[str]]:
        result:defaultdict[str,list] = defaultdict(list)
        for rel in qry_doc:
            rel_splitted = rel.split()
            qry, doc = rel_splitted[0], rel_splitted[1]
            result[qry].append(doc)
        return result