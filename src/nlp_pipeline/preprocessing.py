"""Turns an InternalDocument into a NormalizedDocument.

The important thing this module does NOT do: change the text. No lowercasing, no
whitespace collapsing, no stripping. Rewriting the text would shift every character
position, and evidence spans downstream would then point at the wrong characters in
the real article -- silently. So the text is copied through untouched and every
"normalisation" is stored as a label on a token instead.

Input is a string of text. This module never opens a file.
"""

import re
import unicodedata

from core.internal_document import InternalDocument
from nlp_pipeline.shared_types import Token, NormalizedDocument

# A word (optionally with an apostrophe, e.g. "don't"), or a single non-space symbol.
# finditer gives us the start position of each match for free, which is where Token.idx
# comes from.
TOKEN_PATTERN = re.compile(r"\w+(?:['’]\w+)*|[^\w\s]")

# Small hand-written stopword list. Kept here rather than pulled from nltk/spacy so the
# list is visible, versionable and identical on every machine.
STOPWORDS = frozenset("""
a an the and or but if then else when while of in on at by for with about against between
into through during before after above below to from up down out off over under again further
is are was were be been being am do does did doing have has had having i me my we our you your
he him his she her it its they them their this that these those as not no nor so than too very
s t can will just don should now
""".split())


class TextProcessor:
    def __init__(self, lang_config=None, normalization_config=None):
        self.lang_config = lang_config or {}
        self.normalization_config = normalization_config or {}

    def _normalize_unicode(self, text: str) -> str:
        """NFC composition only -- 'e' + combining accent becomes the single character 'e-acute'.

        This is the one rewrite allowed, and it happens once at the boundary so that
        everything downstream measures offsets against the same string. Running it twice
        changes nothing, which is what makes the pipeline idempotent.
        """
        return unicodedata.normalize("NFC", text)

    def _is_punct(self, word: str) -> bool:
        return all(not ch.isalnum() for ch in word)

    def _lemmatize(self, word: str) -> str:
        # No lemmatiser yet -- the lowercase form stands in for it. Swapping in spaCy
        # later only changes this one function.
        return word

    def _tokenize(self, text: str) -> list:
        tokens = []
        for match in TOKEN_PATTERN.finditer(text):
            word = match.group()
            lower = word.lower()
            tokens.append(Token(
                text=word,
                lower=lower,
                lemma=self._lemmatize(lower),
                idx=match.start(),
                is_stop=lower in STOPWORDS,
                is_punct=self._is_punct(word),
            ))
        return tokens

    def normalize(self, doc: InternalDocument) -> NormalizedDocument:
        text = self._normalize_unicode(doc.text)
        return NormalizedDocument(
            document_id=doc.document_id,
            text=text,
            tokens=self._tokenize(text),
            language=doc.language or self.lang_config.get("language"),
            metadata={
                "source_type": doc.source_type.value,
                "title": doc.title,
                "author": doc.author,
            },
        )
