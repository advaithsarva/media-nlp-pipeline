"""Turns evidence spans into numbers.

The rule that shapes this module: a score may only depend on evidence that was actually
quoted. Nothing here looks at the text again -- it sees the spans and the config, and
nothing else. That is what makes every number reconstructible: anyone holding the output
can recompute it by hand from the findings list and get the same answer.

The formulas come from the original system design, implemented rather than reinvented:

  1  score_article = sum( w_c * s_c )              per-category weighted sum
  2  conf = alpha*rules + (1-alpha)*ml             alpha is 1.0; there is no ML yet
  3  s_i = c_i * w_f ; disruption = max(s_i*d_f)   severity and logical-flow disruption
  4  PropScore                                     noisy-OR, or the corrected smooth-max
  5  factuality                                    not computed: needs claim verification

One deliberate departure. Formula 4 is a noisy-OR, which assumes the propaganda techniques
are statistically independent. They are not, so it saturates towards 1 on ordinary emotive
writing. Both aggregators are implemented and `prop_score_method` chooses; the default is
the corrected one, and the other is kept so the two can be compared on real documents.

Every composite is returned with the breakdown that produced it. A number without its
working is not auditable, and auditability is the point of the project.
"""

import math

from nlp_pipeline.shared_types import CategoryScore, ScoredDocument


