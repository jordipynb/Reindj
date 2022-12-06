from abc import ABC, abstractmethod


class Metrics(ABC):
    @abstractmethod
    def __call__(self, REC: list[int], REL: list[int]) -> float: pass


class Recall(Metrics):
    def __call__(self, REC: list[int], REL: list[int]) -> float:
        rec = set(REC)  # recuperados
        rel = set(REL)  # relevantes
        rr = rec.intersection(rel)  # relevantes recuperados
        return len(rr) / len(rel)  # SOBRE LOS DOCUMENTOS RELEVANTES (recuperados y no recuperados)


class Precission(Metrics):
    def __call__(self, REC: list[int], REL: list[int]) -> float:
        rec = set(REC)  # recuperados
        rel = set(REL)  # relevantes
        rr = rec.intersection(rel)  # relevantes recuperados
        return len(rr) / len(rec)  # SOBRE LOS DOCUMENTOS RECUPERADOS (relevantes e irrelevantes)


class FMean(Metrics):
    def __call__(self, REC: list[int], REL: list[int], beta: float = 0.7) -> float:
        R = Recall()(REC, REL)
        P = Precission()(REC, REL)
        return (1 + beta ** 2) / ((1 / P) + (beta ** 2 / R)) if P != 0 and R != 0 else 0


class F1Mean(Metrics):
    def __call__(self, REC: list[int], REL: list[int]) -> float:
        R = Recall()(REC, REL)
        P = Precission()(REC, REL)
        return 2 / ((1 / P) + (1 / R)) if P != 0 and R != 0 else 0
