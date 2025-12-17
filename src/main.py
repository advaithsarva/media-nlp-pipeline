import os
from pathlib import Path
import logging
import argparse
import json
import yaml
import jsonschema

from io_adapters.input_router import InputRouter
from io_adapters.storage_clients import StorageClientFactory
from taxonomy_tools.taxonomy_loader import load_taxonomy
from nlp_pipeline.preprocessing import TextProcessor
from nlp_pipeline.segmentation import SentenceSegmenter
from nlp_pipeline.features import FeatureExtractor
from nlp_pipeline.rules_engine import RuleEngine
from nlp_pipeline.ml_classifier import MLClassifier
from nlp_pipeline.hybrid_router import HybridRouter
from nlp_pipeline.ontology_graph import OntologyGraph
from nlp_pipeline.scoring_engine import ScoringEngine
from nlp_pipeline.postprocessing import PostProcessor
from nlp_pipeline.embeddings_onnx import EmbeddingGenerator
from nlp_pipeline.vector_index import VectorIndex
from nlp_pipeline.deterministic_utils import (set_global_seeds,compute_config_hashes)
def load_yaml(path:str)->dict:
    with open(path,"r") as yaml_file:
        yaml_data=yaml.safe_load(yaml_file)
    return yaml_data
def load_configs():
    pipeline_conf=load_yaml("C:\Projects\NLPpipline\conf\pipeline_v1.yaml")
    taxonomy_conf=load_yaml("C:\Projects\NLPpipline\conf\taxonomy_v1.yaml")
    scoring_conf=load_yaml("C:\Projects\NLPpipline\conf\scoring_v1.yaml")
    return pipeline_conf,taxonomy_conf,scoring_conf
def build_services(load_configs,pipeline_conf,taxonomy_conf,scoring_conf):
    set_global_seeds(pipeline_conf["pipeline"]["seed"])
    taxonomy=load_taxonomy(taxonomy_conf)
    ontology=OntologyGraph(taxonomy)
    input_router=InputRouter(pipeline_conf["input"])
    storage_client=StorageClientFactory.create(pipeline_conf["output"])

def process_document(context,raw_input):
    pass
def run_pipeline():
    pass

if __name__=="__main__":
    pass