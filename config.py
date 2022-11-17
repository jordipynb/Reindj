from json import load
from pathlib import Path

class Configuration:
    def __init__(self):
        self.__dict__ = load(open(f"./config.json","r"))

    def db_path(self, _type:str) -> Path:
        return Path(self.db[_type]["path"])

    def qry_path(self, _type:str) -> Path:
        return Path(self.db[_type]["qry"])

    def rel_path(self, _type:str) -> Path:
        return Path(self.db[_type]["rel"])

    def get_top(self) -> int:
        return self.top

    def get_umbral(self) -> float:
        return self.umbral