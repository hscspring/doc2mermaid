# doc2map

Convert documents to visual knowledge maps — powered by LLM + Mermaid.

```
Document Text → LLM Structure Extraction → Graph JSON → Mermaid → SVG/PNG
```

## Install

```bash
pip install doc2map

# Mermaid CLI for SVG/PNG rendering
npm install -g @mermaid-js/mermaid-cli
```

## Quick Start

### Python API

```python
from doc2map import doc_to_map

svg_path = doc_to_map(
    open("article.md").read(),
    output="map.svg",
    llm_base_url="https://api.openai.com/v1",
    llm_api_key="sk-...",
    llm_model="gpt-4o-mini",
)
```

### CLI

```bash
export DOC2MAP_BASE_URL=https://api.openai.com/v1
export DOC2MAP_API_KEY=sk-...
export DOC2MAP_MODEL=gpt-4o-mini

doc2map article.md -o map.svg
doc2map article.md -o map.png --theme dark
cat article.txt | doc2map - -o map.svg
```

## How It Works

1. **Extract**: LLM reads your document and extracts a graph structure (nodes + edges)
2. **Render**: The graph is converted to Mermaid diagram syntax with auto-styling
3. **Output**: Mermaid CLI renders the final SVG or PNG

### Node Types & Colors

| Type | Color | Use For |
|------|-------|---------|
| `problem` | Red | Problems, challenges, pain points |
| `idea` | Purple | Ideas, hypotheses, concepts |
| `method` | Blue | Methods, approaches, solutions |
| `step` | Cyan | Process steps, actions |
| `result` | Green | Results, outcomes, findings |
| `takeaway` | Yellow | Key takeaways, conclusions |

## Configuration

LLM settings via environment variables or function arguments:

| Env Var | Argument | Description |
|---------|----------|-------------|
| `DOC2MAP_BASE_URL` | `llm_base_url` | OpenAI-compatible API base URL |
| `DOC2MAP_API_KEY` | `llm_api_key` | API key |
| `DOC2MAP_MODEL` | `llm_model` | Model identifier |

Works with any OpenAI-compatible API (OpenAI, Claude, DeepSeek, local models, etc.).

## License

MIT
