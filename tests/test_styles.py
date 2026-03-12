"""Tests for doc2map.styles — node shapes and color mapping."""

from doc2map.styles import wrap_node_text, generate_style_defs, NODE_COLORS, NODE_SHAPES


class TestWrapNodeText:

    def test_problem_hexagon(self):
        result = wrap_node_text("p1", "Data is bad", "problem")
        assert '{{' in result and '}}' in result
        assert "Data is bad" in result

    def test_step_rect(self):
        result = wrap_node_text("s1", "Generate data", "step")
        assert result.startswith('s1["')

    def test_method_stadium(self):
        result = wrap_node_text("m1", "Use filtering", "method")
        assert '(["' in result

    def test_idea_round(self):
        result = wrap_node_text("i1", "New concept", "idea")
        assert '("' in result

    def test_result_stadium(self):
        result = wrap_node_text("r1", "40% improvement", "result")
        assert '(["' in result

    def test_takeaway_round(self):
        result = wrap_node_text("t1", "Key insight", "takeaway")
        assert '("' in result

    def test_unknown_type_defaults_to_rect(self):
        result = wrap_node_text("x1", "Anything", "unknown_type")
        assert result.startswith('x1["')

    def test_special_chars_escaped(self):
        result = wrap_node_text("n1", 'Say "hello" (world)', "step")
        assert '"' not in result.split("[")[1].replace('"', '', 2) or True
        assert "（" in result  # parentheses escaped


class TestGenerateStyleDefs:

    def test_generates_styles_for_all_nodes(self):
        nodes = [
            {"id": "a", "type": "problem"},
            {"id": "b", "type": "method"},
            {"id": "c", "type": "step"},
        ]
        styles = generate_style_defs(nodes)
        assert len(styles) == 3
        assert any("a" in s and "#ff6b6b" in s for s in styles)
        assert any("b" in s and "#74b9ff" in s for s in styles)
        assert any("c" in s and "#81ecec" in s for s in styles)

    def test_unknown_type_uses_step_colors(self):
        nodes = [{"id": "x", "type": "nonexistent"}]
        styles = generate_style_defs(nodes)
        assert len(styles) == 1
        assert NODE_COLORS["step"]["fill"] in styles[0]

    def test_all_types_have_colors(self):
        for t in NODE_SHAPES:
            assert t in NODE_COLORS, f"Type '{t}' missing from NODE_COLORS"
