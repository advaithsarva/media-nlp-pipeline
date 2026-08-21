#ML-based classifier (scikit-learn, etc.) as an optional component.
import numpy as np
import joblib
import onnxruntime as ort

from typing import Dict, Any
class MLClassifier:
    def __init__(self,model_path,label_map):
        pass
    def _features_to_vector(self,feature_bundle:Dict[str,Any])->np.ndarray:
        pass
    def predict(self,feature_bundle:Dict[str,Any],sentences):
        pass