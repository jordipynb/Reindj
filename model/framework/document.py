from abc import ABC, abstractmethod

class Document(ABC):
    __type__ = "default"

    def __init__(self, id:str, text:str):
        self.id = id
        self.text = text

    @abstractmethod
    def __call__(self): pass

    @classmethod
    def search_document_type(self, _type:str):
        cls = {}
        for _cls in self.__subclasses__():
            cls[_cls.__type__] = _cls
        if not _type in cls:
            raise Exception("Unknown Document Type")
        return cls[_type]


class CranfieldDocument(Document):
    __type__ = "cranfield"

    def __init__(self, id:str, title:str, text:str, author:str, editorial:str):
        Document.__init__(self, id, text.lower())
        self.author = author.lower()
        self.editorial = editorial.lower()

    def __call__(self): pass


class TrecCovidDocument(Document):
    __type__ = "trec-covid"

    def __init__(self, id: str, title: str, text: str, metadata: dict):
        Document.__init__(self, id, text.lower())
        self.title = title
        self.metadata = metadata

    def __call__(self): pass


class VaswaniDocument(Document):
    __type__ = "vaswani"

    def __init__(self, id:str, text:str):
        Document.__init__(self, id, text.lower())

    def __call__(self): pass