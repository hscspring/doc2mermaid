"""
doc2mermaid — Convert documents to visual knowledge maps.

Usage:
    from doc2mermaid import doc_to_map
    svg_path = doc_to_map("Your document text...", output="map.svg")
"""

from doc2mermaid.core import doc_to_map

__version__ = "0.1.1"
__all__ = ["doc_to_map"]
