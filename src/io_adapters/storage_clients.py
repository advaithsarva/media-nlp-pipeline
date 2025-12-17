import json
from pathlib import Path
import pandas as pd
import redis
from typing import Dict,Any,List

class ParquetWriter:
    def __init__(self,config:Dict[str,Any]):
        pass
    def write(self,document):
        pass
    def save_batch(documents):
        pass

class RedisWriter:
    def write(document):
        pass
    def save_batch(documents):
        pass

class LocalStorageWriter:
    def __init__(self,config:Dict[str,Any]):
        pass
    def write(self,document:Dict[str,Any]):
        pass
    def save_batch(documents):
        pass
class StorageClientFactory:
    pass


