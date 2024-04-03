import tkinter
from tkinter import filedialog
from pathlib import Path

def read_project(arguments):
    file: str = arguments.file
    output: str = arguments.output

    tkinter.Tk().withdraw()

    if not file:
        file = Path(filedialog.askopenfilename(filetypes=[('Project File', '*.json')]))

    output = file if not output else output

