from tools import contract_test_runner as ctr


def test_load_cases_discovers_samples():
    cases = ctr.load_cases()
    assert cases, "expected at least one contract case"
    names = {case.name for case in cases}
    assert {
        "basic_ritual_victory",
        "guarded_delivery_warning",
        "signal_loop_gain",
        "conditional_repeat_again",
    }.issubset(names)


def test_all_contract_cases_pass():
    results = ctr.run_contract_tests()
    assert results, "expected results from contract test runner"
    failing = [result for result in results if not result.passed]
    assert not failing, f"contract tests failed: {failing}"
