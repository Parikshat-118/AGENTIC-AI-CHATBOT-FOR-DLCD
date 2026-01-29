from langchain_core.documents import Document
from .pdf_loader import iter_pdfs, extract_pages
from .chunker import chunk_pages
from ..ai.vector_store import add_documents


def ingest():
    print(" Starting ingestion...")

    pdf_count = 0
    chunk_count = 0
    documents: list[Document] = []

    for pdf in iter_pdfs():
        pdf_count += 1
        print(f"\n Ingesting: {pdf.path.name}")

        pages = extract_pages(pdf.path)

        chunks = chunk_pages(
            pdf_id=pdf.path.stem,
            pages=pages,
            category=pdf.category,
            title=pdf.title,
        )

        if not chunks:
            print(" No chunks created")
            continue

        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk.text,
                    metadata={
                        "pdf": pdf.path.name,
                        "page": chunk.page_number,
                        "category": chunk.category,
                        "title": chunk.title,
                    },
                )
            )

        chunk_count += len(chunks)
        print(f"  Prepared {len(chunks)} chunks")

    print(f"\n Storing {len(documents)} chunks in vector DB...")
    add_documents(documents)

    print("\n Ingestion complete")
    print(f"PDFs ingested: {pdf_count}")
    print(f"Chunks stored: {chunk_count}")


if __name__ == "__main__":
    ingest()
