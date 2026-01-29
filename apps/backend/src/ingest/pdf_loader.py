from pathlib import Path
from typing import Iterable, List
from dataclasses import dataclass
import fitz  # pymupdf

from ..config import get_settings

@dataclass
class PdfDocument:
    path: Path
    category: str
    title: str

_settings = get_settings()

def iter_pdfs() -> Iterable[PdfDocument]:
    # Normalize path to handle Windows backslashes correctly
    kb_dir: Path = _settings.KB_DIR.resolve()
    
    print(f"🔍 Scanning Knowledge Base at: {kb_dir}")

    if not kb_dir.exists():
        print(f" Error: The directory {kb_dir} does not exist.")
        return

    # Use a more explicit check for files
    found_any = False
    for path in kb_dir.rglob("*.pdf"):
        found_any = True
        # Calculate relative path to determine category
        try:
            rel = path.relative_to(kb_dir)
            # If PDF is in kb/logic-gates/file.pdf, category is logic-gates
            category = rel.parts[0] if len(rel.parts) > 1 else "general"
            title = path.stem.replace("_", " ")
            
            yield PdfDocument(path=path, category=category, title=title)
        except Exception as e:
            print(f"⚠️ Skipping {path.name} due to error: {e}")

    if not found_any:
        print(f" No .pdf files found in {kb_dir} or its subdirectories.")

def extract_pages(path: Path) -> List[str]:
    pages: List[str] = []
    try:
        with fitz.open(path) as doc:
            for page in doc:
                text = page.get_text("text") or ""
                if text.strip():
                    pages.append(text)
    except Exception as e:
        print(f" Could not read PDF {path}: {e}")
    return pages