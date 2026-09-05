import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliEncodingTests(unittest.TestCase):
    def test_redirected_cli_output_uses_utf8_with_a_legacy_system_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            for arguments, expected in (
                (["--help"], "创建"),
                (["new", "EncodingSmoke", "--directory", directory], "项目已创建"),
            ):
                with self.subTest(arguments=arguments):
                    result = subprocess.run(
                        [sys.executable, "-m", "ppx_py.cli", *arguments],
                        env={**os.environ, "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"},
                        capture_output=True,
                        timeout=30,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
                    self.assertIn(expected, result.stdout.decode("utf-8"))
            self.assertTrue((Path(directory) / "ppx.toml").is_file())
