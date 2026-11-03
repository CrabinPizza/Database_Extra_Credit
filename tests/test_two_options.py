"""Tests that do not require Copilot authentication or paid API access."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from dbagent.copilot_provider import _parse_json
from dbagent import cli

class TestTwoOptions(unittest.TestCase):
    def test_copilot_json_parser(self):
        sample = json.loads((Path(__file__).resolve().parent.parent / "examples" / "university_model.json").read_text())
        self.assertEqual(_parse_json("```json\n" + json.dumps(sample) + "\n```"), sample)

    def test_copilot_provider_routes_from_cli(self):
        sample = json.loads((Path(__file__).resolve().parent.parent / "examples" / "university_model.json").read_text())
        with tempfile.TemporaryDirectory() as folder:
            with patch("dbagent.copilot_provider.extract_requirements_copilot", return_value=sample) as mocked:
                cli.main(["--provider", "copilot", "--requirements", str(Path(__file__).resolve().parent.parent / "examples" / "hospital.txt"), "--out", folder])
                mocked.assert_called_once()
                self.assertTrue((Path(folder) / "create_tables.sql").exists())

if __name__ == "__main__":
    unittest.main()
