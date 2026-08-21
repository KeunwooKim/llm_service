from __future__ import annotations

import argparse
import hashlib
import os
import platform
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from screen_solver.prompts import ANALYSIS_PROMPT

DEFAULT_INTERVAL = 60
AGENT_CANDIDATES = (
    "agent",
    "cursor-agent",
    str(Path.home() / ".local" / "bin" / "agent"),
    str(Path.home() / ".cursor" / "bin" / "agent"),
)


@dataclass(frozen=True)
class Settings:
    interval: int
    workspace: Path
    agent_bin: str | None
    once: bool
    image: Path | None


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def capture_screen(dest: Path) -> Path:
    if platform.system() != "Darwin":
        raise RuntimeError(
            "전체 화면 캡처는 macOS의 screencapture만 지원합니다. "
            "다른 OS에서는 --image 로 기존 스크린샷을 넘기세요."
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    # -x: 셔터 소리 없음
    subprocess.run(
        ["screencapture", "-x", "-C", "-t", "png", str(dest)],
        check=True,
    )
    if not dest.exists() or dest.stat().st_size == 0:
        raise RuntimeError(
            "스크린샷이 비어 있습니다. "
            "시스템 설정 > 개인정보 보호 및 보안 > 화면 기록에서 "
            "Terminal 또는 Cursor에 권한을 주세요."
        )
    return dest


def capture_to_temp() -> Path:
    handle, name = tempfile.mkstemp(prefix="ss-", suffix=".png")
    os.close(handle)
    path = Path(name)
    try:
        return capture_screen(path)
    except Exception:
        path.unlink(missing_ok=True)
        raise


def remove_file(path: Path | None) -> None:
    if path is None:
        return
    try:
        path.unlink(missing_ok=True)
    except OSError:
        return


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
        "`curl https://cursor.com/install -fsS | bash` 후 `agent login` 하세요."
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


def is_problem_answer(body: str) -> bool:
    return body.lstrip().startswith("PROBLEM")


def run_once(settings: Settings, last_digest: str | None) -> tuple[str | None, str | None]:
    owned_temp: Path | None = None
    try:
        if settings.image is not None:
            image_path = settings.image
            if not image_path.exists():
                raise FileNotFoundError(f"이미지 파일이 없습니다: {image_path}")
        else:
            image_path = capture_to_temp()
            owned_temp = image_path

        digest = file_digest(image_path)
        if last_digest is not None and digest == last_digest:
            return digest, None

        body = analyze_with_cursor(
            image_path=image_path,
            workspace=settings.workspace,
            agent_bin=settings.agent_bin,
        )
        return digest, body
    finally:
        remove_file(owned_temp)


def run_loop(settings: Settings) -> int:
    last_digest: str | None = None
    try:
        if settings.once:
            _digest, body = run_once(settings, last_digest)
            if body and is_problem_answer(body):
                print(body.strip(), flush=True)
            return 0

        while True:
            started = time.monotonic()
            try:
                digest, body = run_once(settings, last_digest)
                last_digest = digest or last_digest
                if body and is_problem_answer(body):
                    print(body.strip(), flush=True)
            except Exception:
                pass
            elapsed = time.monotonic() - started
            time.sleep(max(0.0, settings.interval - elapsed))
    except KeyboardInterrupt:
        return 0


def parse_args(argv: list[str] | None = None) -> Settings:
    parser = argparse.ArgumentParser(
        description=(
            "맥북 전체 화면을 1분 간격으로 캡처하고, "
            "Cursor Agent로 프로그래밍 문제를 풀어 파이썬 위주 답과 대안을 출력합니다. "
            "스크린샷·로그·해설 파일은 남기지 않습니다."
        )
    )
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help="캡처 간격(초). 기본 60")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Cursor Agent 작업 폴더")
    parser.add_argument("--agent-bin", default=None, help="Cursor Agent 실행 파일. 기본은 PATH의 agent")
    parser.add_argument("--once", action="store_true", help="한 번만 캡처·분석하고 종료")
    parser.add_argument("--image", type=Path, default=None, help="이미 있는 이미지 분석(캡처 생략)")
    args = parser.parse_args(argv)
    if args.interval <= 0:
        parser.error("--interval 은 1 이상이어야 합니다.")
    return Settings(
        interval=args.interval,
        workspace=args.workspace.resolve(),
        agent_bin=args.agent_bin,
        once=args.once,
        image=args.image.resolve() if args.image else None,
    )


def main(argv: list[str] | None = None) -> int:
    settings = parse_args(argv)
    return run_loop(settings)
