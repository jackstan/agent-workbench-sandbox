"""Acceptance criteria fixed before any builder run. Known failures are intentional."""

import subprocess
import sys
import unittest

from src.duration import duration_minutes


class DurationAcceptanceTests(unittest.TestCase):
    def test_single_units(self):
        self.assertEqual(duration_minutes("2h"), 120)
        self.assertEqual(duration_minutes("45m"), 45)
        self.assertEqual(duration_minutes("0m"), 0)

    def test_combines_hours_and_minutes(self):
        self.assertEqual(duration_minutes("1h 30m"), 90)

    def test_order_and_whitespace_do_not_change_total(self):
        self.assertEqual(duration_minutes("  30m\t1h  "), 90)

    def test_repeated_units_accumulate(self):
        self.assertEqual(duration_minutes("10m 20m 0h"), 30)

    def test_invalid_input_stays_rejected(self):
        for text in ("", " ", "-1h", "1.5h", "2d", "1h junk", "1h30m"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                duration_minutes(text)

    def test_cli_reports_total_minutes(self):
        result = subprocess.run([sys.executable, "-m", "src.duration", "1h 30m"],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "90")


if __name__ == "__main__":
    unittest.main()
