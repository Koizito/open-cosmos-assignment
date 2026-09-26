from datetime import datetime, timezone

import pytest

from poller import parse


def test_decodes_float32_little_endian():
    item = {"time": 1790112910, "value": [14, 113, 82, 63], "tags": []}
    _, value, _ = parse(item)
    assert value == pytest.approx(0.822, abs=1e-3)


def test_decodes_negative_value():
    item = {"time": 1790112910, "value": [0, 0, 128, 190], "tags": []}
    _, value, _ = parse(item)
    assert value < 0


def test_converts_unix_seconds_to_aware_utc_datetime():
    item = {"time": 1790112910, "value": [0, 0, 128, 63], "tags": []}
    timestamp, _, _ = parse(item)
    assert timestamp == datetime.fromtimestamp(1790112910, tz=timezone.utc)
    assert timestamp.tzinfo is not None


def test_passes_tags_through():
    item = {"time": 1790112910, "value": [0, 0, 128, 63], "tags": ["system"]}
    _, _, tags = parse(item)
    assert tags == ["system"]