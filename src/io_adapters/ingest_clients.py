class ESClient:
    def receive(hit_dict):
        pass
    def fetch(query_config):
        pass
class APIClient:
    def receive(json_payload):
        pass
    def fetch(request_config):
        pass
class S3Client:
    def receive(s3_event):
        pass
    def fetch(s3_config):
        pass
class KafkaClient:
    def receive(message):
        pass
    def fetch(consumer_config):
        pass
class ScraperClient:
    def receive(html_content):
        pass
    def fetch(scrape_config):
        pass 
class RedisClient:
    def receive(key_value):
        pass
    def fetch(redis_config):
        pass
