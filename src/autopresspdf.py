import typer
from pathlib import Path
from src.data_types import PdfFile
from src.presser import run_ghostscript, split_pdf, autofix_pdf

app = typer.Typer()


@app.command()
def optimize(
    input_pdf: Path,
    output_pdf: Path = typer.Option(..., help="Optimized PDF output file"),
) -> None:
    """
    Optimize the size of the PDF using GhostScript.
    """
    run_ghostscript(input_pdf, output_pdf)


@app.command()
def split(
    input_pdf: Path,
    output_dir: Path = typer.Option(..., help="Directory for splitted PDFs"),
    max_size: float = typer.Option(..., help="Maximum file size in MB"),
) -> None:
    """
    Split the PDF into parts, ensuring each part is under the size limit.
    """
    max_size_bytes = int(max_size * 1e6)  # Convert MB to bytes
    split_pdf(input_pdf, output_dir, max_size_bytes)


@app.command()
def autofix(
    input_pdf: Path,
    output_dir: Path = typer.Option(..., help="Directory for autofixed PDFs"),
    max_size: float = typer.Option(..., help="Maximum file size in MB"),
) -> None:
    """
    Automatically optimize and split the PDF to fit under the size limit.
    """
    max_size_bytes = int(max_size * 1e6)  # Convert MB to bytes
    autofix_pdf(input_pdf, output_dir, max_size_bytes)


if __name__ == "__main__":
    app()
