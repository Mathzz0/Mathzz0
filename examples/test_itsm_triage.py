"""Unit tests for the standalone triage demo."""
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from itsm_triage import MATRIX, main, triage_incident

class TriageTests(unittest.TestCase):
    def test_matrix_all_pairs(self):
        for impact in (1, 2, 3):
            for urgency in (1, 2, 3):
                with self.subTest(impact=impact, urgency=urgency):
                    self.assertEqual(triage_incident("software", impact, urgency).priority,
                                     MATRIX[impact - 1][urgency - 1])

    def test_routing_and_normalization(self):
        result = triage_incident(" ACCESS ", 1, 2)
        self.assertEqual((result.category, result.assignment_group, result.priority),
                         ("access", "Identity & Access", "P2"))

    def test_unknown_category(self):
        with self.assertRaisesRegex(ValueError, "unknown category"):
            triage_incident("other", 2, 2)

    def test_category_type(self):
        with self.assertRaises(TypeError):
            triage_incident(None, 2, 2)

    def test_invalid_impact_urgency(self):
        for bad in (0, 4, True, 1.5, "1"):
            for field in ("impact", "urgency"):
                with self.subTest(field=field, value=bad):
                    args = dict(category="software", impact=2, urgency=2)
                    args[field] = bad
                    with self.assertRaises(ValueError):
                        triage_incident(**args)

    def test_initial_state(self):
        self.assertEqual(triage_incident("hardware", 3, 3).state, "new")

    def test_cli(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["--category", "hardware", "--impact", "2", "--urgency", "1"])
        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(output.getvalue())["priority"], "P2")

if __name__ == "__main__":
    unittest.main()
