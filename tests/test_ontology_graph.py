"""OntologyGraph must reflect exactly the family/category hierarchy in
conf/taxonomy_v1.yaml -- no more structure than the config actually has."""

import pytest

from nlp_pipeline.ontology_graph import OntologyGraph


@pytest.fixture(scope="module")
def ontology(taxonomy):
    return OntologyGraph(taxonomy)


def test_every_category_reachable_from_root(ontology, taxonomy):
    assert ontology.categories() == sorted(taxonomy.ids())


def test_families_match_taxonomy(ontology, taxonomy):
    assert ontology.families() == sorted(taxonomy.families())


def test_ancestors_of_a_category_are_its_family_then_root(ontology, taxonomy):
    for category in taxonomy.categories:
        ancestors = ontology.get_ancestors(category.id)
        assert ancestors == [category.family, "taxonomy"]


def test_get_family_matches_config(ontology, taxonomy):
    for category in taxonomy.categories:
        assert ontology.get_family(category.id) == category.family


def test_descendants_of_a_family_are_exactly_its_categories(ontology, taxonomy):
    for family, category_ids in taxonomy.families().items():
        assert ontology.get_descendants(family) == sorted(category_ids)


def test_unknown_node_raises(ontology):
    with pytest.raises(KeyError):
        ontology.get_ancestors("not_a_real_node")
    with pytest.raises(KeyError):
        ontology.get_descendants("not_a_real_node")


def test_project_labels_to_levels(ontology):
    projection = ontology.project_labels_to_levels(["loaded_language", "bandwagon"])
    assert projection["category"] == ["bandwagon", "loaded_language"]
    assert projection["family"] == ["fallacy", "propaganda"]


def test_project_labels_rejects_unknown_category(ontology):
    with pytest.raises(KeyError):
        ontology.project_labels_to_levels(["loaded_language", "not_real"])


def test_validate_label_set(ontology):
    assert ontology.validate_label_set(["loaded_language", "bandwagon"]) is True
    assert ontology.validate_label_set(["loaded_language", "not_real"]) is False
    assert ontology.validate_label_set([]) is True
