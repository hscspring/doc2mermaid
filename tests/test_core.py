"""Tests for doc2mermaid.core — end-to-end pipeline (mocked LLM)."""

import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from doc2mermaid.core import doc_to_map


MOCK_GRAPH = {
    "title": "Mock Pipeline",
    "nodes": [
        {"id": "p1", "type": "problem", "text": "Input problem"},
        {"id": "m1", "type": "method", "text": "Solution approach"},
        {"id": "r1", "type": "result", "text": "Final outcome"},
    ],
    "edges": [["p1", "m1"], ["m1", "r1"]],
}


def _mock_extract(text, **kwargs):
    return MOCK_GRAPH


class TestDocToMap:

    def test_missing_llm_config_raises(self, monkeypatch):
        monkeypatch.delenv("DOC2MERMAID_BASE_URL", raising=False)
        monkeypatch.delenv("DOC2MERMAID_API_KEY", raising=False)
        monkeypatch.delenv("DOC2MERMAID_MODEL", raising=False)
        with pytest.raises(ValueError, match="LLM config required"):
            doc_to_map("some text", output="/tmp/test.svg")

    @patch("doc2mermaid.core.extract_graph", side_effect=_mock_extract)
    @patch("doc2mermaid.core.render_mermaid")
    def test_pipeline_calls_extract_and_render(self, mock_render, mock_extract, tmp_path):
        out = str(tmp_path / "out.svg")
        result = doc_to_map(
            "Hello world",
            output=out,
            llm_base_url="http://fake",
            llm_api_key="fake-key",
            llm_model="fake-model",
        )
        mock_extract.assert_called_once()
        mock_render.assert_called_once()
        assert result == out

    @patch("doc2mermaid.core.extract_graph", side_effect=_mock_extract)
    @patch("doc2mermaid.core.render_mermaid")
    def test_output_path_is_absolute(self, mock_render, mock_extract, tmp_path):
        out = str(tmp_path / "subdir" / "map.svg")
        result = doc_to_map(
            "text",
            output=out,
            llm_base_url="http://x",
            llm_api_key="k",
            llm_model="m",
        )
        assert Path(result).is_absolute()

    @patch("doc2mermaid.core.extract_graph", side_effect=_mock_extract)
    @patch("doc2mermaid.core.render_mermaid")
    def test_env_vars_fallback(self, mock_render, mock_extract, tmp_path, monkeypatch):
        monkeypatch.setenv("DOC2MERMAID_BASE_URL", "http://env-url")
        monkeypatch.setenv("DOC2MERMAID_API_KEY", "env-key")
        monkeypatch.setenv("DOC2MERMAID_MODEL", "env-model")

        out = str(tmp_path / "env_test.svg")
        doc_to_map("text", output=out)
        mock_extract.assert_called_once()
