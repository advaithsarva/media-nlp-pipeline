"""Runs the taxonomy's detectors over the text and returns evidence spans.

Two properties matter more than coverage here:

1. Every hit carries the exact substring plus its start and end position in the original
   document, so a reader can check the claim against the article. Nothing is paraphrased.
2. The same document always produces the same spans in the same order. Categories,
   sentences and patterns are all walked in a fixed order, and the result is sorted before
   it is returned.

Five detector kinds, each matching a rule shape that actually appears in the design notes:

    lexicon        a word from a list                       "disastrous"
    regex          a phrase pattern                         "everyone knows"
    regex_unless   a pattern, but only when the sentence     "many people" with no
                   does NOT also contain a context cue       number, %, study or source
    cooccurrence   N or more terms from a list inside one    two virtue words in a
                   short sentence                            slogan-length sentence
    repetition     an n-gram repeated across the document    a slogan used four times

`regex_unless` is the one that makes precision possible. "Many respondents (37%) agreed"
and "many people are saying" are the same phrase doing opposite jobs; only the presence of
supporting context separates them.
"""

import re
from collections import Counter

from nlp_pipeline.shared_types import EvidenceSpan, RuleClassificationResult, NormalizedDocument

DETECTOR_KINDS = ("lexicon", "regex", "regex_unless", "cooccurrence", "repetition",
                  "entity_blame", "entity_sentiment_split")


