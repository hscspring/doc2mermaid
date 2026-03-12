"""
Node type → visual style mapping for Mermaid rendering.
"""

# Mermaid node shapes by type
# round: (text), stadium: ([text]), subroutine: [[text]]
# hexagon: {{text}}, parallelogram: [/text/], trapezoid: [/text\]
NODE_SHAPES = {
    "problem":  "hexagon",     # {{text}}
    "idea":     "round",       # (text)
    "method":   "stadium",     # ([text])
    "step":     "rect",        # [text]
    "result":   "stadium",     # ([text])
    "takeaway": "round",       # (text)
}

# Mermaid style colors by type
NODE_COLORS = {
    "problem":  {"fill": "#ff6b6b", "stroke": "#c0392b", "color": "#fff"},
    "idea":     {"fill": "#a29bfe", "stroke": "#6c5ce7", "color": "#fff"},
    "method":   {"fill": "#74b9ff", "stroke": "#0984e3", "color": "#fff"},
    "step":     {"fill": "#81ecec", "stroke": "#00cec9", "color": "#2d3436"},
    "result":   {"fill": "#55efc4", "stroke": "#00b894", "color": "#2d3436"},
    "takeaway": {"fill": "#ffeaa7", "stroke": "#fdcb6e", "color": "#2d3436"},
}


def wrap_node_text(node_id: str, text: str, node_type: str) -> str:
    """Wrap node text in the appropriate Mermaid shape syntax."""
    shape = NODE_SHAPES.get(node_type, "rect")

    # Escape special Mermaid characters
    safe_text = text.replace('"', "'").replace("(", "（").replace(")", "）")

    if shape == "hexagon":
        return f'{node_id}{{{{"{safe_text}"}}}}'
    elif shape == "round":
        return f'{node_id}("{safe_text}")'
    elif shape == "stadium":
        return f'{node_id}(["{safe_text}"])'
    else:
        return f'{node_id}["{safe_text}"]'


def generate_style_defs(nodes: list) -> list[str]:
    """Generate Mermaid style definitions for all nodes."""
    lines = []
    for node in nodes:
        nid = node["id"]
        ntype = node.get("type", "step")
        colors = NODE_COLORS.get(ntype, NODE_COLORS["step"])
        lines.append(
            f'style {nid} fill:{colors["fill"]},'
            f'stroke:{colors["stroke"]},color:{colors["color"]}'
        )
    return lines
