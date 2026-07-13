import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# entrypoint.py lives at repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import entrypoint as ep


class TestGhHeaders(unittest.TestCase):
    def test_bearer_token(self):
        headers = ep._gh_headers("test-token")
        self.assertEqual(headers["Authorization"], "Bearer test-token")
        self.assertEqual(headers["Accept"], "application/vnd.github+json")


class TestGetToken(unittest.TestCase):
    def test_from_argv(self):
        with patch.object(sys, "argv", ["entrypoint.py", "argv-token"]):
            self.assertEqual(ep._get_token(), "argv-token")

    def test_from_env_when_no_argv(self):
        with patch.object(sys, "argv", ["entrypoint.py"]):
            with patch.dict(os.environ, {"INPUT_GITHUB-TOKEN": "env-token"}, clear=False):
                self.assertEqual(ep._get_token(), "env-token")

    def test_github_token_fallback(self):
        with patch.object(sys, "argv", ["entrypoint.py"]):
            env = {k: v for k, v in os.environ.items() if k not in ("INPUT_GITHUB-TOKEN", "GITHUB_TOKEN")}
            with patch.dict(os.environ, env, clear=True):
                with patch.dict(os.environ, {"GITHUB_TOKEN": "gh-token"}):
                    self.assertEqual(ep._get_token(), "gh-token")


class TestWriteOutputs(unittest.TestCase):
    def test_writes_github_output(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            path = f.name
        try:
            with patch.dict(os.environ, {"GITHUB_OUTPUT": path}):
                ep.write_outputs({"total": 10, "flagged": 2}, "scan-123")
            with open(path) as f:
                content = f.read()
            self.assertIn("total=10", content)
            self.assertIn("flagged=2", content)
            self.assertIn("scan-id=scan-123", content)
        finally:
            os.unlink(path)

    def test_noop_without_github_output(self):
        with patch.dict(os.environ, {}, clear=True):
            ep.write_outputs({"total": 1, "flagged": 0}, "x")  # should not raise


class TestRunSemgrep(unittest.TestCase):
    def test_invalid_json_returns_empty_results(self):
        mock_result = MagicMock(stdout="not json", returncode=0)
        with patch("entrypoint.subprocess.run", return_value=mock_result):
            out = ep.run_semgrep()
        self.assertEqual(out, {"results": [], "errors": []})

    def test_valid_json_parsed(self):
        payload = {"results": [{"check_id": "test"}], "errors": []}
        mock_result = MagicMock(stdout=json.dumps(payload), returncode=0)
        with patch("entrypoint.subprocess.run", return_value=mock_result):
            out = ep.run_semgrep()
        self.assertEqual(out["results"][0]["check_id"], "test")


class TestMarkers(unittest.TestCase):
    def test_scan_marker_present(self):
        self.assertIn("sieve-scan", ep.SCAN_MARKER)

    def test_data_marker_present(self):
        self.assertEqual(ep.DATA_MARKER, "sieve-findings")


if __name__ == "__main__":
    unittest.main()
