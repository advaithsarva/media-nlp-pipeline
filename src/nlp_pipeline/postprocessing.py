"""Builds the final JSON record and checks it against data_schema/output_schema.json.

Validating our own output sounds redundant, but it is what stops a quiet change in one
of the earlier stages from reaching the backend as a differently-shaped record. If the
shape changes, this raises here rather than breaking someone else's code later.

There is no timestamp anywhere in the record. That is on purpose: the pipeline promises
that the same article produces the same bytes every run, and a clock reading would break
that promise on the first run.
"""

import json
from pathlib import Path

import jsonschema

from nlp_pipeline.deterministic_utils import _round_floats

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "data_schema" / "output_schema.json"
SCHEMA_VERSION = "1.0.0"


class PostProcessor:
    def __init__(self, schema_path=None):
        self.schema_path = Path(schema_path) if schema_path else SCHEMA_PATH
        with open(self.schema_path, encoding="utf-8") as f:
            self.schema = json.load(f)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    def build_output(self, scored, doc, config_hashes) -> dict:
        findings = [{
            "category": s.category,
            "rule_id": s.rule_id,
            "sentence_id": s.sentence_id,
            "text": s.text,
            "start_char": s.start_char,
            "end_char": s.end_char,
            "confidence": s.confidence,
        } for s in scored.spans]

        record = {
            "schema_version": SCHEMA_VERSION,
            "document_id": scored.document_id,
            "source": {
                "type": doc.metadata.get("source_type", "unknown"),
                "title": doc.metadata.get("title"),
                "author": doc.metadata.get("author"),
                "language": doc.language,
            },
            "config_hashes": config_hashes,
            "stats": {
                "char_count": len(doc.text),
                "word_count": doc.word_count,
                "sentence_count": len(doc.sentences),
            },
            "findings": findings,
            # sorted keys so the record serialises the same way every run
            "category_scores": {
                cat: {
                    "count": cs.count,
                    "raw": cs.raw,
                    "score": cs.score,
                    "calibrated": cs.calibrated,
                }
                for cat, cs in sorted(scored.category_scores.items())
            },
            "composite": scored.composite,
            "notes": [
                "Scores are uncalibrated: no labelled evaluation set has been used yet.",
                "Every finding is a verbatim substring of the source text at [start_char, end_char).",
            ],
        }
        return _round_floats(record)

    def validate(self, record: dict):
        """Raise on the first schema violation, with the path to the offending field."""
        errors = sorted(self.validator.iter_errors(record), key=lambda e: list(e.path))
        if errors:
            first = errors[0]
            location = "/".join(str(p) for p in first.path) or "(root)"
            raise ValueError(f"output failed schema check at {location}: {first.message}")

    def to_json(self, record: dict) -> str:
        # sort_keys and a fixed separator: this is the string the determinism test compares
        return json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True)

    def check_evidence(self, record: dict, text: str):
        """Re-read every quote out of the article. This is the promise the project is built on."""
        for f in record["findings"]:
            actual = text[f["start_char"]:f["end_char"]]
            if actual != f["text"]:
                raise ValueError(
                    f"evidence does not match the source text at {f['start_char']}: "
                    f"reported {f['text']!r}, text says {actual!r}"
                )
