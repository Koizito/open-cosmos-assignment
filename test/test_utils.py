from datetime import datetime, timedelta, timezone

from utils import discard_reasons

def now():
    return datetime.now(timezone.utc)


def test_recent_untagged_is_not_discarded():
    assert discard_reasons(now(), []) == []


def test_irrelevant_tags_are_ignored():
    assert discard_reasons(now(), ["blue", "region-eu"]) == []


def test_old_row_is_discarded():
    old = now() - timedelta(hours=2)
    assert discard_reasons(old, []) == ["too old"]


def test_row_exactly_at_boundary_is_discarded():
    boundary = now() - timedelta(hours=1)
    assert "too old" in discard_reasons(boundary, [])


def test_system_tag_is_discarded():
    assert discard_reasons(now(), ["system"]) == ["tagged system"]


def test_suspect_tag_is_discarded():
    assert discard_reasons(now(), ["suspect"]) == ["tagged suspect"]


def test_both_discard_tags_give_both_reasons():
    assert discard_reasons(now(), ["system", "suspect"]) == [
        "tagged suspect",
        "tagged system",
    ]


def test_old_and_tagged_gives_both_reasons():
    old = now() - timedelta(hours=2)
    assert discard_reasons(old, ["system"]) == ["too old", "tagged system"]