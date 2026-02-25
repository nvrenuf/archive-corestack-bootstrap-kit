from __future__ import annotations

import json
import logging
from typing import Any


LOGGER_NAME = "fear_signal_radar.ingest_api"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def log_ingest_event(logger: logging.Logger, **fields: Any) -> None:
    logger.info(json.dumps(fields, sort_keys=True, default=str))
