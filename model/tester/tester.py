from config import Configuration
from model.framework import Framework
from .testerparser import TesterParser

class Tester:
    def __init__(self, framework:Framework):
        self.__framework__ = framework
        self.__typedb__ = self.__framework__.__typedb__
        self.__path__ = Configuration().rel_path(self.__typedb__)

    def __get_rel__(self) -> dict[str, list[str]]:
        return TesterParser.search_tester_parser_type(self.__typedb__, self.__framework__.__documents__())(self.__path__)
