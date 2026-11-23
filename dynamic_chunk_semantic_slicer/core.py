"""Core Dynamic Chunk Semantic Slicer implementation."""
import re
from typing import List, Dict, Any

class Chunk:
    def __init__(self, chunk_id: int, text: str, token_estimate: int, is_code: bool):
        self.chunk_id = chunk_id
        self.text = text
        self.token_estimate = token_estimate
        self.is_code = is_code

class DynamicChunkSlicer:
    def __init__(self, target_chunk_size: int = 500):
        self.target_chunk_size = target_chunk_size

    def slice_document(self, text: str) -> List[Chunk]:
        # Split on fenced code blocks first
        parts = re.split(r"(```[\s\S]*?```)", text)
        chunks = []
        chunk_counter = 0

        for part in parts:
            if not part.strip():
                continue
            is_code = part.startswith("```") and part.endswith("```")
            est_tokens = len(part.split())

            if is_code or est_tokens <= self.target_chunk_size:
                chunk_counter += 1
                chunks.append(Chunk(chunk_counter, part.strip(), est_tokens, is_code))
            else:
                # Split prose by paragraphs
                sep = chr(10) + chr(10)
                paragraphs = [p for p in part.split(sep) if p.strip()]
                curr_buf = []
                curr_tokens = 0
                for p in paragraphs:
                    p_toks = len(p.split())
                    if curr_tokens + p_toks > self.target_chunk_size and curr_buf:
                        chunk_counter += 1
                        chunks.append(Chunk(chunk_counter, sep.join(curr_buf).strip(), curr_tokens, False))
                        curr_buf = [p]
                        curr_tokens = p_toks
                    else:
                        curr_buf.append(p)
                        curr_tokens += p_toks
                if curr_buf:
                    chunk_counter += 1
                    chunks.append(Chunk(chunk_counter, sep.join(curr_buf).strip(), curr_tokens, False))

        return chunks
