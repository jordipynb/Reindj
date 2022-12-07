import re
import json
from typing import Generator
from . import Qrydb
from abc import ABC, abstractmethod


class QryParser(ABC):
    __type__ = "default"

    @abstractmethod
    def __call__(self, text: str) -> list[Qrydb]:
        pass

    @classmethod
    def search_qry_parser_type(self, _type: str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Query Parser Type")
        return cls[_type]()


class CranfieldQryParser(QryParser):
    __type__ = "cranfield"

    def __init__(self):
        self.__typedoc__ = Qrydb.search_qry_type(CranfieldQryParser.__type__)
        self.__match_Index__ = re.compile("\.I")
        self.__match_Text__ = re.compile("\\n\.W\\n")

    def __call__(self, text: str) -> list[Qrydb]:
        queries = self.__tokenize_qrys__(text)
        list_qries: list[Qrydb] = []
        for i, qry in enumerate(queries): list_qries.append(self.__typedoc__(str(i + 1), qry))
        return list_qries

    def __tokenize_qrys__(self, text: str) -> Generator[tuple[str, str], None, None]:
        qrys_splitted = re.split(self.__match_Index__, text)
        qrys_splitted.pop(0)
        for qry in qrys_splitted:
            yield re.split(self.__match_Text__, qry, 1)[1]


class VaswaniQryParser(QryParser):
    __type__ = "vaswani"
    
    def __init__(self):
        self.__typedoc__ = Qrydb.search_qry_type(VaswaniQryParser.__type__)

    def __call__(self, text:str) -> list[Qrydb]:
        queries = self.__tokenize_qrys__(text)
        list_qries:list[Qrydb] = []
        for i,qry in enumerate(queries):
             list_qries.append(self.__typedoc__(str(i+1),qry))
        return list_qries

    def __tokenize_qrys__(self, text: str) -> Generator[tuple[str,str],None,None]:
        qrys_splitted = re.split(f"/", text)
        first=re.split(f"\n",qrys_splitted.pop(0),maxsplit=1)
        yield first[1]
        qrys_splitted.pop(len(qrys_splitted)-1)
        for qry in qrys_splitted:
            current=re.split(f"\n",qry,maxsplit=2)
            yield current[2]

class TrecCovidQryParser(QryParser):
    __type__ = "trec-covid"

    def __int__(self):
        self.__typedoc__= Qrydb.search_qry_type(TrecCovidQryParser.__type__)

    def __call__(self, text: str) -> list[Qrydb]:
        qry_dict= json.loads(text)
        qry_list: list(Qrydb) = []
        for qry in qry_dict:
            qry_list.append(self.__typedoc__(int(qry['id']), qry['text'], qry['metadata']))
        return qry_list