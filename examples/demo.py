"""
Quick demo: generate a knowledge map from a sample document.

Usage:
    # Set env vars first:
    export DOC2MAP_BASE_URL=https://api.qnaigc.com/v1
    export DOC2MAP_API_KEY=your-key
    export DOC2MAP_MODEL=minimax/minimax-m2.5

    python examples/demo.py
"""

from doc2map import doc_to_map

SAMPLE_DOC = """
# RolePlay Data Synthesis with Reward Model Filtering

## Problem
Generating high-quality RolePlay training data is expensive and inconsistent.
Manual annotation is slow, and naive LLM generation produces noisy data.

## Method
We propose a multi-candidate generation pipeline with Reward Model filtering.

### Steps
1. Generate multiple candidate dialogue trajectories using a base LLM
2. Score each candidate using a trained Reward Model
3. Apply Best-of-N selection to keep only the highest-scoring trajectory
4. Post-process to ensure formatting and safety compliance

## Results
This pipeline produces dialogue data with 40% higher human preference ratings
compared to single-pass generation, at only 3x the compute cost.

## Takeaways
- Reward Model filtering is a cost-effective alternative to human annotation
- Best-of-N with N=8 provides the best quality/cost tradeoff
"""

if __name__ == "__main__":
    path = doc_to_map(SAMPLE_DOC, output="output/demo_map.svg")
    print(f"Knowledge map saved to: {path}")
