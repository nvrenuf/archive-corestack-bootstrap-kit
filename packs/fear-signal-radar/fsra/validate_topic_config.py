from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


PACK_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_PATH = PACK_DIR / "schemas" / "topic_config.schema.json"


def validate_topic_config(topic_path: Path, schema_path: Path = DEFAULT_SCHEMA_PATH) -> None:
    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    with topic_path.open("r", encoding="utf-8") as f:
        topic = yaml.safe_load(f)

    validator = Draft202012Validator(schema)
    validator.validate(topic)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate FSRA topic config against schema.")
    parser.add_argument("topic_config", type=Path, help="Path to topic YAML file")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help="Path to topic config schema",
    )
    args = parser.parse_args()

    validate_topic_config(args.topic_config, args.schema)
    print("topic config is valid")
