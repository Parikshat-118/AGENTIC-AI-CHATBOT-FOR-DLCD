from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class TextChunk:
    pdf_id: str
    chunk_id: str
    page_number: int
    category: str
    title: str
    text: str


def chunk_pages(
    pdf_id: str,
    pages: List[str],
    category: str,
    title: str,
    max_chars: int = 1200,
    overlap: int = 200,
) -> List[TextChunk]:
    chunks: List[TextChunk] = []
    chunk_index = 0

    for page_idx, page_text in enumerate(pages):
        start = 0
        while start < len(page_text):
            end = min(len(page_text), start + max_chars)
            text_slice = page_text[start:end].strip()

            if text_slice:
                chunks.append(
                    TextChunk(
                        pdf_id=pdf_id,
                        chunk_id=f"{pdf_id}-{chunk_index}",
                        page_number=page_idx + 1,
                        category=category,
                        title=title,
                        text=text_slice,
                    )
                )
                chunk_index += 1

            if end == len(page_text):
                break
            start = end - overlap

    return chunks
