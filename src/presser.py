import subprocess
from pathlib import Path
from io import BytesIO
from collections import deque

from PyPDF2 import PdfReader, PdfWriter

from src.data_types import PdfFile
from src.utils import get_pdf_page_count


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
    num_pages = get_pdf_page_count(output_pdf)

    return PdfFile(path=output_pdf, size=file_size, num_pages=num_pages)


def _write_pdf_to_bytesio(pdf: PdfWriter) -> BytesIO:
    output = BytesIO()
    pdf.write(output)
    output.seek(0)
    return output


def split_pdf(input_pdf: Path, output_dir: Path, max_size: int) -> list[PdfFile]:
    if max_size <= 0:
        raise ValueError("Max size must be positive.")

    if input_pdf.stat().st_size <= max_size:
        # No need to split
        return []

    input_pdf = PdfReader(str(input_pdf))

    output_pdfs = []

    next_pdf = PdfWriter()
    next_pdf_pages = 0

    # Add the pages to a queue
    pages = deque(input_pdf.pages)

    while pages:
        page = pages.popleft()
        next_pdf.add_page(page)
        next_pdf_pages += 1
        next_pdf_bytes = _write_pdf_to_bytesio(next_pdf)
        next_pdf_size = next_pdf_bytes.getbuffer().nbytes

        if next_pdf_size > max_size:
            if next_pdf_pages == 1:
                raise ValueError("PDF file is too big to split.")

            # Remove the last page
            old_pages = next_pdf.pages[:-1]
            next_pdf = PdfWriter()
            for _page in old_pages:
                next_pdf.add_page(_page)
            next_pdf_pages -= 1

            # Return the page to the queue
            pages.appendleft(page)

            # Write final version and get size
            next_pdf_bytes = _write_pdf_to_bytesio(next_pdf)
            next_pdf_size = next_pdf_bytes.getbuffer().nbytes

            # Save the PDF to disk
            output_pdf = output_dir / f"part_{len(output_pdfs)}.pdf"
            with open(output_pdf, "wb") as f:
                f.write(next_pdf_bytes.getbuffer())
            output_pdfs.append(
                PdfFile(path=output_pdf, size=next_pdf_size, num_pages=next_pdf_pages)
            )

            # Reset the next PDF
            next_pdf = PdfWriter()
            next_pdf_pages = 0

    # Make sure to save the last PDF
    if next_pdf_pages > 0:
        output_pdf = output_dir / f"part_{len(output_pdfs)}.pdf"
        with open(output_pdf, "wb") as f:
            f.write(next_pdf_bytes.getbuffer())
        output_pdfs.append(
            PdfFile(path=output_pdf, size=next_pdf_size, num_pages=next_pdf_pages)
        )

    return output_pdfs


def autofix_pdf(input_pdf: Path, output_dir: Path, max_size: int) -> list[PdfFile]:
    # First optimize the PDF, then check the size.
    # If the size is still too big, split the PDF into the output directory.
    optimized_pdf = run_ghostscript(input_pdf, output_dir / "optimized.pdf")
    if optimized_pdf.size > max_size:
        parts = split_pdf(optimized_pdf.path, output_dir, max_size)
        # Remove the optimized PDF
        optimized_pdf.path.unlink()
        return parts
    return [optimized_pdf]
