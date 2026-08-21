"""Shared setup for the test suite.

Puts src/ on the import path so tests can `from nlp_pipeline import ...` without the
package being installed, and builds the pipeline objects once instead of per test.
"""

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nlp_pipeline.preprocessing import TextProcessor          # noqa: E402
from nlp_pipeline.segmentation import SentenceSegmenter       # noqa: E402
from nlp_pipeline.rules_engine import RuleEngine              # noqa: E402
from nlp_pipeline.scoring_engine import ScoringEngine         # noqa: E402
from nlp_pipeline.shared_types import NormalizedDocument      # noqa: E402
from taxonomy_tools.taxonomy_loader import load_taxonomy      # noqa: E402


# A dry, factual paragraph. Nothing in it is manipulative, so no detector may fire on it.
# This is the false-positive guard: a detector that lights up here is not shippable.
NEUTRAL_TEXT = (
    "The Forth Bridge is a cantilever railway bridge across the Firth of Forth in the "
    "east of Scotland. Construction began in 1882 and the bridge opened on 4 March 1890. "
    "It carries about 190 trains each day and was designated a UNESCO World Heritage Site "
    "in 2015. The structure is 2,467 metres long and used approximately 54,000 tonnes of "
    "steel. Network Rail has maintained the bridge since 2002, and a repainting programme "
    "completed in 2011 is expected to last around 25 years. All of the original rivets "
    "were driven by hand."
)

# Every category in the taxonomy has at least one example here, so a broken detector
# shows up as a failure rather than as silence.
LOADED_TEXT = (
    "Everyone knows the scheme was disastrous. Sources say the minister lied, and the "
    "mayor is a liar who made a shameful excuse. Studies show that every single claim "
    "was ludicrous."
)

# One example per category, used to prove each detector can actually fire. Written as
# separate snippets rather than one paragraph because several detectors need a specific
# sentence shape, and a shared paragraph makes it unclear which text triggered what.
CATEGORY_EXAMPLES = {
    "loaded_language": "The policy was a disastrous and shameful retreat.",
    "name_calling": "The minister is a liar and a charlatan.",
    "glittering_generalities": "Freedom, justice and prosperity for every family!",
    "appeal_to_fear": "This is an existential threat and we face annihilation.",
    "whataboutism": "The audit found errors. What about the previous administration?",
    "thought_terminating_cliche": "The scheme failed. It is what it is.",
    "gaslighting": "You are imagining things and that never happened.",
    "guilt_by_association": "The group has ties to terrorists, he argued.",
    "bandwagon": "Everyone knows the plan will work.",
    "false_dilemma": "There is no other choice; we have no choice but to sign.",
    "no_true_scotsman": "No true patriot would question the budget.",
    "burden_of_proof": "No one has ever proven the claim false, so prove me wrong.",
    "motive_fallacy": "He only says this because he has a vested interest in the outcome.",
    "slippery_slope": "This will inevitably lead to chaos and opens the floodgates.",
    "anecdotal_evidence": "A friend of mine lost their job, which proves the policy failed.",
    "unsupported_quantifier": "Many people are unhappy and every single voter agrees.",
    "appeal_to_authority": "Experts say the measure is safe and research shows it works.",
    "source_opaqueness": "Sources say the deal is done, and critics claim otherwise.",
    "statistical_manipulation": "Support surged by 300% and hit a record high.",
    "hedging": "The change may possibly reduce costs, which suggests a saving.",
    "repetition": (
        "We will take back control. The plan is sound. We will take back control of the "
        "borders. Critics disagree. We will take back control, he said again."
    ),
}


@pytest.fixture(scope="session")
def configs():
    conf = ROOT / "conf"
    with open(conf / "pipeline_v1.yaml", encoding="utf-8") as f:
        pipeline = yaml.safe_load(f)
    with open(conf / "taxonomy_v1.yaml", encoding="utf-8") as f:
        taxonomy = yaml.safe_load(f)
    with open(conf / "scoring_v1.yaml", encoding="utf-8") as f:
        scoring = yaml.safe_load(f)
    return pipeline, taxonomy, scoring


@pytest.fixture(scope="session")
def taxonomy(configs):
    return load_taxonomy(configs[1])


@pytest.fixture(scope="session")
def engine(taxonomy):
    return RuleEngine(taxonomy)


@pytest.fixture(scope="session")
def scorer(configs, taxonomy):
    return ScoringEngine(configs[2], taxonomy)


@pytest.fixture(scope="session")
def build_doc():
    """Text in, a segmented and tokenised NormalizedDocument out."""
    processor = TextProcessor()
    segmenter = SentenceSegmenter()

    def _build(text, document_id="test"):
        doc = NormalizedDocument(
            document_id=document_id,
            text=text,
            tokens=processor._tokenize(text),
        )
        segmenter.segment(doc)
        return doc

    return _build
