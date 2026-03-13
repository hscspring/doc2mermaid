"""
LLM-based structure extraction: document text → Graph JSON.
"""

import json
import re

from openai import OpenAI


EXTRACT_PROMPT = """You are an expert at converting documents into visual knowledge maps.

Read the following document and extract its core structure.

Return a graph JSON with:

nodes:
- id (short snake_case identifier)
- type (one of: problem, idea, method, step, result, takeaway)
- text (short phrase, under 12 words)

edges:
- directional relationships between node ids: [source_id, target_id]

Rules:
1. Keep nodes under 10
2. Each node text must be concise (under 12 words)
3. Preserve the logical flow of the document
4. Prefer step-by-step pipelines when the document describes a process
5. Use appropriate node types to reflect the role of each concept
6. Node text MUST be in the SAME language as the input document (e.g. Chinese doc → Chinese nodes)
7. Return ONLY valid JSON, no markdown fences, no extra text

Output format:

{"title":"...","nodes":[{"id":"...","type":"...","text":"..."}],"edges":[["source_id","target_id"]]}

Document:

"""


def extract_graph(text: str, *, base_url: str, api_key: str, model: str) -> dict:
    """Call LLM to extract a graph structure from document text.

    Returns:
        Dict with keys: title, nodes, edges.
    """
    client = OpenAI(base_url=base_url, api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": EXTRACT_PROMPT + text},
        ],
        temperature=0.3,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content.strip()
    graph = _parse_graph_json(raw)
    _validate_graph(graph)
    return graph


def _parse_graph_json(raw: str) -> dict:
    """Parse LLM output into graph JSON, handling common formatting issues."""
    # Strip markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    # Try direct parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON object from mixed text
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Failed to parse graph JSON from LLM output:\n{raw[:500]}")


def _validate_graph(graph: dict):
    """Basic validation of the graph structure."""
    if "nodes" not in graph or "edges" not in graph:
        raise ValueError("Graph JSON must contain 'nodes' and 'edges' keys")

    if not graph["nodes"]:
        raise ValueError("Graph must have at least one node")

    node_ids = {n["id"] for n in graph["nodes"]}
    for edge in graph["edges"]:
        if len(edge) != 2:
            raise ValueError(f"Edge must be [source, target], got: {edge}")
        if edge[0] not in node_ids:
            raise ValueError(f"Edge source '{edge[0]}' not in nodes")
        if edge[1] not in node_ids:
            raise ValueError(f"Edge target '{edge[1]}' not in nodes")
