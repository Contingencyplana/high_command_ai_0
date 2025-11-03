from tools import exchange_watcher as watcher


def test_compute_changes_tracks_added_and_removed_entries():
    previous = {
        "orders_pending": {"order-1": {"id": "order-1"}},
        "acks_pending": {},
        "reports_inbox": {"report-1": {"id": "report-1"}},
    }
    current = {
        "orders_pending": {"order-2": {"id": "order-2"}},
        "acks_pending": {"ack-1": {"id": "ack-1"}},
        "reports_inbox": {},
    }

    changes = watcher.compute_changes(previous, current)

    assert changes["orders_pending"]["added"] == ["order-2"]
    assert changes["orders_pending"]["removed"] == ["order-1"]
    assert changes["acks_pending"]["added"] == ["ack-1"]
    assert changes["acks_pending"]["removed"] == []
    assert changes["reports_inbox"]["added"] == []
    assert changes["reports_inbox"]["removed"] == ["report-1"]


def test_format_entry_includes_summary_and_timestamp():
    entry = {"summary": "Reminder", "timestamp": "2025-10-12T21:00:00Z"}
    rendered = watcher.format_entry("order-2", entry)
    assert "order-2" in rendered
    assert "Reminder" in rendered
    assert "2025-10-12T21:00:00Z" in rendered