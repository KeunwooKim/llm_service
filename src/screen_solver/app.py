from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from screen_solver.prompts import ANALYSIS_PROMPT

DEFAULT_INTERVAL = 60
DEFAULT_KEEP = 60
AGENT_CANDIDATES = (
    "agent",
    "cursor-agent",
    str(Path.home() / ".local" / "bin" / "agent"),
    str(Path.home() / ".cursor" / "bin" / "agent"),
)


@dataclass(frozen=True)
class Settings:
    interval: int
    keep: int
    captures_dir: Path
    solutions_dir: Path
    workspace: Path
    agent_bin: str | None
    once: bool
    capture_only: bool
    image: Path | None


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prune_dir(directory: Path, keep: int, pattern: str) -> None:
    if keep <= 0:
        return
    files = sorted(
        (
            path
            for path in directory.glob(pattern)
            if not path.name.startswith("latest.")
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for stale in files[keep:]:
        stale.unlink(missing_ok=True)


def capture_screen(dest: Path) -> Path:
    if platform.system() != "Darwin":
        raise RuntimeError(
            "전체 화면 캡처는 macOS의 screencapture만 지원합니다. "
            "다른 OS에서는 --image 로 기존 스크린샷을 넘기세요."
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    # -x: 무음, -C: 마우스 커서 포함, -t png: PNG
    subprocess.run(
        ["screencapture", "-x", "-C", "-t", "png", str(dest)],
        check=True,
    )
    if not dest.exists() or dest.stat().st_size == 0:
        raise RuntimeError(
            f"스크린샷이 비어 있습니다: {dest}. "
            "시스템 설정 > 개인정보 보호 및 보안 > 화면 기록에서 "
            "Terminal 또는 Cursor에 권한을 주세요."
        )
    return dest


def resolve_agent_bin(explicit: str | None) -> str:
    if explicit:
        path = shutil.which(explicit) if os.path.sep not in explicit else explicit
        if path and Path(path).exists():
            return path
        raise FileNotFoundError(f"Cursor Agent 실행 파일을 찾을 수 없습니다: {explicit}")
    for candidate in AGENT_CANDIDATES:
        found = shutil.which(candidate) if os.path.sep not in candidate else candidate
        if found and Path(found).exists():
            return str(found)
    raise FileNotFoundError(
        "Cursor Agent CLI(`agent`)를 찾을 수 없습니다. "
        "https://cursor.com/docs/cli/installation 의 "
        "`curl https://cursor.com/install -fsS | bash` 후 `agent login` 하세요. "
        "캡처만 하려면 --capture-only 를 쓰세요."
    )


def build_agent_command(agent_bin: str, workspace: Path, image_path: Path) -> list[str]:
    prompt = ANALYSIS_PROMPT.format(image_path=image_path)
    return [
        agent_bin,
        "-p",
        "--mode",
        "ask",
        "--trust",
        "--workspace",
        str(workspace),
        "--output-format",
        "text",
        prompt,
    ]


def analyze_with_cursor(
    image_path: Path,
    workspace: Path,
    agent_bin: str | None = None,
    timeout: int = 180,
    runner=subprocess.run,
) -> str:
    resolved = resolve_agent_bin(agent_bin)
    command = build_agent_command(resolved, workspace, image_path)
    result = runner(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        detail = stderr or stdout or f"exit {result.returncode}"
        raise RuntimeError(f"Cursor Agent 분석 실패: {detail}")
    output = (result.stdout or "").strip()
    if not output:
        raise RuntimeError("Cursor Agent가 빈 응답을 반환했습니다.")
    return output


def write_solution(path: Path, image_path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Screen solver\n\n"
        f"- captured: `{image_path.name}`\n"
        f"- analyzed_at: `{datetime.now(timezone.utc).isoformat()}`\n\n"
    )
    path.write_text(header + body.rstrip() + "\n", encoding="utf-8")


def copy_latest(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def run_once(settings: Settings, last_digest: str | None) -> str | None:
    stamp = utc_stamp()
    if settings.image is not None:
        image_path = settings.image
        if not image_path.exists():
            raise FileNotFoundError(f"이미지 파일이 없습니다: {image_path}")
    else:
        image_path = settings.captures_dir / f"{stamp}.png"
        capture_screen(image_path)
        copy_latest(image_path, settings.captures_dir / "latest.png")
        prune_dir(settings.captures_dir, settings.keep, "*.png")

    digest = file_digest(image_path)
    if last_digest is not None and digest == last_digest:
        print(f"[skip] 화면이 이전과 같습니다: {image_path.name}", flush=True)
        if settings.image is None:
            image_path.unlink(missing_ok=True)
        return digest

    print(f"[capture] {image_path}", flush=True)
    if settings.capture_only:
        return digest

    body = analyze_with_cursor(
        image_path=image_path,
        workspace=settings.workspace,
        agent_bin=settings.agent_bin,
    )
    solution_path = settings.solutions_dir / f"{stamp}.md"
    write_solution(solution_path, image_path, body)
    copy_latest(solution_path, settings.solutions_dir / "latest.md")
    prune_dir(settings.solutions_dir, settings.keep, "*.md")
    print(f"[solved] {solution_path}", flush=True)
    return digest


def run_loop(settings: Settings) -> int:
    settings.captures_dir.mkdir(parents=True, exist_ok=True)
    settings.solutions_dir.mkdir(parents=True, exist_ok=True)
    last_digest: str | None = None
    try:
        if settings.once:
            run_once(settings, last_digest)
            return 0

        print(
            f"[watch] {settings.interval}s 간격으로 캡처합니다. "
            f"captures={settings.captures_dir} solutions={settings.solutions_dir}",
            flush=True,
        )
        while True:
            started = time.monotonic()
            try:
                last_digest = run_once(settings, last_digest) or last_digest
            except Exception as exc:  # noqa: BLE001 - keep the loop alive
                print(f"[error] {exc}", file=sys.stderr, flush=True)
            elapsed = time.monotonic() - started
            time.sleep(max(0.0, settings.interval - elapsed))
    except KeyboardInterrupt:
        print("\n[stop] 중단했습니다.", flush=True)
        return 0


def parse_args(argv: list[str] | None = None) -> Settings:
    parser = argparse.ArgumentParser(
        description=(
            "맥북 전체 화면을 1분 간격으로 캡처하고, "
            "Cursor Agent로 프로그래밍 문제를 풀어 파이썬 위주 답과 대안을 저장합니다."
        )
    )
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help="캡처 간격(초). 기본 60")
    parser.add_argument("--keep", type=int, default=DEFAULT_KEEP, help="유지할 최근 파일 개수. 기본 60")
    parser.add_argument("--captures", type=Path, default=Path("captures"), help="스크린샷 저장 폴더")
    parser.add_argument("--solutions", type=Path, default=Path("solutions"), help="해설 저장 폴더")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Cursor Agent 작업 폴더")
    parser.add_argument("--agent-bin", default=None, help="Cursor Agent 실행 파일. 기본은 PATH의 agent")
    parser.add_argument("--once", action="store_true", help="한 번만 캡처·분석하고 종료")
    parser.add_argument("--capture-only", action="store_true", help="캡처만 하고 Cursor Agent는 호출하지 않음")
    parser.add_argument("--image", type=Path, default=None, help="이미 있는 이미지 분석(캡처 생략)")
    args = parser.parse_args(argv)
    if args.interval <= 0:
        parser.error("--interval 은 1 이상이어야 합니다.")
    return Settings(
        interval=args.interval,
        keep=args.keep,
        captures_dir=args.captures.resolve(),
        solutions_dir=args.solutions.resolve(),
        workspace=args.workspace.resolve(),
        agent_bin=args.agent_bin,
        once=args.once,
        capture_only=args.capture_only,
        image=args.image.resolve() if args.image else None,
    )


def main(argv: list[str] | None = None) -> int:
    settings = parse_args(argv)
    return run_loop(settings)
