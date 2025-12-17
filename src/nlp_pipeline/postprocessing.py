# Builds final output JSON, attaches spans/offsets, enforces output_schema.json.
import json
from typing import Dict, Any, List
import jsonschema
class PostProcessor:
    def __init__(self,output_schema,taxonomy_version,pipeline_version):
        pass
    def to_output_schema(original_doc,normalized_doc,segments,final_classifciation,scores):
        pass