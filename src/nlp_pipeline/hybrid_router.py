#Combines rule-based + ML-based methods: priority rules, fallbacks, tie-breaking logic.
from typing import Dict, Any

from nlp_pipeline.ontology_graph import OntologyGraph
class HybridRouter:
    def __init__(self,hybrid_config:Dict[str,Any],ontology_graph:OntologyGraph):
        pass
    def merge(self,rule_result,ml_result,ontology:OntologyGraph):
        pass