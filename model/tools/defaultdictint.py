from collections import defaultdict
class defaultdictint:
    def __init__(self):
        self.dict:defaultdict[int,int] = defaultdict(int)

    def __call__(self, key:int, incr:int):
        self.dict[key] += incr
        return self.dict

    def __iter__(self):
        return iter(self.dict.items())

    def __repr__(self) -> str:
        return str(dict(self.dict))

    def __len__(self) -> int:
        return len(self.dict)