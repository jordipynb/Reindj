from abc import ABC, abstractmethod
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from . import Qrydb
import numpy as np
import re


class QryIndexer(ABC):
    __type__ = "default"

    @abstractmethod
    def __call__(self, qry:Qrydb, terms:list[str], vector:list[float]=None) -> np.ndarray:pass

    @classmethod
    def search_qry_indexer_type(self, _type: str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Query Indexer Type")
        return cls[_type]()


class VectorQryIndexer(QryIndexer):
    __type__ = "vector"
    
    def __call__(self, qry:Qrydb, terms:list[str], S,idf:list[float]=None) -> np.ndarray:
        if idf is None or len(idf) == 0: raise Exception("idf is necessary and is Empty")
        text = qry.text
        dict_terms, max_frequency = self.__extract_terms__(text)
        return self.__get_weight__(terms, idf, dict_terms, max_frequency)

    def __extract_terms__(self, text: str) -> tuple[dict[str, int], int]:
        separators = ("\n", "|", "\"", " ", "\\", "/", "{", "}", "[", "]", "(", ")", "`", "^", "&",
                      "-", "+", "*", "!", "?", ".", ",", ";", ":", "\'", "#", "$", "@", "%", "~", "<", ">", "=")
        is_relevant = lambda pos: pos == 'NOUN' or pos == 'ADJ' or pos == 'VERB'
        stop_words: set[str] = set(stopwords.words('english'))
        dict_terms: dict[str, int] = defaultdict(int)
        max_frequency = 0
        terms_pos: dict[str, str] = defaultdict(str)
        regular_exp = '|'.join(map(re.escape, separators))
        text = re.split(regular_exp, text)
        tokenize = list(filter("".__ne__, text))
        for token in tokenize:
            # if len(token) < 3: continue
            if not token in stop_words:
                word_lemmatize = WordNetLemmatizer().lemmatize(token)
                lemmatize = [word_lemmatize]
                pos = terms_pos[word_lemmatize]
                if pos == "":
                    word, pos = pos_tag(lemmatize, tagset='universal')[0]
                    terms_pos[word] = pos
                if is_relevant(pos):
                    value = dict_terms[word_lemmatize] = dict_terms[word_lemmatize] + 1
                    max_frequency = max(value, max_frequency)
        return dict_terms, max_frequency

    def __get_weight__(self, terms: list[str], idf: list[float], dict_terms: dict[str, int],
                       max_frequency: list[int]) -> np.ndarray:
        weight = np.zeros(len(terms))
        for term, value in dict_terms.items():
            if term in terms:
                index = terms.index(term)
                idf_value = idf[index]
                tf_iq = value / max_frequency
                weight[index] = (0.5 + 0.5 * tf_iq) * idf_value
        return weight


class Latent_Semantic_Indexer(QryIndexer):
    __type__ = "latent_semantic"

    def __call__(self, qry:Qrydb,terms:list[str], T:np.array,S:np.array,) -> np.ndarray:
        text = qry.text
        q= self.__extract_terms__(text,terms)
        t=np.dot(np.linalg.inv(S),T.transpose())
        return np.dot(t,q)

    def __extract_terms__(self, text:str, terms:list[str]) -> np.ndarray:
        separators = ("\n", "|", "\"", " ", "\\", "/", "{", "}", "[", "]", "(", ")","`","^","&",
                      "-","+","*","!","?",".",",",";",":","\'","#","$","@","%","~","<",">","=")
        is_relevant = lambda pos: pos == 'NOUN' or pos == 'ADJ' or pos == 'VERB'
        stop_words:set[str] = set(stopwords.words('english'))
        vector:np.ndarray= np.zeros(len(terms))
        terms_pos:dict[str,str] = defaultdict(str)
        regular_exp = '|'.join(map(re.escape, separators))
        text = re.split(regular_exp,text)
        tokenize = list(filter(("").__ne__, text))
        for token in tokenize:
            if not token in stop_words:
                word_lemmatize = WordNetLemmatizer().lemmatize(token)
                lemmatize = [word_lemmatize]
                pos = terms_pos[word_lemmatize]
                if pos == "":
                    word,pos = pos_tag(lemmatize, tagset='universal')[0]
                    terms_pos[word] = pos
                    if is_relevant(pos) and word in terms:
                        vector[terms.index(word)]=1
        return vector


class BooleanQryIndexer(QryIndexer):
    __type__ = "boolean"

    def __call__(self, qry: Qrydb, terms: dict[str, np.ndarray], T, idf) -> np.ndarray:
        text = qry.text
        return self.__extract_terms__(text)

    def __extract_terms__(self, text: str) -> dict[str, int]:
        separators = ("\n", "|", "\"", " ", "\\", "/", "{", "}", "[", "]", "(", ")", "`", "^", "&",
                      "-", "+", "*", "!", "?", ".", ",", ";", ":", "\'", "#", "$", "@", "%", "~", "<", ">", "=")
        is_relevant = lambda pos: pos == 'NOUN' or pos == 'ADJ' or pos == 'VERB'
        stop_words: set[str] = set(stopwords.words('english'))
        dict_terms: dict[str, int] = defaultdict(int)
        terms_pos: dict[str, str] = defaultdict(str)
        regular_exp = '|'.join(map(re.escape, separators))
        text = re.split(regular_exp, text)
        tokenize = list(filter("".__ne__, text))
        for token in tokenize:
            if not token in stop_words:
                word_lemmatize = WordNetLemmatizer().lemmatize(token)
                lemmatize = [word_lemmatize]
                pos = terms_pos[word_lemmatize]
                if pos == "":
                    word, pos = pos_tag(lemmatize, tagset='universal')[0]
                    terms_pos[word] = pos
                if is_relevant(pos):
                    dict_terms[word] = 1
        return dict_terms
