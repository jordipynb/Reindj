from . import Document

class Corpus:
    def __init__(self, docs:list[Document]):
        self.__docs__ = docs
        self.__bodies__ = list(map(lambda doc: doc.text, self.__docs__))
    
    def __len__(self) -> int:
        return len(self.__docs__)

    def __getitem__(self, index:int) -> Document:
        return self.__docs__[index]

    def __iter__(self) -> list[Document]:
        return iter(self.__docs__)

    @property
    def bodies(self) -> list[str]:
        return self.__bodies__