import re
import json
import tkinter
from tkinter import filedialog
from pathlib import Path
from typing import List
from models import DualShock4Button, Note, NoteType

def create_project(arguments):
    file: str = arguments.file
    output: str = arguments.output

    tkinter.Tk().withdraw()

    if not file:
        file = Path(filedialog.askopenfilename(filetypes=[('Audacity Marker File', '*.txt')]))

    if not output:
        output = file.with_suffix('.json')

    markers: list[str]  = []
    with open(file, 'r') as file:
        markers = file.readlines()
    
    notes: List[Note] = []
    for marker in markers:
        matches = re.search(r'(\d+\.\d+)\s(\d+\.\d+)\s([\w+ ]+)', marker)
        start_time = float(matches.group(1))
        end_time = float(matches.group(2))
        button, type = str.split(matches.group(3), ' ') if ' ' in matches.group(3) else (matches.group(3), 'normal')

        notes.append(Note(
            type=NoteType(type.upper()),
            button=DualShock4Button(button.upper()),
            start_time=start_time,
            length=end_time - start_time
        ))
    
    with open(output, 'w') as file:
        file.write(json.dumps([note.__dict__ for note in notes], indent=4))
        print(f'Project created at {output}')
