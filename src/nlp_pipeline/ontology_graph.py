"""Graph representation of the taxonomy: families, categories, and how they relate.

The taxonomy in `conf/taxonomy_v1.yaml` is already a two-level hierarchy -- every
category names a `family` (fallacy, propaganda, bias, style) -- so the graph built here
is exactly that hierarchy made queryable, plus one synthetic root above the families.
Nothing here invents structure the config does not already have.

    taxonomy
    ├── fallacy
    │   ├── bandwagon
    │   ├── false_dilemma
    │   └── ...
    ├── propaganda
    │   ├── loaded_language
    │   └── ...
    ├── bias
    └── style

This is what lets a label produced at the category level ("loaded_language") be rolled
up to the level a consumer actually wants ("propaganda"), and what lets a proposed label
be checked against the real taxonomy before anything downstream trusts it.

A plain dict-of-lists would do the ancestors/descendants queries just as well for a graph
this shallow; networkx is used anyway because it is the dependency the rest of the project
already declares for this job (see `requirements-dev.txt` and the architecture diagram in
README.md), and because `project_labels_to_levels` and `validate_label_set` read more
plainly as graph queries than as one-off dict walks.
"""

from typing import Any, Dict, Iterable, List, Set

import networkx as nx

ROOT = "taxonomy"


class OntologyGraph:
    def __init__(self, taxonomy_config: Dict[str, Any]):
        """`taxonomy_config` is a loaded `Taxonomy` (see taxonomy_tools.taxonomy_loader) --
        anything with `.categories` (each carrying `.id` and `.family`) works."""
        self.taxonomy = taxonomy_config
        self.graph = nx.DiGraph()
        self._build()

    # ---------- construction ----------

    def _build(self):
        self.graph.add_node(ROOT, level="root")

        families = {}
        for category in self.taxonomy.categories:
            families.setdefault(category.family, []).append(category)

        # sorted: family and category order must not depend on dict iteration order,
        # or two runs over the same taxonomy could disagree on it
        for family in sorted(families):
            self.graph.add_node(family, level="family")
            self.graph.add_edge(ROOT, family)
            for category in sorted(families[family], key=lambda c: c.id):
                self.graph.add_node(category.id, level="category", family=family)
                self.graph.add_edge(family, category.id)

    # ---------- lookups ----------

    def _require_node(self, node_id: str):
        if node_id not in self.graph:
            raise KeyError("no such taxonomy node: " + repr(node_id))

    def get_ancestors(self, node_id: str) -> List[str]:
        """Nearest ancestor first: a category returns [family, 'taxonomy']."""
        self._require_node(node_id)
        ancestors = nx.ancestors(self.graph, node_id)
        # order by distance from node_id, nearest first; ties broken by name so the
        # result is stable
        distances = nx.shortest_path_length(self.graph.reverse(copy=False), node_id)
        return sorted(ancestors, key=lambda n: (distances[n], n))

    def get_descendants(self, node_id: str) -> List[str]:
        """All nodes reachable below `node_id`, sorted for a stable result."""
        self._require_node(node_id)
        return sorted(nx.descendants(self.graph, node_id))

    def get_family(self, category_id: str) -> str:
        """The one family a category belongs to. Convenience wrapper over get_ancestors
        for the common case of "which family is this category in"."""
        self._require_node(category_id)
        if self.graph.nodes[category_id].get("level") != "category":
            raise KeyError(category_id + " is not a category node")
        return next(iter(self.graph.predecessors(category_id)))

    def families(self) -> List[str]:
        return sorted(n for n, d in self.graph.nodes(data=True) if d.get("level") == "family")

    def categories(self) -> List[str]:
        return sorted(n for n, d in self.graph.nodes(data=True) if d.get("level") == "category")

    # ---------- label operations ----------

    def project_labels_to_levels(self, label_set: Iterable[str]) -> Dict[str, List[str]]:
        """Roll a set of category labels up to every level above them.

        Returns {"category": [...], "family": [...]}, both sorted and de-duplicated.
        Used by consumers that want "which families of manipulation are present" without
        caring about the individual technique -- e.g. a dashboard summary.
        """
        labels = set(label_set)
        unknown = labels - set(self.categories())
        if unknown:
            raise KeyError("not a category label: " + ", ".join(sorted(unknown)))

        families: Set[str] = set()
        for label in labels:
            families.add(self.get_family(label))

        return {
            "category": sorted(labels),
            "family": sorted(families),
        }

    def validate_label_set(self, label_set: Iterable[str]) -> bool:
        """True only when every label in the set is a real category in this taxonomy.

        Used before trusting a label that came from outside the rule engine -- an ML
        prediction or a taxonomy-suggestion proposal -- so a typo'd or stale label fails
        loudly here instead of silently producing an empty score downstream.
        """
        known = set(self.categories())
        return set(label_set) <= known
