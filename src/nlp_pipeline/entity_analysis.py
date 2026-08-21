"""Finds the people, organisations and places in a document, and how the article treats each.

Two detectors need this and could not be built without it:

  scapegoating   one group blamed repeatedly for unrelated problems -- you cannot count
                 "blamed for" per group without knowing which words name a group
  card_stacking  one side described warmly and the other coldly -- you cannot compare
                 sentiment per side without knowing which side each sentence is about

Both were in the original design and stayed unbuilt for exactly this reason.

Two libraries, both chosen because they are reproducible:

  spaCy en_core_web_sm  named entity recognition. A statistical model, but inference is
                        deterministic: no dropout, no sampling, and the weights are frozen
                        in a pinned package version. Same text, same entities, always.
  VADER                 sentiment. A lexicon plus a handful of rules -- not a model at all,
                        so it cannot drift. Chosen over TextBlob (which needs an NLTK
                        corpus download) and over a transformer (which needs a GPU budget
                        and would still be harder to explain to a reader).

The model name and version are written into the document metadata, because a different
spaCy model would find different entities and the output has to say which one ran.

Loading spaCy costs about a second and 50MB. That is why this stage is optional: if no
entity-based category is switched on, it never loads.
"""

from nlp_pipeline.shared_types import Entity

# The labels worth analysing. PERSON and ORG for card stacking; NORP (nationalities,
# religious and political groups) and GPE (countries, cities) because those are what
# scapegoating actually targets.
DEFAULT_LABELS = ("PERSON", "ORG", "NORP", "GPE")


class EntityAnalyzer:
    def __init__(self, config=None):
        config = config or {}
        self.model_name = config.get("spacy_model", "en_core_web_sm")
        self.labels = tuple(config.get("entity_labels", DEFAULT_LABELS))
        self._nlp = None
        self._sentiment = None

    # ---------- lazy loading ----------

    @property
    def nlp(self):
        """Loaded on first use, then kept. Building it per document would dominate runtime."""
        if self._nlp is None:
            import spacy
            # only the NER component is needed; skipping the parser and lemmatizer makes
            # this roughly three times faster
            self._nlp = spacy.load(self.model_name, disable=["parser", "lemmatizer"])
        return self._nlp

    @property
    def sentiment(self):
        if self._sentiment is None:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self._sentiment = SentimentIntensityAnalyzer()
        return self._sentiment

    def model_version(self):
        try:
            return self.nlp.meta.get("version", "unknown")
        except Exception:
            return "unavailable"

    # ---------- the work ----------

    def _sentence_id_at(self, doc, position):
        for sentence in doc.sentences:
            if sentence.start_char <= position < sentence.end_char:
                return sentence.sentence_id
        return -1

    def _entity_key(self, text):
        """Group mentions of the same thing together.

        Crude on purpose: lowercase and strip a leading article. Real coreference would
        merge "the mayor" with "Lopez", and that is a much larger problem than this stage
        is trying to solve. Documented rather than half-attempted.
        """
        key = " ".join(text.lower().split())
        for article in ("the ", "a ", "an "):
            if key.startswith(article):
                key = key[len(article):]
        return key

    def extract_entities(self, doc):
        spacy_doc = self.nlp(doc.text)
        entities = []
        for ent in spacy_doc.ents:
            if ent.label_ not in self.labels:
                continue
            # spaCy's offsets are into the exact string we handed it, which is the same
            # untouched document text everything else measures against -- so an entity
            # mention slices back out of the article like any other evidence span
            entities.append(Entity(
                text=ent.text,
                label=ent.label_,
                start_char=ent.start_char,
                end_char=ent.end_char,
                sentence_id=self._sentence_id_at(doc, ent.start_char),
            ))
        return entities

    def score_entity_sentiment(self, doc, entities):
        """How positively or negatively the article speaks in each entity's sentences.

        Sentence-level, not entity-level: VADER scores text, and the sentence an entity
        appears in is the closest honest approximation of "how this entity is described".
        A sentence mentioning two entities contributes its score to both -- a real
        limitation, and the reason card_stacking needs a wide gap before it fires.
        """
        by_entity = {}
        sentence_scores = {}

        for entity in entities:
            if entity.sentence_id < 0:
                continue
            if entity.sentence_id not in sentence_scores:
                text = doc.sentences[entity.sentence_id].text
                sentence_scores[entity.sentence_id] = \
                    self.sentiment.polarity_scores(text)["compound"]

            key = self._entity_key(entity.text)
            record = by_entity.setdefault(key, {
                "label": entity.label,
                "mentions": 0,
                "sentence_ids": [],
                "scores": [],
            })
            record["mentions"] += 1
            if entity.sentence_id not in record["sentence_ids"]:
                record["sentence_ids"].append(entity.sentence_id)
                record["scores"].append(sentence_scores[entity.sentence_id])

        result = {}
        for key, record in by_entity.items():
            scores = record["scores"] or [0.0]
            result[key] = {
                "label": record["label"],
                "mentions": record["mentions"],
                # sorted so the stored order does not depend on which mention came first
                "sentence_ids": sorted(record["sentence_ids"]),
                "average_sentiment": round(sum(scores) / len(scores), 6),
            }
        return result

    def analyze(self, doc):
        entities = self.extract_entities(doc)
        # sorted by position: canonical order, so two runs serialise identically
        entities.sort(key=lambda e: (e.start_char, e.end_char, e.label))

        doc.entities = entities
        doc.entity_sentiment = self.score_entity_sentiment(doc, entities)
        doc.metadata["entity_model"] = self.model_name + ":" + self.model_version()
        return doc
