"""Training sample format: one JSONL row of chat messages."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ALLOWED_ROLES = ("system", "user", "assistant")


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class Sample:
    messages: tuple[Message, ...]


class SampleError(ValueError):
    pass


def validate_sample(raw: object) -> Sample:
    if not isinstance(raw, dict):
        raise SampleError("sample must be an object")
    extra = set(raw) - {"messages"}
    if extra:
        raise SampleError(f"unknown keys: {sorted(extra)}")
    rows = raw.get("messages")
    if not isinstance(rows, list) or not rows:
        raise SampleError("messages must be a non-empty list")

    messages: list[Message] = []
    for item in rows:
        if not isinstance(item, dict):
            raise SampleError("each message must be an object")
        role = item.get("role")
        content = item.get("content")
        if role not in ALLOWED_ROLES:
            raise SampleError(f"role must be one of {ALLOWED_ROLES}")
        if not isinstance(content, str) or not content.strip():
            raise SampleError("content must be a non-empty string")
        messages.append(Message(role=role, content=content))

    roles = {m.role for m in messages}
    if "user" not in roles or "assistant" not in roles:
        raise SampleError("sample needs at least one user and one assistant turn")
    return Sample(messages=tuple(messages))


def read_jsonl(path: Path) -> Iterable[Sample]:
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            yield validate_sample(json.loads(line))
        except (json.JSONDecodeError, SampleError) as exc:
            raise SampleError(f"{path}:{line_no}: {exc}") from exc
