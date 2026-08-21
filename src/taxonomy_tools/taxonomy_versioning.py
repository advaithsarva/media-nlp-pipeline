#Handles version IDs, diffs between versions (v1 vs v2), migration logic. Great for long-term evolution.
from typing import Dict,Any
def diff_taxonomies(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Return added/removed/changed nodes."""
    # compare node id sets


def plan_migration(diff: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest how to map old labels to new ones."""
    # simple example: for removed nodes, map to parent
