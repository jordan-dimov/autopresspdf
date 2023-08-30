from dataclasses import dataclass
from pathlib import Path


@dataclass
class PdfFile:
    path: Path
    size: int  # Size in bytes
    num_pages: int
