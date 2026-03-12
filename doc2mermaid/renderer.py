"""
Graph JSON → Mermaid code → SVG/PNG rendering.
"""

import subprocess
import shutil
import tempfile
from pathlib import Path

from doc2mermaid.styles import wrap_node_text, generate_style_defs


def graph_to_mermaid(graph: dict, *, theme: str = "default") -> str:
    """Convert a graph dict to Mermaid diagram code.

    Args:
        graph: Dict with title, nodes, edges.
        theme: Mermaid theme name.

    Returns:
        Mermaid diagram string.
    """
    lines = ["graph TD"]

    # Node definitions
    for node in graph["nodes"]:
        node_line = wrap_node_text(node["id"], node["text"], node.get("type", "step"))
        lines.append(f"    {node_line}")

    # Edge definitions
    for src, tgt in graph["edges"]:
        lines.append(f"    {src} --> {tgt}")

    # Style definitions
    lines.append("")
    lines.extend(f"    {s}" for s in generate_style_defs(graph["nodes"]))

    return "\n".join(lines)


def render_mermaid(mermaid_code: str, output_path: str):
    """Render Mermaid code to SVG or PNG via mmdc (Mermaid CLI).

    Falls back to saving raw .mmd file if mmdc is not installed.

    Args:
        mermaid_code: The Mermaid diagram string.
        output_path:  Target file path (.svg, .png, or .mmd).
    """
    out = Path(output_path)
    ext = out.suffix.lower()

    mmdc = shutil.which("mmdc")

    if mmdc is None:
        # Fallback: save as .mmd text file
        mmd_path = out.with_suffix(".mmd")
        mmd_path.write_text(mermaid_code, encoding="utf-8")

        if ext == ".mmd":
            return

        raise RuntimeError(
            f"Mermaid CLI (mmdc) not found. Saved raw diagram to {mmd_path}\n"
            f"Install: npm install -g @mermaid-js/mermaid-cli"
        )

    with tempfile.NamedTemporaryFile(suffix=".mmd", mode="w", delete=False, encoding="utf-8") as f:
        f.write(mermaid_code)
        mmd_tmp = f.name

    try:
        cmd = [mmdc, "-i", mmd_tmp, "-o", str(out)]
        if ext == ".png":
            cmd.extend(["-s", "3"])  # 3x scale for crisp PNG
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise RuntimeError(f"mmdc failed:\n{result.stderr}")
    finally:
        Path(mmd_tmp).unlink(missing_ok=True)
