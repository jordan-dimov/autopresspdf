from pathlib import Path

import PySimpleGUI as sg

from src.data_types import PdfFile
from src.presser import autofix_pdf


def autofix(
    input_pdf: Path,
    output_dir: Path,
    max_size: float,
) -> list[PdfFile]:
    """
    Automatically optimize and split the PDF to fit under the size limit.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    max_size_bytes = int(max_size * 1e6)  # Convert MB to bytes
    return autofix_pdf(input_pdf, output_dir, max_size_bytes)


if __name__ == "__main__":
    file_types = (
        ("PDF Files", "*.pdf"),
    )
    file_input = [
        sg.Text("Choose a PDF file: "),
        sg.Input(enable_events=True, key="-FIN-"),
        sg.FileBrowse(file_types=file_types),
    ]
    folder_input = [
        sg.Text("Output folder: "),
        sg.Input(enable_events=True, key="-OUTFOLD-"),
        sg.FolderBrowse(),
    ]
    layout = [
        file_input,
        folder_input,
        [sg.Text("Max file size (MB): "), sg.InputText("10", key="-MAXSIZE-")],
        [sg.Button("Optimise", enable_events=True, key="-OK-")],
    ]

    window = sg.Window("AutoPressPDF", layout)

    while True:
        event, values = window.read()
        if event in ["Exit", sg.WIN_CLOSED]:
            print(f"Thank you for using AutoPressPDF!")
            break
        elif event == "-FIN-":
            file_path = values["-FIN-"]
            print(file_path)
        elif event == "-OUTFOLD-":
            out_folder = values["-OUTFOLD-"]
            print(out_folder)
        elif event == "-OK-":
            file_path = values["-FIN-"]
            out_folder = values["-OUTFOLD-"]
            print(f"Processing '{file_path}' into: {out_folder}")
            parts = autofix(Path(file_path), Path(out_folder), float(values["-MAXSIZE-"]))
            for i, part in enumerate(parts):
                print(part)

    window.close()