class ScoringEngine:
    def __init__(self, scoring_conf, taxonomy):
        conf = scoring_conf.get("scoring", {})
        self.lam = float(conf.get("lambda", 4.0))
        self.beta = float(conf.get("beta", 0.5))
        self.round_places = int(conf.get("round_places", 6))
        self.expose_composite = bool(conf.get("expose_composite", False))
        self.prop_score_method = conf.get("prop_score_method", "smooth_max")
        self.gamma = float(conf.get("prop_score_gamma", 4.0))
        self.alpha = float(conf.get("alpha", 1.0))
        self.frequency_alpha = float(conf.get("frequency_alpha", 0.3))

        self.weights = scoring_conf.get("category_weights", {}) or {}
        self.increments = scoring_conf.get("additive_increments", {}) or {}
        self.families = scoring_conf.get("composite_families", {}) or {}
        self.bands = scoring_conf.get("bands", {}) or {}
        self.taxonomy = taxonomy

    # ---------- helpers ----------

    def _round(self, value):
        return round(value, self.round_places)

    def _hybrid_confidence(self, rule_confidence, ml_confidence=None):
        """Formula 2. With no ML classifier, alpha is 1.0 and this returns the rule score."""
        if ml_confidence is None or self.alpha >= 1.0:
            return rule_confidence
        return self.alpha * rule_confidence + (1.0 - self.alpha) * ml_confidence

    def _saturate(self, raw, word_count):
        """The per-category score: evidence, normalised by length, squashed into 0..1."""
        if raw <= 0:
            return 0.0
        # max(...,1) guards against dividing by zero on an empty document
        density = raw / (max(word_count, 1) ** self.beta)
        return 1.0 - math.exp(-self.lam * density)

    def _band(self, value):
        if value < float(self.bands.get("low", 0.3)):
            return "low"
        if value < float(self.bands.get("moderate", 0.7)):
            return "moderate"
        return "high"

    def _category_ids_for(self, composite_name):
        wanted = self.families.get(composite_name, [])
        return [c.id for c in self.taxonomy.categories if c.family in wanted]

    # ---------- per category ----------

    def _score_categories(self, result, word_count):
        scores = {}
        # every category gets an entry, including ones that found nothing: a stable output
        # shape is far easier to validate, diff and store than one whose keys vary
        for cat in self.taxonomy.categories:
            spans = result.spans_for(cat.id)
            weight = float(self.weights.get(cat.id, 1.0))
            raw = sum(self._hybrid_confidence(s.confidence) for s in spans) * weight
            scores[cat.id] = CategoryScore(
                category=cat.id,
                count=len(spans),
                raw=self._round(raw),
                score=self._round(self._saturate(raw, word_count)),
                calibrated=False,
            )
        return scores

    # ---------- severity and coherence (formula 3) ----------

    def _severity(self, result):
        """s_i = c_i * w_f per instance; severity_f = 1 - exp(-n_f) per type."""
        per_category = {}
        worst_disruption = 0.0
        worst_source = None

        for cat in self.taxonomy.categories:
            spans = result.spans_for(cat.id)
            if not spans:
                continue

            instance_severities = [s.confidence * cat.severity_weight for s in spans]
            # document-level accumulation: five ad hominems are a more systematically
            # fallacious argument than one, but not five times worse
            accumulated = 1.0 - math.exp(-len(spans))

            per_category[cat.id] = {
                "instances": len(spans),
                "max_instance_severity": self._round(max(instance_severities)),
                "accumulated_severity": self._round(accumulated),
                "severity_weight": cat.severity_weight,
            }

            disruption = max(instance_severities) * cat.disruption
            if disruption > worst_disruption:
                worst_disruption = disruption
                worst_source = cat.id

        return {
            "per_category": per_category,
            "logical_flow_disruption": self._round(worst_disruption),
            "disruption_driven_by": worst_source,
            "coherence": self._round(1.0 - worst_disruption),
        }

    # ---------- composites ----------

    def _prop_score(self, category_scores):
        """Formula 4, both ways. Returns the value and everything needed to check it."""
        ids = self._category_ids_for("prop_score")
        values = [category_scores[i].score for i in ids if i in category_scores]
        present = [v for v in values if v > 0]

        if not present:
            value = 0.0
        elif self.prop_score_method == "noisy_or":
            product = 1.0
            for v in present:
                product *= (1.0 - v)
            value = 1.0 - product
        else:
            # smooth-max: log-mean-exp. Averages when gamma is small, approaches the
            # maximum as gamma grows, and never compounds correlated evidence the way a
            # product does.
            total = sum(math.exp(self.gamma * v) for v in present)
            value = math.log(total / len(present)) / self.gamma

        return {
            "value": self._round(min(max(value, 0.0), 1.0)),
            "method": self.prop_score_method,
            "gamma": self.gamma if self.prop_score_method == "smooth_max" else None,
            "inputs": {i: category_scores[i].score for i in ids if i in category_scores},
        }

    def _additive_manipulation(self, category_scores):
        """A fixed amount per signal present, clipped at 1.0.

        The least clever composite here and by some way the most defensible, because the
        total is literally the sum of a list the reader can see.
        """
        excluded = set()
        for family in self.families.get("excluded", []):
            excluded.update(c.id for c in self.taxonomy.categories if c.family == family)

        breakdown = {}
        for category, score in sorted(category_scores.items()):
            if score.count == 0 or category in excluded:
                continue
            breakdown[category] = float(self.increments.get(category, 0.1))

        total = min(sum(breakdown.values()), 1.0)
        return {
            "value": self._round(total),
            "band": self._band(total),
            "breakdown": {k: self._round(v) for k, v in breakdown.items()},
            "clipped": sum(breakdown.values()) > 1.0,
        }

    def _family_score(self, category_scores, composite_name):
        """Mean score across one family, with the members listed."""
        ids = self._category_ids_for(composite_name)
        values = [category_scores[i].score for i in ids if i in category_scores]
        value = sum(values) / len(values) if values else 0.0
        return {
            "value": self._round(value),
            "inputs": {i: category_scores[i].score for i in ids if i in category_scores},
        }

    def _composites(self, category_scores, severity):
        prop = self._prop_score(category_scores)
        fallacy = self._family_score(category_scores, "fallacy_score")
        bias = self._family_score(category_scores, "bias_signal")
        additive = self._additive_manipulation(category_scores)

        # ManipulationIndex. Three inputs, so the independence problem is far milder
        # than with thirteen -- but it is still a noisy-OR, so it is labelled as such.
        parts = [prop["value"], fallacy["value"], bias["value"]]
        product = 1.0
        for p in parts:
            product *= (1.0 - p)
        manipulation = 1.0 - product

        # article-level weighted sum, normalised by the weights used
        weight_total = sum(float(self.weights.get(c.id, 1.0)) for c in self.taxonomy.categories)
        article = sum(
            float(self.weights.get(c.id, 1.0)) * category_scores[c.id].score
            for c in self.taxonomy.categories if c.id in category_scores
        )
        article = article / weight_total if weight_total else 0.0

        return {
            "calibrated": False,
            "warning": (
                "Uncalibrated. No labelled evaluation set has been used, so these weights "
                "are informed guesses rather than fitted values. Read the breakdowns, "
                "not the totals."
            ),
            "prop_score": prop,
            "fallacy_score": fallacy,
            "bias_signal": bias,
            "additive_manipulation": additive,
            "manipulation_index": {
                "value": self._round(manipulation),
                "method": "noisy_or",
                "inputs": {"prop_score": prop["value"],
                           "fallacy_score": fallacy["value"],
                           "bias_signal": bias["value"]},
            },
            "article_score": {
                "value": self._round(article),
                "method": "weighted_mean_of_category_scores",
            },
            "logical_flow_disruption": severity["logical_flow_disruption"],
            "coherence": severity["coherence"],
        }

    # ---------- entry point ----------

    def score(self, result, doc) -> ScoredDocument:
        category_scores = self._score_categories(result, doc.word_count)
        severity = self._severity(result)
        composites = self._composites(category_scores, severity)

        return ScoredDocument(
            document_id=result.document_id,
            spans=result.spans,
            category_scores=category_scores,
            # The single headline number reaches the output only when explicitly enabled.
            composite=composites["additive_manipulation"]["value"] if self.expose_composite else None,
            severity=severity,
            composites=composites,
        )
