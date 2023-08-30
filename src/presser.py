from typing import List
from pathlib import Path

from src.data_types import PdfFile


def run_ghostscript(input_pdf: Path, output_pdf: Path) -> PdfFile:
    # Implement GhostScript optimization here
    # Return a PdfFile instance
    pass


def split_pdf(input_pdf: Path, output_dir: Path, max_size: int) -> List[PdfFile]:
    # Implement PDF splitting logic here
    # Return a list of PdfFile instances
    pass


def autofix_pdf(input_pdf: Path, output_dir: Path, max_size: int):
    # Implement the 'autofix' algorithm here
    pass
