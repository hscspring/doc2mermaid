"""Tests for doc2mermaid.renderer — Mermaid code generation and rendering."""

import shutil
import pytest
from pathlib import Path
from doc2mermaid.renderer import graph_to_mermaid, render_mermaid


SAMPLE_GRAPH = {
    "title": "Test Pipeline",
    "nodes": [
        {"id": "p1", "type": "problem", "text": "Data quality is low"},
        {"id": "m1", "type": "method", "text": "Reward model filtering"},
        {"id": "s1", "type": "step", "text": "Generate candidates"},
        {"id": "s2", "type": "step", "text": "Score with RM"},
        {"id": "r1", "type": "result", "text": "40% quality improvement"},
    ],
    "edges": [["p1", "m1"], ["m1", "s1"], ["s1", "s2"], ["s2", "r1"]],
}


class TestGraphToMermaid:

    def test_starts_with_graph_td(self):
        code = graph_to_mermaid(SAMPLE_GRAPH)
        assert code.startswith("graph TD")

    def test_contains_all_nodes(self):
        code = graph_to_mermaid(SAMPLE_GRAPH)
        for node in SAMPLE_GRAPH["nodes"]:
            assert node["id"] in code
            assert node["text"] in code

    def test_contains_all_edges(self):
        code = graph_to_mermaid(SAMPLE_GRAPH)
        for src, tgt in SAMPLE_GRAPH["edges"]:
            assert f"{src} --> {tgt}" in code

    def test_contains_style_definitions(self):
        code = graph_to_mermaid(SAMPLE_GRAPH)
        assert "style p1" in code
        assert "style m1" in code
        assert "fill:" in code

    def test_empty_edges(self):
        graph = {
            "title": "Solo",
            "nodes": [{"id": "n1", "type": "idea", "text": "Just one node"}],
            "edges": [],
        }
        code = graph_to_mermaid(graph)
        assert "n1" in code
        assert "-->" not in code

    def test_node_shapes_by_type(self):
        code = graph_to_mermaid(SAMPLE_GRAPH)
        assert "{{" in code  # problem → hexagon
        assert '(["' in code  # method/result → stadium
        assert '["' in code  # step → rect


class TestRenderMermaid:

    @pytest.fixture
    def tmp_output(self, tmp_path):
        return tmp_path / "test_output.svg"

    def test_render_svg(self, tmp_output):
        if shutil.which("mmdc") is None:
            pytest.skip("mmdc not installed")
        code = graph_to_mermaid(SAMPLE_GRAPH)
        render_mermaid(code, str(tmp_output))
        assert tmp_output.exists()
        assert tmp_output.stat().st_size > 100

    def test_render_png(self, tmp_path):
        if shutil.which("mmdc") is None:
            pytest.skip("mmdc not installed")
        out = tmp_path / "test.png"
        code = graph_to_mermaid(SAMPLE_GRAPH)
        render_mermaid(code, str(out))
        assert out.exists()
        assert out.stat().st_size > 100

    def test_fallback_mmd_when_no_mmdc(self, tmp_path, monkeypatch):
        monkeypatch.setattr(shutil, "which", lambda _: None)
        out = tmp_path / "test.mmd"
        code = graph_to_mermaid(SAMPLE_GRAPH)
        render_mermaid(code, str(out))
        assert out.exists()
        content = out.read_text()
        assert "graph TD" in content

    def test_raises_when_no_mmdc_and_svg_requested(self, tmp_path, monkeypatch):
        monkeypatch.setattr(shutil, "which", lambda _: None)
        out = tmp_path / "test.svg"
        code = graph_to_mermaid(SAMPLE_GRAPH)
        with pytest.raises(RuntimeError, match="mmdc"):
            render_mermaid(code, str(out))
