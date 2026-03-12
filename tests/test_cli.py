"""Tests for doc2map.cli — command-line interface."""

import sys
import pytest
from unittest.mock import patch, MagicMock
from doc2map.cli import main


class TestCli:

    @patch("doc2map.cli.doc_to_map", return_value="/tmp/out.svg")
    def test_basic_invocation(self, mock_d2m, tmp_path):
        infile = tmp_path / "input.md"
        infile.write_text("# Hello\nSome content here.")
        outfile = str(tmp_path / "out.svg")

        with patch("sys.argv", ["doc2map", str(infile), "-o", outfile,
                                "--base-url", "http://x", "--api-key", "k", "--model", "m"]):
            main()

        mock_d2m.assert_called_once()
        args = mock_d2m.call_args
        assert "Hello" in args[0][0] or "Hello" in args.kwargs.get("text", args[0][0])

    def test_empty_input_exits(self, tmp_path):
        infile = tmp_path / "empty.md"
        infile.write_text("")

        with patch("sys.argv", ["doc2map", str(infile)]):
            with pytest.raises(SystemExit):
                main()

    @patch("doc2map.cli.doc_to_map", side_effect=ValueError("bad config"))
    def test_error_exits(self, mock_d2m, tmp_path):
        infile = tmp_path / "input.md"
        infile.write_text("Content")

        with patch("sys.argv", ["doc2map", str(infile)]):
            with pytest.raises(SystemExit):
                main()

    @patch("doc2map.cli.doc_to_map", return_value="/tmp/out.svg")
    def test_stdin_input(self, mock_d2m, monkeypatch):
        monkeypatch.setattr("sys.stdin", MagicMock(read=lambda: "stdin content"))

        with patch("sys.argv", ["doc2map", "-", "-o", "/tmp/out.svg",
                                "--base-url", "http://x", "--api-key", "k", "--model", "m"]):
            main()

        call_text = mock_d2m.call_args[0][0]
        assert "stdin content" in call_text
