import argparse

from pypdf import PdfReader

from app.rag.config import PDF_DIR
from app.rag.store import add_pdf_pages


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index PDFs for the DevOps interviewer"
    )
    parser.add_argument(
        "--file",
        help="Optional PDF filename inside the configured PDF folder",
    )
    args = parser.parse_args()

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    if args.file:
        if "/" in args.file or "\\" in args.file:
            raise SystemExit("Provide a PDF filename only, not a path.")
        files = [PDF_DIR / args.file]
    else:
        files = sorted(PDF_DIR.glob("*.pdf"))

    files = [
        path for path in files
        if path.is_file() and path.suffix.lower() == ".pdf"
    ]
    if not files:
        raise SystemExit(f"No PDF files found in {PDF_DIR}")

    failed = False
    for path in files:
        try:
            reader = PdfReader(str(path))
            pages = [
                (page_number, page.extract_text() or "")
                for page_number, page in enumerate(reader.pages, start=1)
            ]
            chunk_count = add_pdf_pages(path.name, pages)
            print(f"Indexed {chunk_count} chunks from {path.name}")
        except Exception as exc:
            failed = True
            print(f"Failed to index {path.name}: {exc}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()