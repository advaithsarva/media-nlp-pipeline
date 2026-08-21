#Suggest new taxonomy nodes based on clustering/embeddings/co-occurrence. Good for future "active learning" features.
from typing import Dict,Any
def suggest_new_nodes(embeddings, existing_taxonomy) -> Dict[str, Any]:
    """Cluster unlabeled embeddings and suggest new topics."""
    # cluster embeddings (k-means)
    # for clusters not matching current taxonomy, propose new labels
