import os
import json
import argparse

BPM = 133
DIVISION = 16

parser = argparse.ArgumentParser(description='Process JSON file and snap values to nearest division')
parser.add_argument('file', type=str, help='JSON file to process')
args = parser.parse_args()

with open(args.file, 'r') as file:
    notes = json.load(file)

divisions = (60 / BPM) / DIVISION

for note in notes:
    note['start_time'] = note['start_time'] / divisions * divisions
    note['length'] = note['length'] / divisions * divisions

file, extension = os.path.splitext(args.file)
args.file = f'{file}-snapped{extension}'

with open(args.file, 'w') as file:
    file.write(json.dumps(notes, indent=4))