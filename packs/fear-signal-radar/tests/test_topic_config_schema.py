from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

PACK_DIR = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PACK_DIR / "schemas" / "topic_config.schema.json"
TOPIC_PATH = PACK_DIR / "configs" / "topics" / "work-money_entry-level-collapse.yaml"


def _load_schema() -> dict:
    assert SCHEMA_PATH.exists(), f"Schema not found: {SCHEMA_PATH}"
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_topic() -> dict:
    assert TOPIC_PATH.exists(), f"Topic config not found: {TOPIC_PATH}"
    with TOPIC_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _validate(config: dict) -> None:
    schema = _load_schema()
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(config), key=lambda e: e.path)
    if errors:
        raise ValidationError(errors[0].message)


def test_schema_validates_correct_topic() -> None:
    topic = _load_topic()
    _validate(topic)


def test_missing_required_field_fails() -> None:
    topic = deepcopy(_load_topic())
    topic.pop("topic_id", None)
    with pytest.raises(ValidationError):
        _validate(topic)


def test_invalid_platform_enum_fails() -> None:
    topic = deepcopy(_load_topic())
    topic["platforms_enabled"] = topic["platforms_enabled"] + ["tiktok"]
    with pytest.raises(ValidationError):
        _validate(topic)


def test_missing_scoring_weight_field_fails() -> None:
    topic = deepcopy(_load_topic())
    topic["scoring_weights"].pop("velocity", None)
    with pytest.raises(ValidationError):
        _validate(topic)


def test_additional_property_rejected() -> None:
    topic = deepcopy(_load_topic())
    topic["unexpected"] = "nope"
    with pytest.raises(ValidationError):
        _validate(topic)


def test_reddit_requires_subreddits() -> None:
    topic = deepcopy(_load_topic())
    assert "reddit" in topic["platforms_enabled"]
    topic.pop("subreddits", None)
    with pytest.raises(ValidationError):
        _validate(topic)


def test_youtube_requires_queries() -> None:
    topic = deepcopy(_load_topic())
    assert "youtube" in topic["platforms_enabled"]
    topic.pop("youtube_queries", None)
    with pytest.raises(ValidationError):
        _validate(topic)


def test_scoring_weights_range_enforced() -> None:
    topic = deepcopy(_load_topic())
    topic["scoring_weights"]["volume"] = 10
    with pytest.raises(ValidationError):
        _validate(topic)


def test_no_duplicate_platforms() -> None:
    topic = deepcopy(_load_topic())
    topic["platforms_enabled"] = ["reddit", "reddit", "youtube"]
    with pytest.raises(ValidationError):
        _validate(topic)
