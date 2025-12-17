'''Intended: Ray-based distributed preprocessing on CPU, lighter than Spark.
Good for “medium-big” but not full cluster environments.'''
import ray
from main import load_configs
from io_adapters.input_router import InputRouter
from nlp_pipeline.preprocessing import TextProcessor
from nlp_pipeline.segmentation import SentenceSegmenter
from nlp_pipeline.features import FeatureExtractor
from io_adapters.storage_clients import StorageClientFactory


@ray.remote
def process_single_remote(raw_input_obj,pipeline_cfg,feature_cfg):
    pass

def ray_preprocess():
    ray.init()



    ray.shutdown()
