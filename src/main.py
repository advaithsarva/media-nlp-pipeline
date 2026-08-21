"""Entry point. Wires the stages together and runs a document through them.

    python src/main.py --input data/raw/sample_article.txt

Nothing in here contains analysis logic -- it loads config, builds the stages once, and
passes the document along. If you want to know what a stage does, read that stage.

The stages, in order:
    InputRouter        file or string  -> InternalDocument
    TextProcessor      InternalDocument -> NormalizedDocument (tokens attached)
    SentenceSegmenter  adds sentences with exact character offsets
    RuleEngine         finds evidence spans
    ScoringEngine      turns spans into one score per category
    PostProcessor      builds the JSON record and checks it against the schema
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONF_DIR = ROOT / "conf"
# Allows "python src/main.py" to work without installing the package first.
sys.path.insert(0, str(ROOT / "src"))

from io_adapters.input_router import InputRouter                    # noqa: E402
from taxonomy_tools.taxonomy_loader import load_taxonomy            # noqa: E402
from nlp_pipeline.preprocessing import TextProcessor                # noqa: E402
from nlp_pipeline.segmentation import SentenceSegmenter             # noqa: E402
from nlp_pipeline.rules_engine import RuleEngine                    # noqa: E402
from nlp_pipeline.scoring_engine import ScoringEngine               # noqa: E402
from nlp_pipeline.postprocessing import PostProcessor               # noqa: E402
from nlp_pipeline.deterministic_utils import (                      # noqa: E402
    _set_global_seeds,
    _compute_config_hashes,
)


def load_yaml(path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_configs(conf_dir=CONF_DIR):
    conf_dir = Path(conf_dir)
    pipeline_conf = load_yaml(conf_dir / "pipeline_v1.yaml")
    taxonomy_conf = load_yaml(conf_dir / "taxonomy_v1.yaml")
    scoring_conf = load_yaml(conf_dir / "scoring_v1.yaml")
    return pipeline_conf, taxonomy_conf, scoring_conf


class PipelineRunner:
    """Holds the stages. Built once, then reused for every document."""

    def __init__(self, conf_dir=CONF_DIR):
        self.pipeline_conf, self.taxonomy_conf, self.scoring_conf = load_configs(conf_dir)

        seed = self.pipeline_conf.get("pipeline", {}).get("seed")
        if seed is None:
            raise ValueError("pipeline.seed is missing from pipeline_v1.yaml")
        _set_global_seeds(seed)

        # Stamped onto every output so a result can be traced back to the exact
        # configuration that produced it.
        self.config_hashes = _compute_config_hashes(
            self.pipeline_conf, self.taxonomy_conf, self.scoring_conf
        )

        self.taxonomy = load_taxonomy(self.taxonomy_conf)
        self.router = InputRouter(self.pipeline_conf.get("input", {}))
        self.processor = TextProcessor(self.pipeline_conf.get("pipeline", {}))
        self.segmenter = SentenceSegmenter(self.pipeline_conf.get("segmentation", {}))
        self.rules = RuleEngine(self.taxonomy)
        self.scorer = ScoringEngine(self.scoring_conf, self.taxonomy)
        self.postprocessor = PostProcessor()

    def process_document(self, raw_input) -> dict:
        document = self.router.route_push_input(raw_input)
        normalized = self.processor.normalize(document)
        self.segmenter.segment(normalized)
        result = self.rules.classify(normalized)
        scored = self.scorer.score(result, normalized)

        record = self.postprocessor.build_output(scored, normalized, self.config_hashes)
        self.postprocessor.validate(record)
        # Belt and braces: read every quote back out of the article itself. This is the
        # one claim the whole project rests on, so it is checked rather than trusted.
        self.postprocessor.check_evidence(record, normalized.text)
        return record

    def run_pipeline(self):
        """Process everything the configured pull source offers."""
        return [self.process_document(doc) for doc in self.router.route_pull_source()]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the NLP pipeline on one document.")
    parser.add_argument("--input", help="path to a file, or a quoted string of text")
    parser.add_argument("--out", help="write the JSON here instead of to the screen")
    parser.add_argument("--conf", default=str(CONF_DIR), help="config directory")
    args = parser.parse_args(argv)

    runner = PipelineRunner(args.conf)

    if args.input:
        records = [runner.process_document(args.input)]
    else:
        records = runner.run_pipeline()

    output = json.dumps(
        records[0] if len(records) == 1 else records,
        ensure_ascii=False, indent=2, sort_keys=True,
    )

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output + "\n", encoding="utf-8")
        print("wrote " + args.out)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
