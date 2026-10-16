"""Flask secret key startup validation in a separate Python interpreter."""
import os
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "src"


def import_application(secret):
    """Import the Flask application without connecting to a real MySQL server."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SOURCE_DIR)
    env.pop("FLASK_SECRET_KEY", None)
    if secret is not None:
        env["FLASK_SECRET_KEY"] = secret
    return subprocess.run(
        [sys.executable, "-c", "import app; print('IMPORT_OK')"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


class FlaskSecretConfigurationTests(unittest.TestCase):
    def test_missing_secret_rejected(self):
        result = import_application(None)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FLASK_SECRET_KEY", result.stderr)

    def test_short_secret_rejected(self):
        result = import_application("test-only-short")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FLASK_SECRET_KEY", result.stderr)

    def test_valid_secret_allows_import(self):
        result = import_application("x" * 32)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("IMPORT_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
