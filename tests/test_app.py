from __future__ import annotations

import os
import platform
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from screen_solver.app import (
    analyze_with_cursor,
    build_agent_command,
    capture_screen,
    file_digest,
    parse_args,
    prune_dir,
    run_once,
    write_solution,
)
from screen_solver.prompts import ANALYSIS_PROMPT

TINY_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c63000100000500010d0a2db40000000049454e44ae426082"
)


class DigestAndPruneTests(unittest.TestCase):
    def test_file_digest_matches_identical_bytes(self) -> None:
        with TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.png"
            b = Path(tmp) / "b.png"
            a.write_bytes(TINY_PNG)
            b.write_bytes(TINY_PNG)
            self.assertEqual(file_digest(a), file_digest(b))

    def test_prune_keeps_latest_and_newest(self) -> None:
        with TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "latest.png").write_bytes(TINY_PNG)
            for index in range(5):
                path = folder / f"20260101T00000{index}Z.png"
                path.write_bytes(TINY_PNG)
                os.utime(path, (index, index))
            prune_dir(folder, keep=2, pattern="*.png")
            remaining = sorted(p.name for p in folder.glob("*.png"))
            self.assertIn("latest.png", remaining)
            self.assertEqual(len(remaining), 3)


class CaptureTests(unittest.TestCase):
    def test_capture_screen_rejects_non_mac(self) -> None:
        if platform.system() == "Darwin":
            self.skipTest("macOS에서는 거부 경로를 검증하지 않음")
        with TemporaryDirectory() as tmp:
            dest = Path(tmp) / "shot.png"
            with self.assertRaisesRegex(RuntimeError, "macOS"):
                capture_screen(dest)


class AgentCommandTests(unittest.TestCase):
    def test_prompt_asks_for_python_and_alternatives(self) -> None:
        self.assertIn("파이썬", ANALYSIS_PROMPT)
        self.assertIn("다른 답변", ANALYSIS_PROMPT)
        self.assertIn("{image_path}", ANALYSIS_PROMPT)

    def test_build_agent_command_uses_ask_mode(self) -> None:
        image = Path("/tmp/shot.png")
        command = build_agent_command("agent", Path("/tmp/ws"), image)
        self.assertEqual(command[0], "agent")
        self.assertIn("-p", command)
        self.assertIn("ask", command)
        self.assertIn(str(image), command[-1])

    def test_analyze_with_cursor_returns_stdout(self) -> None:
        def fake_run(command, **kwargs):
            self.assertEqual(command[0], "/usr/bin/agent")
            return SimpleNamespace(returncode=0, stdout="PROBLEM\nprint(1)\n", stderr="")

        with patch("screen_solver.app.resolve_agent_bin", return_value="/usr/bin/agent"):
            text = analyze_with_cursor(
                Path("/tmp/shot.png"),
                Path("/tmp/ws"),
                runner=fake_run,
            )
        self.assertIn("PROBLEM", text)

    def test_analyze_with_cursor_raises_on_failure(self) -> None:
        def fake_run(command, **kwargs):
            return SimpleNamespace(returncode=1, stdout="", stderr="not logged in")

        with patch("screen_solver.app.resolve_agent_bin", return_value="/usr/bin/agent"):
            with self.assertRaisesRegex(RuntimeError, "not logged in"):
                analyze_with_cursor(
                    Path("/tmp/shot.png"),
                    Path("/tmp/ws"),
                    runner=fake_run,
                )


class RunOnceTests(unittest.TestCase):
    def test_skips_unchanged_image(self) -> None:
        with TemporaryDirectory() as tmp:
            image = Path(tmp) / "shot.png"
            image.write_bytes(TINY_PNG)
            settings = parse_args(
                ["--once", "--capture-only", "--image", str(image), "--captures", tmp]
            )
            digest = file_digest(image)
            result = run_once(settings, last_digest=digest)
            self.assertEqual(result, digest)

    def test_writes_solution_from_agent(self) -> None:
        with TemporaryDirectory() as tmp:
            image = Path(tmp) / "shot.png"
            image.write_bytes(TINY_PNG)
            solutions = Path(tmp) / "solutions"
            settings = parse_args(
                [
                    "--once",
                    "--image",
                    str(image),
                    "--captures",
                    tmp,
                    "--solutions",
                    str(solutions),
                    "--workspace",
                    tmp,
                ]
            )
            with patch(
                "screen_solver.app.analyze_with_cursor",
                return_value="PROBLEM\n```python\nprint(1)\n```\n",
            ) as mocked:
                run_once(settings, last_digest=None)
            mocked.assert_called_once()
            latest = (solutions / "latest.md").read_text(encoding="utf-8")
            self.assertIn("print(1)", latest)
            self.assertIn("shot.png", latest)

    def test_parse_interval_default_is_one_minute(self) -> None:
        settings = parse_args([])
        self.assertEqual(settings.interval, 60)
        self.assertFalse(settings.once)
        self.assertFalse(settings.capture_only)


class WriteSolutionTests(unittest.TestCase):
    def test_write_solution_adds_header(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.md"
            write_solution(path, Path("a.png"), "body")
            text = path.read_text(encoding="utf-8")
            self.assertIn("a.png", text)
            self.assertIn("body", text)


if __name__ == "__main__":
    unittest.main()
