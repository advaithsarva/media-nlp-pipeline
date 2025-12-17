'''Intended: Spark-based cleaning/normalization for VERY large corpora (TB-level).
Reads from S3/Parquet → runs preprocessing → saves clean Parquet.'''
from pyspark import SparkSession
from main import load_configs
from io_adapters.input_router import InputRouter
from nlp_pipeline.preprocessing import TextProcessor
from nlp_pipeline.segmentation import SentenceSegmenter
from nlp_pipeline.features import FeatureExtractor

def spark_preprocess():
    pass
