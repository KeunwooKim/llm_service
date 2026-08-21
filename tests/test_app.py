from __future__ import annotations

import io
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
    is_problem_answer,
    parse_args,
    remove_file,
    run_loop,
    run_once,
)
from screen_solver.prompts import ANALYSIS_PROMPT

TINY_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c63000100000500010d0a2db40000000049454e44ae426082"
)


class DigestTests(unittest.TestCase):
    def test_file_digest_matches_identical_bytes(self) -> None:
        with TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.png"
            b = Path(tmp) / "b.png"
            a.write_bytes(TINY_PNG)
            b.write_bytes(TINY_PNG)
            self.assertEqual(file_digest(a), file_digest(b))


class CaptureTests(unittest.TestCase):
    def test_capture_screen_rejects_non_mac(self) -> None:
        if platform.system() == "Darwin":
            self.skipTest("macOS에서는 거부 경로를 검증하지 않음")
        with TemporaryDirectory() as tmp:
            dest = Path(tmp) / "shot.png"
            with self.assertRaisesRegex(RuntimeError, "macOS"):
                capture_screen(dest)


class AgentCommandTests(unittest.TestCase):
    def test_prompt_asks_for_python_and_forbids_files(self) -> None:
        self.assertIn("파이썬", ANALYSIS_PROMPT)
        self.assertIn("다른 답변", ANALYSIS_PROMPT)
        self.assertIn("디스크에 파일", ANALYSIS_PROMPT)
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
    def test_skips_unchanged_image_without_agent(self) -> None:
        with TemporaryDirectory() as tmp:
            image = Path(tmp) / "shot.png"
            image.write_bytes(TINY_PNG)
            settings = parse_args(["--once", "--image", str(image)])
            digest = file_digest(image)
            with patch("screen_solver.app.analyze_with_cursor") as mocked:
                result_digest, body = run_once(settings, last_digest=digest)
            mocked.assert_not_called()
            self.assertEqual(result_digest, digest)
            self.assertIsNone(body)
            self.assertTrue(image.exists())

    def test_returns_answer_and_does_not_write_files(self) -> None:
        with TemporaryDirectory() as tmp:
            image = Path(tmp) / "shot.png"
            image.write_bytes(TINY_PNG)
            settings = parse_args(["--once", "--image", str(image), "--workspace", tmp])
            with patch(
                "screen_solver.app.analyze_with_cursor",
                return_value="PROBLEM\n```python\nprint(1)\n```\n",
            ):
                digest, body = run_once(settings, last_digest=None)
            self.assertIsNotNone(digest)
            self.assertIn("print(1)", body or "")
            self.assertFalse((Path(tmp) / "solutions").exists())
            self.assertFalse((Path(tmp) / "captures").exists())
            self.assertFalse((Path(tmp) / "logs").exists())
            self.assertTrue(image.exists())

    def test_deletes_owned_temp_capture(self) -> None:
        created: dict[str, Path] = {}

        def fake_capture(dest: Path) -> Path:
            dest.write_bytes(TINY_PNG)
            created["path"] = dest
            return dest

        settings = parse_args(["--once"])
        with patch("screen_solver.app.capture_screen", side_effect=fake_capture):
            with patch(
                "screen_solver.app.analyze_with_cursor",
                return_value="PROBLEM\nprint(1)\n",
            ):
                run_once(settings, last_digest=None)
        self.assertIn("path", created)
        self.assertFalse(created["path"].exists())

    def test_parse_interval_default_is_one_minute(self) -> None:
        settings = parse_args([])
        self.assertEqual(settings.interval, 60)
        self.assertFalse(settings.once)
        self.assertIsNone(settings.image)


class OutputTests(unittest.TestCase):
    def test_is_problem_answer(self) -> None:
        self.assertTrue(is_problem_answer("PROBLEM\ncode"))
        self.assertFalse(is_problem_answer("NO_PROBLEM"))
        self.assertFalse(is_problem_answer("hello"))

    def test_once_prints_problem_only(self) -> None:
        with TemporaryDirectory() as tmp:
            image = Path(tmp) / "shot.png"
            image.write_bytes(TINY_PNG)
            settings = parse_args(["--once", "--image", str(image)])
            with patch(
                "screen_solver.app.analyze_with_cursor",
                return_value="PROBLEM\nprint(1)\n",
            ):
                with patch("sys.stdout", new=io.StringIO()) as stdout:
                    code = run_loop(settings)
            self.assertEqual(code, 0)
            self.assertIn("print(1)", stdout.getvalue())

    def test_once_silent_when_no_problem(self) -> None:
        with TemporaryDirectory() as tmp:
            image = Path(tmp) / "shot.png"
            image.write_bytes(TINY_PNG)
            settings = parse_args(["--once", "--image", str(image)])
            with patch(
                "screen_solver.app.analyze_with_cursor",
                return_value="NO_PROBLEM",
            ):
                with patch("sys.stdout", new=io.StringIO()) as stdout:
                    run_loop(settings)
            self.assertEqual(stdout.getvalue(), "")

    def test_remove_file_ignores_missing(self) -> None:
        remove_file(Path("/tmp/does-not-exist-screen-solver.png"))


if __name__ == "__main__":
    unittest.main()
