from abc import ABC, abstractmethod
from nltk import pos_tag, download, data
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from ..tools import defaultdictint
import numpy as np
import re
import nltk
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# # nltk.download()
# ### region Download resource before use
# # try:
# #    data.find('tokenizers/punkt')
# # except LookupError:
# nltk.download('punkt')
#
# # try:
# #    data.find("corpora/omw-1.4")
# # except LookupError:
# nltk.download('omw-1.4')
#
# # try:
# #    data.find("corpora/wordnet")
# # except LookupError:
# nltk.download("wordnet")
#
# # try:
# #    data.find("taggers/averaged_perceptron_tagger")
# # except LookupError:
# nltk.download('averaged_perceptron_tagger')
#
# # try:
# #    data.find("corpora/stopwords")
# # except LookupError:
# nltk.download("stopwords")
# ### endregion
#
# nltk.download('universal_tagset')

class Indexer(ABC):
    __type__ = "default"

    @abstractmethod
    def __call__(self, docs_bodies: list[str]) -> tuple[np.ndarray, np.ndarray, list[str]]:
        pass

    @classmethod
    def search_indexer_type(self, _type: str):
        cls = {}
        for _cls in self.__subclasses__(): cls[_cls.__type__] = _cls
        if not _type in cls: raise Exception("Unknown Indexer Type")
        return cls[_type]()


class VectorIndexer(Indexer):
    __type__ = "vector"

    def __call__(self, docs_bodies: list[str]) -> tuple[np.ndarray, np.ndarray, list[str]]:
        dict_terms, max_frequency = self.__extract_terms__(docs_bodies)
        N = len(docs_bodies)
        n = len(dict_terms)
        return self.__get_weight__(N, n, dict_terms, max_frequency)

    def __extract_terms__(self, docs_bodies: list[str]) -> tuple[dict[str, dict[int, int]], np.ndarray]:
        separators = ("\n", "|", "\"", " ", "\\", "/", "{", "}", "[", "]", "(", ")", "`", "^", "&",
                      "-", "+", "*", "!", "?", ".", ",", ";", ":", "\'", "#", "$", "@", "%", "~", "<", ">", "=")
        is_relevant = lambda pos: pos == 'NOUN' or pos == 'ADJ' or pos == 'VERB'
        stop_words: set[str] = set(stopwords.words('english'))
        dict_terms: dict[str, dict[int, int]] = defaultdict(defaultdictint)
        max_frequency = np.zeros(len(docs_bodies))
        terms_pos: dict[str, str] = defaultdict(str)
        for i, doc_text in enumerate(docs_bodies):
            max_temp = 0
            regular_exp = '|'.join(map(re.escape, separators))
            doc_text = re.split(regular_exp, doc_text)
            tokenize = list(filter(("").__ne__, doc_text))
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
                        value = dict_terms[word_lemmatize](i, 1)
                        max_temp = max(value[i], max_temp)
            max_frequency[i] = max_temp
        return dict_terms, max_frequency

    def __get_weight__(self, n_doc: int, n_terms: int, dict_terms: dict[str, dict[int, int]],
                       max_frequency: list[int]) -> tuple[np.ndarray, np.ndarray, list[str]]:
        idf = np.zeros(n_terms)
        weight = np.zeros((n_doc, n_terms))
        for i, (_, value) in enumerate(dict_terms.items()):
            idf[i] = np.log10((n_doc + 1) / len(value))
            for j, count in value:
                tf_ij = count / max_frequency[j]
                weight[j][i] = idf[i] * tf_ij
        return weight, idf, list(dict_terms.keys())


class BooleanIndexer(Indexer):
    __type__ = "boolean"

    def __call__(self):
        pass
