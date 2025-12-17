from typing import Dict,Any,Iterable,List
from io_adapters.file_readers import *
from io_adapters.ingest_clients import *
from data_schema.input_schema import validate_input_payload
class InputRouter:
    def __init__(self,input_config:Dict[str,Any]):
        self.config=input_config
        #file readers
        self.pdf_reader=PDFReader()
        self.docx_reader=DocsReader()
        self.ppt_reader=PPTReader()
        self.txt_reader=TxtReader()
        self.json_reader=JSONReader(input_config.get('json',{}))
        self.csv_reader=CSVReader(input_config.get('csv',{}))
        
        #client readers
        self.api_client=APIClient(input_config.get("api",{}))
        self.es_client=ESClient(input_config.get('es',{}))
        self.kafka_client=KafkaClient(input_config.get('kafka',{}))
        self.s3_client=S3Client(input_config.get('s3',{}))
        self.scrapper_client=ScraperClient(input_config.get('scrape',{}))
        self.redis_client=RedisClient(input_config.get('redis',{}))

    def _route_file(self,file_name:str,file_bytes:bytes,mime_type:str):
        pass
    def _route_push_api(self,payload: Dict[str:Any]):
        return self.api_client.receive(payload)
    def _route_push_es(self,hit_dict:Dict[str,Any]):
        return self.es_client.receive(hit_dict)
    def to_internal_documents(self,raw_input_obj:Dict[str,Any]):
        pass
    def iter_souce_batches(self)-> Iterable[List[Dict[str,Any]]]:
        pass
