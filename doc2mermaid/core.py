"""
Core pipeline: document text → Graph JSON → Mermaid → SVG/PNG.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from doc2mermaid.extractor import extract_graph
from doc2mermaid.renderer import graph_to_mermaid, render_mermaid


def doc_to_map(
    text: str,
    output: str = "map.svg",
    *,
    llm_base_url: str = "",
    llm_api_key: str = "",
    llm_model: str = "",
    theme: str = "default",
) -> str:
    """Convert document text to a visual knowledge map.

    Args:
        text:         Document / blog / article text (plain text or Markdown).
        output:       Output file path. Extension determines format (.svg or .png).
        llm_base_url: OpenAI-compatible API base URL.
        llm_api_key:  API key.
        llm_model:    Model identifier.
        theme:        Mermaid theme ("default", "dark", "forest", "neutral").

    Returns:
        Absolute path to the generated image file.
    """
    base_url = llm_base_url or os.getenv("DOC2MERMAID_BASE_URL", "")
    api_key = llm_api_key or os.getenv("DOC2MERMAID_API_KEY", "")
    model = llm_model or os.getenv("DOC2MERMAID_MODEL", "")

    if not all([base_url, api_key, model]):
        raise ValueError(
            "LLM config required. Pass llm_base_url/llm_api_key/llm_model "
            "or set DOC2MERMAID_BASE_URL, DOC2MERMAID_API_KEY, DOC2MERMAID_MODEL env vars."
        )

    graph = extract_graph(text, base_url=base_url, api_key=api_key, model=model)
    mermaid_code = graph_to_mermaid(graph, theme=theme)

    output_path = Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    render_mermaid(mermaid_code, str(output_path))
    return str(output_path)
