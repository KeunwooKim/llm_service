"""Load the single project config from configs/llm.json."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "llm.json"


@dataclass(frozen=True)
class ModelConfig:
    base_id: str
    license_note: str


@dataclass(frozen=True)
class DataConfig:
    raw_dir: str
    processed_dir: str
    sample_path: str
    train_name: str
    eval_name: str


@dataclass(frozen=True)
class TrainConfig:
    method: str
    max_seq_length: int
    assistant_only_loss: bool


@dataclass(frozen=True)
class EvalConfig:
    prompt_count: int


@dataclass(frozen=True)
class LlmConfig:
    project_name: str
    goal: str
    system_prompt: str
    hub_repo: str
    model: ModelConfig
    data: DataConfig
    train: TrainConfig
    eval: EvalConfig

    def missing_decisions(self) -> list[str]:
        missing: list[str] = []
        if not self.goal.strip():
            missing.append("goal")
        if not self.system_prompt.strip():
            missing.append("system_prompt")
        if not self.hub_repo.strip():
            missing.append("hub_repo")
        return missing


def load_config(path: Path | None = None) -> LlmConfig:
    config_path = path or DEFAULT_CONFIG_PATH
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    return LlmConfig(
        project_name=raw["project_name"],
        goal=raw.get("goal", ""),
        system_prompt=raw.get("system_prompt", ""),
        hub_repo=raw.get("hub_repo", ""),
        model=ModelConfig(**raw["model"]),
        data=DataConfig(**raw["data"]),
        train=TrainConfig(**raw["train"]),
        eval=EvalConfig(**raw["eval"]),
    )
