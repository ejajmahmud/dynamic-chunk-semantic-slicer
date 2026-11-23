"""Tests for DynamicChunkSlicer."""
import unittest
from dynamic_chunk_semantic_slicer.core import DynamicChunkSlicer

class TestDynamicChunkSlicer(unittest.TestCase):
    def test_code_block_preservation(self):
        doc = "Intro text." + chr(10) + chr(10) + "```python" + chr(10) + "x = 1" + chr(10) + "y = 2" + chr(10) + "```" + chr(10) + chr(10) + "Outro text."
        slicer = DynamicChunkSlicer(target_chunk_size=10)
        chunks = slicer.slice_document(doc)
        code_chunks = [c for c in chunks if c.is_code]
        self.assertEqual(len(code_chunks), 1)
        self.assertIn("```python", code_chunks[0].text)
