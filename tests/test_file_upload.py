from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "file-upload.py"


class UploadHandler(BaseHTTPRequestHandler):
    requests = []
    status = 201

    def do_POST(self):
        body = self.rfile.read(int(self.headers["Content-Length"]))
        self.requests.append((self.headers["Content-Type"], body))
        self.send_response(self.status)
        if self.status == 302:
            self.send_header("Location", "/elsewhere")
        self.end_headers()

    def log_message(self, format, *args):
        pass


class FileUploadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), UploadHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/upload"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def setUp(self):
        UploadHandler.requests = []
        UploadHandler.status = 201
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.file = Path(self.directory.name) / "notes.txt"

    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.file), "--url", self.url, *args],
            capture_output=True, text=True,
        )

    def test_uploads_file_at_size_limit_as_multipart(self):
        self.file.write_bytes(b"notes")
        result = self.run_script("--format", "txt", "--size-limit", "5")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("HTTP 201", result.stdout)
        self.assertEqual(len(UploadHandler.requests), 1)
        content_type, body = UploadHandler.requests[0]
        boundary = content_type.split("boundary=")[1].encode("ascii")
        self.assertTrue(body.startswith(b"--" + boundary + b"\r\n"))
        self.assertIn(b'name="file"; filename="notes.txt"', body)
        self.assertIn(b"\r\n\r\nnotes\r\n", body)
        self.assertTrue(body.endswith(b"--" + boundary + b"--\r\n"))

    def test_invalid_files_are_not_uploaded(self):
        for content, limit in ((b"notes", "4"), (b"", "5"), (b" \n", "5"),
                               (b"\xff", "5"), (b"a\0b", "5")):
            with self.subTest(content=content):
                self.file.write_bytes(content)
                result = self.run_script("--format", "txt", "--size-limit", limit)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Error:", result.stderr)
                self.assertEqual(UploadHandler.requests, [])

    def test_rejects_bad_arguments_and_filename(self):
        self.file.write_bytes(b"notes")
        for args in (
            ("--format", "pdf", "--size-limit", "5"),
            ("--format", "txt", "--size-limit", "0"),
        ):
            with self.subTest(args=args):
                result = self.run_script(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(UploadHandler.requests, [])
        self.file = self.file.with_suffix(".pdf")
        self.file.write_bytes(b"notes")
        result = self.run_script("--format", "txt", "--size-limit", "5")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(UploadHandler.requests, [])

    def test_missing_file_and_insecure_remote_endpoint_are_rejected(self):
        result = self.run_script("--format", "txt", "--size-limit", "5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("regular file", result.stderr)

        self.file.write_bytes(b"notes")
        result = self.run_script(
            "--format", "txt", "--size-limit", "5", "--url", "http://example.invalid/upload"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("URL must be HTTPS", result.stderr)
        self.assertEqual(UploadHandler.requests, [])

    def test_http_failure_and_redirect_are_not_successes(self):
        self.file.write_bytes(b"notes")
        for status in (500, 302):
            with self.subTest(status=status):
                UploadHandler.status = status
                result = self.run_script("--format", "txt", "--size-limit", "5")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"HTTP status {status}", result.stderr)
                self.assertNotIn("succeeded", result.stdout)


if __name__ == "__main__":
    unittest.main()
