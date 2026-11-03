"""Offline regression tests for mapping, rendering, and input validation."""

import unittest
from pathlib import Path
from dbagent.model import load_model, validate_model
from dbagent.mapping import map_relations
from dbagent.render import mermaid, oracle_ddl, review_report

BASE = Path(__file__).resolve().parent.parent

class AgentTests(unittest.TestCase):
    def setUp(self):
        """Build a reusable example design before each test."""
        self.model = load_model(BASE / 'examples' / 'university_model.json')
        self.tables, self.warnings = map_relations(self.model)

    def test_four_entities_plus_junction(self):
        """Check that a many-to-many relationship creates a junction table."""
        self.assertEqual(len(self.tables), 5)
        self.assertIn('Student_Section', [t['name'] for t in self.tables])

    def test_foreign_keys(self):
        """Verify parent relationships map to foreign keys in Section."""
        section = next(t for t in self.tables if t['name'] == 'Section')
        self.assertEqual({f['references'] for f in section['foreign_keys']}, {'Course', 'Instructor'})

    def test_ddl_and_diagram(self):
        """Verify both SQL and Mermaid artifacts are produced."""
        self.assertIn('CREATE TABLE Student_Section', oracle_ddl(self.tables))
        self.assertIn('FOREIGN KEY', oracle_ddl(self.tables))
        self.assertIn('erDiagram', mermaid(self.model))

    def test_report_explicitly_does_not_claim_3nf(self):
        """Prevent the report from incorrectly claiming to prove 3NF."""
        report = review_report('Sample', self.model, self.tables, self.warnings)
        self.assertIn('does not prove 3NF', report)

    def test_reject_bad_identifier(self):
        """Reject unsafe names before they reach SQL generation."""
        bad = {'entities': [{'name': 'X; DROP TABLE T', 'attributes': [{'name':'id','type':'integer'}], 'primary_key':['id']}], 'relationships': []}
        with self.assertRaises(ValueError):
            validate_model(bad)

if __name__ == '__main__':
    unittest.main()
