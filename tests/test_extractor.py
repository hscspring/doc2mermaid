"""Tests for doc2map.extractor — JSON parsing and validation."""

import pytest
from doc2map.extractor import _parse_graph_json, _validate_graph


# ---------- _parse_graph_json ----------

class TestParseGraphJson:

    def test_clean_json(self):
        raw = '{"title":"T","nodes":[{"id":"a","type":"step","text":"A"}],"edges":[]}'
        g = _parse_graph_json(raw)
        assert g["title"] == "T"
        assert len(g["nodes"]) == 1

    def test_json_with_markdown_fences(self):
        raw = '```json\n{"title":"T","nodes":[],"edges":[]}\n```'
        g = _parse_graph_json(raw)
        assert g["title"] == "T"

    def test_json_with_bare_fences(self):
        raw = '```\n{"title":"T","nodes":[],"edges":[]}\n```'
        g = _parse_graph_json(raw)
        assert g["title"] == "T"

    def test_json_embedded_in_text(self):
        raw = 'Here is the graph:\n{"title":"T","nodes":[],"edges":[]}\nDone.'
        g = _parse_graph_json(raw)
        assert g["title"] == "T"

    def test_invalid_json_raises(self):
        with pytest.raises(ValueError, match="Failed to parse"):
            _parse_graph_json("not json at all")

    def test_multiline_json(self):
        raw = """
        {
            "title": "Multi",
            "nodes": [
                {"id": "n1", "type": "idea", "text": "Test node"}
            ],
            "edges": []
        }
        """
        g = _parse_graph_json(raw)
        assert g["title"] == "Multi"
        assert g["nodes"][0]["id"] == "n1"


# ---------- _validate_graph ----------

class TestValidateGraph:

    def _make_graph(self, nodes=None, edges=None):
        return {
            "title": "Test",
            "nodes": nodes or [{"id": "a", "type": "step", "text": "A"}],
            "edges": edges or [],
        }

    def test_valid_graph(self):
        g = self._make_graph(
            nodes=[
                {"id": "a", "type": "step", "text": "A"},
                {"id": "b", "type": "result", "text": "B"},
            ],
            edges=[["a", "b"]],
        )
        _validate_graph(g)  # should not raise

    def test_missing_nodes_key(self):
        with pytest.raises(ValueError, match="nodes"):
            _validate_graph({"edges": []})

    def test_missing_edges_key(self):
        with pytest.raises(ValueError, match="edges"):
            _validate_graph({"nodes": [{"id": "a"}]})

    def test_empty_nodes(self):
        with pytest.raises(ValueError, match="at least one node"):
            _validate_graph({"nodes": [], "edges": []})

    def test_edge_bad_length(self):
        g = self._make_graph(edges=[["a"]])
        with pytest.raises(ValueError, match="source, target"):
            _validate_graph(g)

    def test_edge_unknown_source(self):
        g = self._make_graph(edges=[["unknown", "a"]])
        with pytest.raises(ValueError, match="unknown"):
            _validate_graph(g)

    def test_edge_unknown_target(self):
        g = self._make_graph(edges=[["a", "missing"]])
        with pytest.raises(ValueError, match="missing"):
            _validate_graph(g)
