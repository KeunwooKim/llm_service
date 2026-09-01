import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm.config import REPO_ROOT, load_config
from llm.schema import SampleError, read_jsonl, validate_sample
from llm.stages import STAGES, render_board


class ConfigTests(unittest.TestCase):
    def test_default_config_loads(self) -> None:
        cfg = load_config()
        self.assertEqual(cfg.project_name, "llm-service")
        self.assertEqual(cfg.model.base_id, "Qwen/Qwen2.5-1.5B-Instruct")
        self.assertEqual(cfg.train.method, "lora")
        self.assertIn("goal", cfg.missing_decisions())
        self.assertIn("hub_repo", cfg.missing_decisions())

    def test_paths_exist(self) -> None:
        cfg = load_config()
        self.assertTrue((REPO_ROOT / cfg.data.sample_path).is_file())
        self.assertTrue((REPO_ROOT / "docs" / "llm.md").is_file())


class SchemaTests(unittest.TestCase):
    def test_example_jsonl(self) -> None:
        path = REPO_ROOT / "data" / "samples" / "example.jsonl"
        samples = list(read_jsonl(path))
        self.assertGreaterEqual(len(samples), 1)
        self.assertEqual(samples[0].messages[0].role, "system")

    def test_rejects_bad_role(self) -> None:
        with self.assertRaises(SampleError):
            validate_sample(
                {
                    "messages": [
                        {"role": "human", "content": "hi"},
                        {"role": "assistant", "content": "yo"},
                    ]
                }
            )

    def test_rejects_missing_assistant(self) -> None:
        with self.assertRaises(SampleError):
            validate_sample({"messages": [{"role": "user", "content": "hi"}]})

    def test_roundtrip_line(self) -> None:
        line = json.dumps(
            {
                "messages": [
                    {"role": "user", "content": "ping"},
                    {"role": "assistant", "content": "pong"},
                ]
            },
            ensure_ascii=False,
        )
        sample = validate_sample(json.loads(line))
        self.assertEqual(sample.messages[-1].content, "pong")


class StageTests(unittest.TestCase):
    def test_eight_stages_in_order(self) -> None:
        ids = [stage.id for stage in STAGES]
        self.assertEqual(
            ids,
            [
                "0_decide",
                "1_env",
                "2_data",
                "3_base",
                "4_sft",
                "5_eval",
                "6_hub",
                "7_serve",
            ],
        )

    def test_board_lists_missing_goal(self) -> None:
        board = render_board()
        self.assertIn("missing: goal", board)
        self.assertIn("0_decide", board)
