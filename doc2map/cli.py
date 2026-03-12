"""
Command-line interface for doc2map.

Usage:
    doc2map input.md -o output.svg
    doc2map input.md -o output.png --theme dark
    cat article.txt | doc2map - -o map.svg
"""

import argparse
import sys

from doc2map.core import doc_to_map


def main():
    parser = argparse.ArgumentParser(
        prog="doc2mermaid",
        description="Convert documents to visual knowledge maps",
    )
    parser.add_argument(
        "input",
        help="Input file path, or '-' to read from stdin",
    )
    parser.add_argument(
        "-o", "--output",
        default="map.svg",
        help="Output file path (.svg or .png, default: map.svg)",
    )
    parser.add_argument(
        "--base-url",
        default="",
        help="LLM API base URL (or set DOC2MAP_BASE_URL env var)",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="LLM API key (or set DOC2MAP_API_KEY env var)",
    )
    parser.add_argument(
        "--model",
        default="",
        help="LLM model ID (or set DOC2MAP_MODEL env var)",
    )
    parser.add_argument(
        "--theme",
        default="default",
        choices=["default", "dark", "forest", "neutral"],
        help="Mermaid theme (default: default)",
    )

    args = parser.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()

    if not text.strip():
        print("Error: empty input", file=sys.stderr)
        sys.exit(1)

    try:
        result = doc_to_map(
            text,
            output=args.output,
            llm_base_url=args.base_url,
            llm_api_key=args.api_key,
            llm_model=args.model,
            theme=args.theme,
        )
        print(f"Generated: {result}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
