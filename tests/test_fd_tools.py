"""Tests of provided FD helpers (not student 3NF solutions)."""
import unittest
from dbagent.fd_tools import attribute_closure, remove_redundant_fds, split_rhs

class FDToolTests(unittest.TestCase):
    def test_transitive_closure(self):
        fds = [{"lhs": ["A"], "rhs": ["B"]}, {"lhs": ["B"], "rhs": ["C"]}]
        self.assertEqual(attribute_closure(["A"], fds), {"A", "B", "C"})

    def test_split_rhs(self):
        self.assertEqual(len(split_rhs([{"lhs": ["A"], "rhs": ["C", "B"]}])), 2)

    def test_redundancy_remove_and_keep(self):
        fds = [{"lhs": ["A"], "rhs": ["B"]},
               {"lhs": ["B"], "rhs": ["C"]},
               {"lhs": ["A"], "rhs": ["C"]}]
        remaining, audit = remove_redundant_fds(fds)
        self.assertEqual(remaining, fds[:2])
        self.assertEqual([x["redundant"] for x in audit], [False, False, True])
        self.assertEqual(audit[-1]["closure_without_tested_fd"], ["A", "B", "C"])

    def test_removed_rule_is_not_reused(self):
        fds = [{"lhs": ["A"], "rhs": ["B"]},
               {"lhs": ["A"], "rhs": ["B"]}]
        remaining, audit = remove_redundant_fds(fds)
        self.assertEqual(len(remaining), 1)
        self.assertEqual([x["redundant"] for x in audit], [True, False])

if __name__ == "__main__": unittest.main()
