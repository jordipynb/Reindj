from abc import ABC, abstractmethod


class Qrydb(ABC):
    __type__ = "default"

    def __init__(self, id: int, text: str):
        self.id = id
        self.text = text

    def __getitem__(self, index: int) -> str:
        return self.text[index]

    @abstractmethod
    def __call__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @classmethod
    def search_qry_type(self, _type: str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Query Type")
        return cls[_type]


class CranfieldQry(Qrydb):
    __type__ = "cranfield"

    def __init__(self, id: int, text: str):
        Qrydb.__init__(self, id, text.lower())

    def __call__(self): pass

    def __eq__(self, other):
        if isinstance(other, CranfieldQry):
            return self.id == other.id
        raise TypeError("The \'other\' argument must be a Cranfield Query")


class TrecCovidQry(Qrydb):
    __type__ = "trec-covid"

    def __int__(self, id: int, text: str, metadata: dict):
        Qrydb.__init__(self, id, text.lower())
        self.metadata = metadata

    def __call__(self): pass

    def __eq__(self, other):
        if isinstance(other, TrecCovidQry):
            return self.id == other.id
    raise TypeError("The \'other\' argument must be a trec-COVID Query")


class VaswaniQry(Qrydb):
    __type__ = "vaswani"

    def __init__(self, id:int, text:str):
        Qrydb.__init__(self, id, text.lower())

    def __call__(self): pass

    def __eq__(self, other):
        if isinstance(other, VaswaniQry):
            return self.id == other.id
        raise TypeError("The \'other\' argument must be a Vaswani Query")
