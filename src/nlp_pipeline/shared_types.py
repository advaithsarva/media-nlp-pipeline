"""Shapes passed between pipeline stages. No logic lives here.

Only stdlib and `core` may be imported by this module -- importing anything else
from nlp_pipeline or io_adapters creates a circular import.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


# "Label, don't rewrite": `text` is the word exactly as it appears in the document,
# `lower` and `lemma` are labels sitting next to it. Because the document text is
# never modified, `idx` stays a true position into it forever.
@dataclass(frozen=True)
class Token:
    text: str
    lower: str
    lemma: str
    idx: int          # start position in the original document text
    is_stop: bool
    is_punct: bool


# Invariant: document_text[start_char:end_char] == text
# If that ever breaks, every offset downstream is wrong.
@dataclass(frozen=True)
class Sentence:
    sentence_id: int
    text: str
    start_char: int
    end_char: int     # exclusive, like a Python slice


# A named thing spaCy found -- a person, organisation, nationality or place. Offsets come
# straight from spaCy and refer to the same untouched document text as everything else,
# which is why an entity mention can be quoted as evidence like any other span.
@dataclass(frozen=True)
class Entity:
    text: str
    label: str        # PERSON, ORG, NORP, GPE, ...
    start_char: int
    end_char: int
    sentence_id: int


@dataclass
class NormalizedDocument:
    """The original text plus annotations. Deliberately has no `clean_text` field."""
    document_id: str
    text: str
    tokens: List[Token]                 # required: a document with no tokens hides a bug
    sentences: List[Sentence] = field(default_factory=list)
    # Empty unless the entity stage ran. Detectors that need entities check this and
    # stay quiet when it is empty, rather than guessing.
    entities: List[Entity] = field(default_factory=list)
    # entity key -> {mentions, sentence_ids, average_sentiment}. Filled by EntityAnalyzer.
    entity_sentiment: Dict[str, Any] = field(default_factory=dict)
    language: Optional[str] = None
    # default_factory so each instance gets its own dict instead of sharing one
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def word_count(self) -> int:
        return sum(1 for t in self.tokens if not t.is_punct)


# Evidence is a first-class object, not a string bolted onto a result (R4).
# Same slice invariant as Sentence. `rule_id` is what makes a score traceable
# back to the exact rule that produced it.
@dataclass(frozen=True)
class EvidenceSpan:
    text: str
    start_char: int
    end_char: int
    rule_id: str
    category: str
    confidence: float
    sentence_id: int


@dataclass
class RuleClassificationResult:
    document_id: str
    spans: List[EvidenceSpan] = field(default_factory=list)

    def spans_for(self, category: str) -> List[EvidenceSpan]:
        return [s for s in self.spans if s.category == category]

    @property
    def categories(self) -> List[str]:
        # sorted, not set-order: iteration order over a set is not stable between runs
        return sorted({s.category for s in self.spans})


@dataclass
class CategoryScore:
    category: str
    count: int          # how many evidence spans fired
    raw: float          # sum of the confidences of those spans
    score: float        # raw, length-normalised into 0..1
    calibrated: bool = False   # always False until a labelled eval set exists (R3)


@dataclass
class ScoredDocument:
    document_id: str
    spans: List[EvidenceSpan] = field(default_factory=list)
    category_scores: Dict[str, CategoryScore] = field(default_factory=dict)
    # The single headline number. Stays None unless expose_composite is turned on,
    # because the detectors underneath it have not been measured yet.
    composite: Optional[float] = None
    # Severity, accumulation and logical-flow disruption (claudenew.md 12.4 / 21.1).
    severity: Dict[str, Any] = field(default_factory=dict)
    # Every composite plus the breakdown that produced it. Always computed, so it can be
    # inspected, and published only when expose_composite says so.
    composites: Dict[str, Any] = field(default_factory=dict)
