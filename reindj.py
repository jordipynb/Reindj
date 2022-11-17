from model.framework import Framework,Document
from model.query import Query
from model.ranking import Rank
from model.tester import Tester
from model.tools import Precission, Recall, FMean, F1Mean
import numpy as np

class Reindj:
    def __init__(self, __typedb__:str, __typemodel__:str):
        self.__typedb__ = __typedb__
        self.__typemodel__ = __typemodel__   
        self.framework = Framework(self.__typedb__, self.__typemodel__)
        self.qry = Query(self.framework)
        self.rank = Rank(self.framework)
        self.tester = Tester(self.framework)

    def evaluate(self):
        self.queries = self.qry.__get_queries__()
        rel = self.tester.__get_rel__()
        metrics = np.array([Precission(), Recall(), FMean(), F1Mean()])
        results = [[],[],[],[]]
        for i in rel.keys():
            if self.qry.__typeqry__(i, "") in self.queries:
                qry = self.queries[self.queries.index(self.qry.__typeqry__(i, ""))]
                docs_rec = list(map(lambda doc:doc.id, self.doc_query(qry.text)))
                for i, metric in enumerate(metrics): results[i].append(metric(docs_rec, rel[qry.id]))
        evaluation = {
            "P" : np.mean(results[0]),
            "R" : np.mean(results[1]),
            "F" : np.mean(results[2]),
            "F1": np.mean(results[3])
        }
        return evaluation

    def doc_query(self, text_qry:str) -> list[Document]:
        weight = self.qry(text_qry)
        return self.rank.get_top_list(weight)