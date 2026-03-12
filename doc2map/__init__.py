"""
doc2map — Convert documents to visual knowledge maps.

Usage:
    from doc2map import doc_to_map
    svg_path = doc_to_map("Your document text...", output="map.svg")
"""

from doc2map.core import doc_to_map

__version__ = "0.1.0"
__all__ = ["doc_to_map"]