class RuleEngine:
    def __init__(self, taxonomy, threshold=None):
        self.taxonomy = taxonomy
        self.threshold = taxonomy.default_threshold if threshold is None else threshold
        self.rules = self._compile_rules()

    # ---------- setup ----------

    def _lexicon_pattern(self, terms):
        """One alternation regex for a whole word list, so the text is scanned once.

        re.escape matters: nothing in the current lists contains a regex-special
        character, but a term added later with a "." or "(" would quietly break the
        pattern rather than fail.
        """
        return re.compile(r"\b(?:" + "|".join(re.escape(t) for t in terms) + r")\b", re.IGNORECASE)

    def _compile_rules(self):
        compiled = []
        for cat in self.taxonomy.categories:
            if cat.detector == "lexicon":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":lexicon",
                    "kind": "lexicon",
                    "pattern": self._lexicon_pattern(cat.terms),
                })

            elif cat.detector == "regex":
                for i, pattern in enumerate(cat.patterns):
                    compiled.append({
                        "category": cat,
                        "rule_id": cat.id + ":regex:" + str(i),
                        "kind": "regex",
                        "pattern": re.compile(pattern, re.IGNORECASE),
                    })

            elif cat.detector == "regex_unless":
                # one shared "the sentence is properly supported" test for the category
                unless = self._lexicon_pattern(cat.unless_terms) if cat.unless_terms else None
                unless_patterns = [re.compile(p, re.IGNORECASE) for p in cat.unless_patterns]
                for i, pattern in enumerate(cat.patterns):
                    compiled.append({
                        "category": cat,
                        "rule_id": cat.id + ":unless:" + str(i),
                        "kind": "regex_unless",
                        "pattern": re.compile(pattern, re.IGNORECASE),
                        "unless": unless,
                        "unless_patterns": unless_patterns,
                    })

            elif cat.detector == "cooccurrence":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":cooccurrence",
                    "kind": "cooccurrence",
                    "pattern": self._lexicon_pattern(cat.terms),
                    "min_hits": cat.min_hits,
                    "max_words": cat.max_words,
                })

            elif cat.detector == "repetition":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":repetition",
                    "kind": "repetition",
                    "ngram_size": cat.ngram_size,
                    "min_repeats": cat.min_repeats,
                })

            elif cat.detector == "entity_blame":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":entity_blame",
                    "kind": "entity_blame",
                    "pattern": self._lexicon_pattern(cat.terms),
                    "entity_labels": tuple(cat.entity_labels),
                    "min_blamed_sentences": cat.min_blamed_sentences,
                    # spaCy only labels proper nouns, so "Muslims" and "France" are
                    # entities but "migrants" is not. Unnamed groups are the commonest
                    # scapegoat targets in real reporting, so they are supplied by name.
                    "group_pattern": (self._lexicon_pattern(cat.group_terms)
                                      if cat.group_terms else None),
                })

            elif cat.detector == "entity_sentiment_split":
                compiled.append({
                    "category": cat,
                    "rule_id": cat.id + ":entity_sentiment_split",
                    "kind": "entity_sentiment_split",
                    "entity_labels": tuple(cat.entity_labels),
                    "positive_threshold": cat.positive_threshold,
                    "negative_threshold": cat.negative_threshold,
                    "min_entities": cat.min_entities,
                    "min_mentions": cat.min_mentions,
                })

            else:
                raise ValueError(cat.id + ": unknown detector " + repr(cat.detector))

        return compiled

    # ---------- the detectors ----------

    def _quoted_regions(self, text):
        """(start, end) of every stretch between a matched pair of quotation marks.

        Straight and curly quotes both count. Anything longer than 600 characters is
        discarded as an unmatched opening quote rather than a real quotation -- otherwise
        one stray apostrophe swallows half the article.
        """
        regions = []
        for pattern in (r'"([^"]{1,600})"', r'“([^”]{1,600})”'):
            for match in re.finditer(pattern, text):
                regions.append((match.start(), match.end()))
        return regions

    def _in_quotation(self, start, end, regions):
        return any(a <= start and end <= b for a, b in regions)

    def _span(self, doc, sentence, start, end, rule, confidence=None):
        cat = rule["category"]
        return EvidenceSpan(
            text=doc.text[start:end],
            start_char=start,
            end_char=end,
            rule_id=rule["rule_id"],
            category=cat.id,
            confidence=cat.base_confidence if confidence is None else confidence,
            sentence_id=sentence.sentence_id,
            in_quotation=self._in_quotation(start, end, self._quotes),
        )

    def _is_supported(self, sentence_text, rule):
        """True when the sentence carries the evidence that makes the phrase legitimate.

        "Many (37%) of respondents" is supported. "Many people say" is not.
        """
        if rule["unless"] is not None and rule["unless"].search(sentence_text):
            return True
        for pattern in rule["unless_patterns"]:
            if pattern.search(sentence_text):
                return True
        return False

    def _scan_sentence(self, doc, sentence, rule):
        kind = rule["kind"]
        text = sentence.text
        offset = sentence.start_char
        found = []

        if kind in ("lexicon", "regex"):
            for match in rule["pattern"].finditer(text):
                found.append(self._span(doc, sentence, offset + match.start(),
                                        offset + match.end(), rule))

        elif kind == "regex_unless":
            if not self._is_supported(text, rule):
                for match in rule["pattern"].finditer(text):
                    found.append(self._span(doc, sentence, offset + match.start(),
                                            offset + match.end(), rule))

        elif kind == "cooccurrence":
            matches = list(rule["pattern"].finditer(text))
            # a slogan is short and dense; the same two words spread across a long
            # explanatory sentence is ordinary writing, not a slogan
            word_count = len(text.split())
            if len(matches) >= rule["min_hits"] and word_count <= rule["max_words"]:
                # one span covering first hit to last, so the evidence shows the pairing
                start = offset + matches[0].start()
                end = offset + matches[-1].end()
                found.append(self._span(doc, sentence, start, end, rule))

        return found

    def _scan_repetition(self, doc, rule):
        """Phrases repeated across the whole document -- a document-level detector.

        Unlike the others this cannot work sentence by sentence, because the signal is
        precisely that the same phrase keeps coming back.
        """
        size = rule["ngram_size"]
        words = [t for t in doc.tokens if not t.is_punct]
        if len(words) < size:
            return []

        # build every n-gram with the position it starts at, so evidence stays quotable
        ngrams = []
        for i in range(len(words) - size + 1):
            group = words[i:i + size]
            # "of the people in" repeats in any long document and means nothing. A phrase
            # only counts as deliberate repetition if it carries at least one real word.
            if all(w.is_stop for w in group):
                continue
            # And a phrase containing a named entity is the document's subject, not a
            # slogan. Validation against Wikipedia showed this dominating everything else:
            # "the North British Railway" and "the light-dependent reactions" repeat
            # because the article is about them.
            start_of_group = group[0].idx
            end_of_group = group[-1].idx + len(group[-1].text)
            if any(e.start_char < end_of_group and start_of_group < e.end_char
                   for e in doc.entities):
                continue
            phrase = " ".join(w.lower for w in group)
            start = group[0].idx
            end = group[-1].idx + len(group[-1].text)
            ngrams.append((phrase, start, end))

        counts = Counter(phrase for phrase, _, _ in ngrams)
        found = []
        last_end = -1
        for phrase, start, end in ngrams:
            if counts[phrase] < rule["min_repeats"]:
                continue
            # The window slides one word at a time, so a four-word repeated slogan matches
            # as several overlapping n-grams. Reporting all of them turns one repetition
            # into five findings. Keep the first and skip anything overlapping it, which
            # leaves exactly one span per actual occurrence.
            if start < last_end:
                continue
            sentence = self._sentence_at(doc, start)
            if sentence is None:
                continue
            found.append(self._span(doc, sentence, start, end, rule))
            last_end = end
        return found

    def _scan_entity_blame(self, doc, rule):
        """Scapegoating: the same group blamed in several separate sentences.

        claudenew.md 13.2 gives the shape -- for each ORG/NORP/GPE entity, count the
        sentences that also contain a blame phrase, and flag when the count reaches two.
        The threshold is deliberately about *distinct sentences*, not mentions: a single
        sentence naming a group three times is one accusation, not three.

        What is quoted as evidence is the entity mention itself, so the reader sees who
        was blamed and can go and read the sentence around it.
        """
        # which sentences contain a blame phrase at all
        blaming = set()
        for sentence in doc.sentences:
            if rule["pattern"].search(sentence.text):
                blaming.add(sentence.sentence_id)
        if not blaming:
            return []

        # Candidate targets are named entities of the right kind, plus the group nouns
        # from the config. Both are collected as (start, end, sentence_id, key) so the
        # rest of the rule does not care where a target came from.
        targets = {}

        for entity in doc.entities:
            if entity.label in rule["entity_labels"] and entity.sentence_id in blaming:
                key = " ".join(entity.text.lower().split())
                targets.setdefault(key, []).append(
                    (entity.start_char, entity.end_char, entity.sentence_id))

        if rule["group_pattern"] is not None:
            for sentence in doc.sentences:
                if sentence.sentence_id not in blaming:
                    continue
                for match in rule["group_pattern"].finditer(sentence.text):
                    key = match.group().lower()
                    targets.setdefault(key, []).append((
                        sentence.start_char + match.start(),
                        sentence.start_char + match.end(),
                        sentence.sentence_id,
                    ))

        found = []
        for key in sorted(targets):
            mentions = targets[key]
            # distinct sentences, not mentions: naming a group three times in one
            # sentence is one accusation, not three
            if len({m[2] for m in mentions}) < rule["min_blamed_sentences"]:
                continue
            for start, end, sentence_id in mentions:
                found.append(self._span(doc, doc.sentences[sentence_id], start, end, rule))
        return found

    def _scan_entity_sentiment_split(self, doc, rule):
        """Card stacking: one side described warmly, the other coldly.

        claudenew.md 13.2: build an entity-sentiment map and flag when the most positively
        described entity is above +0.5 and the most negative below -0.5. Both ends must be
        extreme -- an article that is warm about everyone is not stacking the deck.

        min_mentions guards the obvious failure: one passing mention in one emotive
        sentence is not evidence of how a whole article treats a subject.
        """
        if not doc.entity_sentiment:
            return []

        eligible = {
            key: record for key, record in doc.entity_sentiment.items()
            if record["label"] in rule["entity_labels"]
            and record["mentions"] >= rule["min_mentions"]
        }
        if len(eligible) < rule["min_entities"]:
            return []

        scores = {k: r["average_sentiment"] for k, r in eligible.items()}
        warmest = max(scores, key=lambda k: (scores[k], k))
        coldest = min(scores, key=lambda k: (scores[k], k))

        if scores[warmest] < rule["positive_threshold"]:
            return []
        if scores[coldest] > rule["negative_threshold"]:
            return []

        # Quote both ends. One span alone would show a warm mention with no hint of the
        # cold one, and the asymmetry is the whole finding.
        wanted = {warmest, coldest}
        found = []
        for entity in doc.entities:
            key = " ".join(entity.text.lower().split())
            if key in wanted and entity.sentence_id >= 0:
                sentence = doc.sentences[entity.sentence_id]
                found.append(self._span(doc, sentence, entity.start_char,
                                        entity.end_char, rule))
        return found

    def _sentence_at(self, doc, position):
        for sentence in doc.sentences:
            if sentence.start_char <= position < sentence.end_char:
                return sentence
        return None

    # ---------- entry point ----------

    def classify(self, doc: NormalizedDocument) -> RuleClassificationResult:
        # computed once per document and read by _span
        self._quotes = self._quoted_regions(doc.text)
        spans = []

        for rule in self.rules:
            if rule["category"].base_confidence < self.threshold:
                continue    # the R2 gate: a detector below threshold never emits

            # document-level detectors: these cannot work sentence by sentence, because
            # the signal is a pattern across the whole document
            if rule["kind"] == "repetition":
                spans.extend(self._scan_repetition(doc, rule))
            elif rule["kind"] == "entity_blame":
                spans.extend(self._scan_entity_blame(doc, rule))
            elif rule["kind"] == "entity_sentiment_split":
                spans.extend(self._scan_entity_sentiment_split(doc, rule))
            else:
                for sentence in doc.sentences:
                    spans.extend(self._scan_sentence(doc, sentence, rule))

        # canonical order, so two runs over the same document produce identical output
        spans.sort(key=lambda s: (s.start_char, s.end_char, s.rule_id))
        return RuleClassificationResult(document_id=doc.document_id, spans=spans)
