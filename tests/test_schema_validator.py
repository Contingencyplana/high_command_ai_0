import pytest

from tools.schema_validator import SchemaValidationError, validate_payload


def test_valid_order_payload():
    payload = {
        "schema": "high-command-order@1.0",
        "order_id": "order-1",
        "issued_by": "high_command_ai_0",
        "target": "toysoldiers_ai_0",
        "priority": "standard",
        "timestamp_issued": "2025-10-12T00:00:00Z",
        "summary": "Test order",
        "directives": [],
        "requires_ack": True,
    }
    validate_payload(payload)


def test_missing_required_field():
    payload = {"schema": "field-report@1.0", "report_id": "rep-1"}
    with pytest.raises(SchemaValidationError):
        validate_payload(payload)


def test_unknown_schema():
    payload = {"schema": "unknown@1.0"}
    with pytest.raises(SchemaValidationError):
        validate_payload(payload)
