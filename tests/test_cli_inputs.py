"""CLI input routing tests; patch the LLM so no paid API is called."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from dbagent.cli import main
from dbagent.model import load_model

ROOT = Path(__file__).resolve().parent.parent


class CLIInputTests(unittest.TestCase):
    def test_file_input_calls_llm_with_contents(self):
        with tempfile.TemporaryDirectory() as tmp:
            requirements = Path(tmp) / 'req.txt'
            requirements.write_text('Design a library database.', encoding='utf-8')
            model = load_model(ROOT / 'examples/university_model.json')
            with patch('dbagent.cli.extract_requirements', return_value=model) as llm:
                main(['--requirements', str(requirements), '--out', str(Path(tmp) / 'out')])
            self.assertEqual(llm.call_args.args[0], 'Design a library database.')
            self.assertTrue((Path(tmp) / 'out' / 'er_diagram.mmd').exists())

    def test_interactive_collects_lines_until_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            model = load_model(ROOT / 'examples/university_model.json')
            with patch('builtins.input', side_effect=['A school has students.', 'Students enroll in courses.', 'END']):
                with patch('dbagent.cli.extract_requirements', return_value=model) as llm:
                    main(['--interactive', '--out', str(Path(tmp) / 'out')])
            self.assertEqual(llm.call_args.args[0], 'A school has students.\nStudents enroll in courses.')
            self.assertTrue((Path(tmp) / 'out' / 'create_tables.sql').exists())

    def test_empty_interactive_input_rejected(self):
        with patch('builtins.input', return_value='END'):
            with self.assertRaises(SystemExit):
                main(['--interactive'])


if __name__ == '__main__':
    unittest.main()
