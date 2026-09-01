"""Ordered pipeline. Later stages stay blocked until decisions exist."""

from __future__ import annotations

from dataclasses import dataclass

from llm.config import LlmConfig, load_config


@dataclass(frozen=True)
class Stage:
    id: str
    title: str
    output: str
    status: str


STAGES: tuple[Stage, ...] = (
    Stage("0_decide", "결정", "한 줄 목표, Hub id", "waiting"),
    Stage("1_env", "환경", "HF_TOKEN, 선택 의존성", "waiting"),
    Stage("2_data", "데이터", "processed JSONL", "format_only"),
    Stage("3_base", "베이스 모델", "토크나이저·모델 id", "candidate"),
    Stage("4_sft", "SFT", "LoRA 어댑터", "not_built"),
    Stage("5_eval", "평가", "고정 프롬프트 로그", "not_built"),
    Stage("6_hub", "Hub 업로드", "모델 카드 + 가중치", "not_built"),
    Stage("7_serve", "서빙", "로컬 추론 또는 Space", "not_built"),
)


def render_board(config: LlmConfig | None = None) -> str:
    cfg = config or load_config()
    missing = cfg.missing_decisions()
    lines = [
        f"project: {cfg.project_name}",
        f"base: {cfg.model.base_id}",
        f"train: {cfg.train.method}",
        f"missing: {', '.join(missing) if missing else '(none)'}",
        "",
    ]
    for stage in STAGES:
        lines.append(f"[{stage.status}] {stage.id}  {stage.title}  → {stage.output}")
    return "\n".join(lines)


def main() -> None:
    print(render_board())


if __name__ == "__main__":
    main()
