"""Optional student tests; skipped until the student implements normalization."""
import json
import unittest
from pathlib import Path
from dbagent.normalization import find_3nf_violations, decompose_to_3nf

CASE = Path(__file__).resolve().parent.parent / 'examples' / 'normalization_case.json'


class StudentNormalizationTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(CASE.read_text(encoding='utf-8'))

    @unittest.skip('Remove this decorator after implementing 3NF violation checking')
    def test_violation_detection(self):
        violations = find_3nf_violations(self.case['attributes'], self.case['functional_dependencies'])
        self.assertTrue(violations)

    @unittest.skip('Remove this decorator after implementing 3NF decomposition')
    def test_synthesis(self):
        relations = decompose_to_3nf(self.case['attributes'], self.case['functional_dependencies'])
        self.assertTrue(relations)
        # Students must add assertions for dependency preservation,
        # lossless join, and 3NF on their returned relations.


if __name__ == '__main__':
    unittest.main()
