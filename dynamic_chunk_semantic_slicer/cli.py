"""CLI for Dynamic Chunk Semantic Slicer."""
import argparse
from .core import DynamicChunkSlicer

def main():
    parser = argparse.ArgumentParser(description="Dynamic Chunk Semantic Slicer CLI")
    parser.add_argument("--demo", action="store_true", help="Run chunk slicing demo")
    args = parser.parse_args()

    sample = "# Overview" + chr(10) + chr(10) + "```python" + chr(10) + "def execute_agent():" + chr(10) + "    return True" + chr(10) + "```" + chr(10) + chr(10) + "More text follows."
    slicer = DynamicChunkSlicer(target_chunk_size=50)
    chunks = slicer.slice_document(sample)
    print(f"Generated {len(chunks)} intact chunks:")
    for c in chunks:
        print(f"  Chunk {c.chunk_id} (Code: {c.is_code}, Tokens: ~{c.token_estimate})")

if __name__ == "__main__":
    main()
