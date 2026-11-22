import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "upload-format.py"


class UploadFormatTests(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
        )

    def test_generates_configuration_from_arguments(self):
        result = self.run_script(
            "--max-input-size", "1024", "--languages", "English", "French"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "upload_formats": ["txt"],
            "max_input_size_bytes": 1024,
            "note_languages": ["English", "French"],
        })

    def test_rejects_invalid_size_and_missing_or_empty_languages(self):
        for args in (
            ("--max-input-size", "0", "--languages", "English"),
            ("--max-input-size", "-1", "--languages", "English"),
            ("--max-input-size", "abc", "--languages", "English"),
            ("--max-input-size", "10"),
            ("--max-input-size", "10", "--languages", " "),
        ):
            with self.subTest(args=args):
                result = self.run_script(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
