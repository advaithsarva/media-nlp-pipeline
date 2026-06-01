import requests
from elasticsearch import Elasticsearch
import boto3
from kafka import KafkaConsumer
import redis
from bs4 import BeautifulSoup 
from typing import Dict,Any,Iterable,List
from io_adapters.shared_types import InternalDocument
class APIClient:
    def __init__(self,config:Dict[str,Any]):
        pass
    def receive(self,json_payload:Dict[str,Any])-> InternalDocument:
        pass
    def fetch(self,request_config:Dict[str,Any])-> Iterable[InternalDocument]:
        pass
class ESClient:
    def __init__(self,config:Dict[str,Any]):
        pass
    def receive(self,hit_dict: Dict[str,Any])-> InternalDocument:
        pass
    def fetch(self,query_config:Dict[str,Any])->Iterable[InternalDocument]:
        pass

class S3Client:
    def __init__(self,config:Dict[str,Any]):
        pass
    def receive(self,s3_event:Dict[str,Any])-> InternalDocument:
        pass
    def fetch(self,s3_config,_ignored)->Iterable[InternalDocument]:
        pass
class KafkaClient:
    def __init__(self,config:Dict[str,Any]):
        pass
    def receive(self,message:Dict[str,Any])-> InternalDocument:
        pass
    def fetch(self,consumer_config,_ignored)-> Iterable[InternalDocument]:
        pass
class ScraperClient:
    def __init__(self,config:Dict[str,Any]):
        pass
    def receive(self,html_content:Dict[str,Any])-> InternalDocument:
        pass
    def fetch(self, urls_config: Dict[str, Any]) -> Iterable[InternalDocument]:
        pass 
class RedisClient:
    def __init__(self, config: Dict[str, Any]):
        pass
    def receive(self,key_value:Dict[str,Any])-> InternalDocument:
        pass
    def fetch(self, _ignored) -> Iterable[InternalDocument]:
        pass


