import hashlib
import os
import platform
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from ppx_py import Settings
from ppx_py.update import ApplicationUpdater


ROOT = Path(__file__).resolve().parents[3]


class DownloadHandler(BaseHTTPRequestHandler):
    payload = b"PPX update package" * 256

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Length", str(len(self.payload)))
        self.end_headers()
        self.wfile.write(self.payload)

    def log_message(self, *_args):
        pass


class ApplicationUpdateTests(unittest.TestCase):
    def setUp(self):
        self.updater = ApplicationUpdater(Settings.load(ROOT / "ppx.toml"))

    def test_version_comparison_is_numeric(self):
        self.assertTrue(self.updater.compare_versions("5.9.9", "5.10.0"))
        self.assertFalse(self.updater.compare_versions("5.10.0", "5.9.9"))
        self.assertFalse(self.updater.compare_versions("5.10.0", "5.10.0"))

    def test_selects_asset_for_current_platform(self):
        assets = [
            {"name": "PPX-V6.0.0_Windows.exe"},
            {"name": "PPX-V6.0.0_macOS.dmg"},
            {"name": "PPX-V6.0.0_Linux.deb"},
        ]
        with patch.object(platform, "system", return_value="Darwin"):
            selected = self.updater.select_asset(assets)
        self.assertEqual(selected["name"], "PPX-V6.0.0_macOS.dmg")

    def test_never_falls_back_to_an_incompatible_architecture(self):
        with patch.object(platform, "system", return_value="Darwin"), patch.object(
            platform, "machine", return_value="arm64"
        ):
            wrong = {"name": "App_macOS_x64.dmg"}
            self.assertIsNone(self.updater.select_asset([wrong]))
            right = {"name": "App_macOS_arm64.dmg"}
            self.assertEqual(self.updater.select_asset([wrong, right]), right)
            generic = {"name": "App_macOS.dmg"}
            self.assertEqual(self.updater.select_asset([wrong, generic]), generic)

    def test_concurrent_download_does_not_clear_cancellation(self):
        self.updater._download_lock.acquire()
        try:
            self.updater.cancel()
            result = self.updater.download()
            self.assertEqual(result["code"], -2)
            self.assertTrue(self.updater._cancelled.is_set())
        finally:
            self.updater._download_lock.release()

    def test_cancel_during_release_check_prevents_download(self):
        def check():
            self.updater.cancel()
            return {"code": 0, "assets": [{
                "name": "App_macOS.dmg", "digest": "sha256:" + "0" * 64,
            }]}
        with patch.object(self.updater, "check", side_effect=check), patch.object(
            platform, "system", return_value="Darwin"
        ), patch.object(self.updater, "_download") as download:
            self.assertEqual(self.updater.download()["msg"], "取消更新")
            download.assert_not_called()

    def test_cancel_at_last_progress_never_publishes_file(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), DownloadHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "update.dmg"
                path.write_bytes(b"previous valid download")
                self.updater.progress = lambda _progress: self.updater.cancel()
                result = self.updater._download(
                    f"http://127.0.0.1:{server.server_port}/update", path, 0,
                    "sha256:" + hashlib.sha256(DownloadHandler.payload).hexdigest(),
                )
                self.assertFalse(result["status"])
                self.assertEqual(result["msg"], "取消更新")
                self.assertEqual(path.read_bytes(), b"previous valid download")
                self.assertFalse(path.with_suffix(".dmg.part").exists())
        finally:
            server.shutdown()
            server.server_close()

    def test_download_verifies_sha256_and_uses_atomic_file(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), DownloadHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "update.dmg"
                digest = "sha256:" + hashlib.sha256(DownloadHandler.payload).hexdigest()
                result = self.updater._download(
                    f"http://127.0.0.1:{server.server_port}/update",
                    path,
                    len(DownloadHandler.payload),
                    digest,
                )
                self.assertTrue(result["status"])
                self.assertTrue(path.is_file())
                self.assertFalse(Path(str(path) + ".part").exists())
        finally:
            server.shutdown()
            server.server_close()

    def test_download_rejects_invalid_digest(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), DownloadHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "update.dmg"
                result = self.updater._download(
                    f"http://127.0.0.1:{server.server_port}/update",
                    path,
                    len(DownloadHandler.payload),
                    "sha256:" + "0" * 64,
                )
                self.assertFalse(result["status"])
                self.assertFalse(path.exists())
                self.assertFalse(Path(str(path) + ".part").exists())
        finally:
            server.shutdown()
            server.server_close()

    def test_download_rejects_missing_digest_before_creating_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "update.dmg"
            result = self.updater._download("https://example.invalid/update", path, 0, "")
            self.assertFalse(result["status"])
            self.assertIn("SHA-256", result["msg"])
            self.assertFalse(path.exists())

    def test_rejects_unsafe_release_asset_names(self):
        for name in ("../update.dmg", "folder/update.dmg", "folder\\update.dmg", ".."):
            with self.subTest(name=name):
                self.assertFalse(self.updater.safe_asset_name(name))
        self.assertTrue(self.updater.safe_asset_name("PPX-V6.0.0_macOS.dmg"))


if __name__ == "__main__":
    unittest.main()
