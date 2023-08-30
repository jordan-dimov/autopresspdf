from pathlib import Path

from PyPDF2 import PdfReader


def get_pdf_page_count(pdf_path: Path) -> int:
    """
    Returns the number of pages in a PDF.
    """
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        return len(pdf_reader.pages)
