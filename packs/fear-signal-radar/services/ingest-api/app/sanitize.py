from __future__ import annotations

import html
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_DROP_BLOCK_TAGS = re.compile(r"<(script|style|iframe)\\b[^>]*>.*?</\\1>", re.IGNORECASE | re.DOTALL)
_STRIP_ANY_TAG = re.compile(r"<[^>]+>")


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def strip_html(value: str) -> str:
    no_blocks = _DROP_BLOCK_TAGS.sub(" ", value)
    no_tags = _STRIP_ANY_TAG.sub(" ", no_blocks)
    return normalize_whitespace(html.unescape(no_tags))


def sanitize_text(value: str | None, *, max_len: int) -> str | None:
    if value is None:
        return None
    cleaned = strip_html(value)
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len]
    return cleaned


def sanitize_url(value: str, *, max_len: int = 2000) -> str:
    cleaned = strip_html(value)
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len]
    return cleaned


def normalize_url_for_dedupe(url: str) -> str:
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    hostname = (parts.hostname or "").lower()

    netloc = hostname
    if parts.port:
        netloc = f"{netloc}:{parts.port}"
    if parts.username:
        auth = parts.username
        if parts.password:
            auth = f"{auth}:{parts.password}"
        netloc = f"{auth}@{netloc}"

    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/") or "/"

    filtered_query = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not (k.lower().startswith("utm_") or k.lower() in {"gclid", "fbclid"})
    ]
    query = urlencode(filtered_query, doseq=True)

    return urlunsplit((scheme, netloc, path, query, ""))
