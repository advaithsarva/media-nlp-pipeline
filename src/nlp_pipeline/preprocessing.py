#All text cleaning + normalization: lowercase, Unicode, HTML strip, etc.
import re
import unicodedata
from typing import Dict, Any

from io_adapters.shared_types import InternalDocument
from nlp_pipeline.shared_types import NormalizedDocument

class TextProcessor:
    def __init__(self,lang_config,normalization_config):
        pass
    def _strip_html(self,text:str)-> str:
        pass
    def _normalize_unicode(self,text:str)->str:
        pass
    def _normalize_whitespace(self,text:str)->str:
        pass
    def _lemmatize(self,text:str)->str:
        pass
    def normalize(self,doc:InternalDocument)->NormalizedDocument:
        pass