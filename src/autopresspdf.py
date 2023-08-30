import typer
from pathlib import Path
from src.data_types import PdfFile
from src.presser import run_ghostscript, split_pdf, autofix_pdf

app = typer.Typer()

verbose_option = typer.Option(False, "--verbose", "-v", help="Enable verbose output")


@app.command()
def optimize(
    input_pdf: Path,
    output_pdf: Path = typer.Option(..., help="Optimized PDF output file"),
    verbose: bool = verbose_option,
) -> None:
    """
    Optimize the size of the PDF using GhostScript.
    """
    optimized_pdf = run_ghostscript(input_pdf, output_pdf)

    if verbose:
        size_MB = optimized_pdf.size / 1e6  # Convert bytes to MB
        typer.echo(
            f"Output is {size_MB:.2f} MB and has {optimized_pdf.num_pages} pages. Location: {optimized_pdf.path}"
        )


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
