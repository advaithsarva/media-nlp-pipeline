#ONNX-optimized embedding model (SentenceTransformers / MiniLM). Best for fast CPU embeddings.
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from typing import Dict, Any
class EmbeddingGenerator:
    def __init__(self, emb_cfg: Dict[str, Any]):
        pass
    def embed(text_or_segments:str)->"np.ndarry":
        pass