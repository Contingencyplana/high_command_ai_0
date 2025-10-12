from tools.forge.selector import build_predicate, filter_records


def test_empty_selector_matches_all():
    predicate = build_predicate("")
    assert predicate.test({})


def test_simple_equality():
    predicate = build_predicate("realm:Dayland")
    assert predicate.test({"realm": "Dayland"})
    assert not predicate.test({"realm": "Nightland"})


def test_numeric_comparison():
    predicate = build_predicate("entropy>=0.5")
    assert predicate.test({"entropy": 0.6})
    assert not predicate.test({"entropy": 0.4})


def test_and_or_logic():
    records = [
        {"realm": "Dayland", "entropy": 0.3},
        {"realm": "Nightland", "entropy": 0.7},
        {"realm": "Dayland", "entropy": 0.8},
    ]
    results = filter_records(records, "realm:Dayland AND entropy<0.5")
    assert results == [{"realm": "Dayland", "entropy": 0.3}]

    results = filter_records(records, "realm:Dayland OR entropy>0.6")
    assert len(results) == 3
