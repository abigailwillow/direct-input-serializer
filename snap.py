import os
import json
import argparse

parser = argparse.ArgumentParser(description='Process JSON file and snap values to nearest division')
parser.add_argument('file', type=str, help='JSON file to process')
parser.add_argument('-b', '--bpm', type=int, help='BPM of the song')
parser.add_argument('-d', '--division', type=int, help='Division to snap to')
arguments = parser.parse_args()

with open(arguments.file, 'r') as file:
    notes = json.load(file)

divisions = (60 / arguments.bpm) / arguments.division

for note in notes:
    note['start_time'] = round(note['start_time'] / divisions) * divisions
    note['length'] = round(note['length'] / divisions) * divisions if note['type'] == 'hold' else 0

file, extension = os.path.splitext(arguments.file)
arguments.file = f'{file}-snapped{extension}'

with open(arguments.file, 'w') as file:
    file.write(json.dumps(notes, indent=4))