import subprocess
from typing import List
from pathlib import Path

from src.data_types import PdfFile


def run_ghostscript(input_pdf: Path, output_pdf: Path) -> PdfFile:
    """
    Optimize a PDF file using GhostScript.
    """
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_pdf}",
        f"{input_pdf}",
    ]

    subprocess.run(cmd, check=True)

    # Collect file information
    file_size = output_pdf.stat().st_size
    # For now, we'll set the number of pages to a placeholder. Actual logic to count pages can be added later.
    num_pages = 0

    return PdfFile(path=output_pdf, size=file_size, num_pages=num_pages)


def split_pdf(input_pdf: Path, output_dir: Path, max_size: int) -> List[PdfFile]:
    # Implement PDF splitting logic here
    # Return a list of PdfFile instances
    pass


def autofix_pdf(input_pdf: Path, output_dir: Path, max_size: int):
    # Implement the 'autofix' algorithm here
    pass
