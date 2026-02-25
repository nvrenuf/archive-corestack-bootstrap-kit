from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SignalIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic_id: str
    platform: Literal["reddit", "youtube", "news"]
    content_type: str
    url: str

    source_id: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    collected_at: datetime | None = None
    title: str | None = None
    text_snippet: str | None = None
    language: str | None = None
    engagement_json: dict[str, Any] = Field(default_factory=dict)
    tags_json: dict[str, Any] = Field(default_factory=dict)
    raw_ref_json: dict[str, Any] = Field(default_factory=dict)


class RunStartIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic_id: str
    time_window_days: int


class RunFinishIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: UUID
    status: Literal["ok", "error"]
    counts_json: dict[str, Any]
    error_text: str | None = None
