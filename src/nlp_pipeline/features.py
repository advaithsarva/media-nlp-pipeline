# Feature engineering: n-grams, TF-IDF, other signals used by rules/ML.
from collections import Counter
from typing import Dict,Any,List
import spacy
from nlp_pipeline.shared_types import NormalizedDocument, Sentence
class FeatureExtractor:
    def __init__(self,feature_config:Dict[str,Any]):
        pass
    def _tokenize(self,text:str)->List[str]:
        pass
    def _extract_ngrams(self,tokens:List[str])->Counter:
        pass

    def build_features(normailzed_doc,segments,metadata):
        pass

class LogicalFallacy:
    pass
class Rhetorical:
    pass
class Bais:
    pass
class Sentiment_Subjecivity:
    pass
class Stance:
    pass
class FactCheck:
    pass
class Linguistic:
    pass
class Mathematics:
    pass
class Deterministic:
    pass
class Metadata:
    pass
class Advanced:
    pass
