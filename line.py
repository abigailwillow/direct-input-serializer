import os
import json
import argparse

class Line:
    def __init__(self, row: int, spawn_time: int, start_time: int, end_time: int, despawn_time: int):
        self.row = row
        self.spawn_time = spawn_time
        self.start_time = start_time
        self.end_time = end_time
        self.despawn_time = despawn_time
        self.lyric_width = 1
        self.lyric_texture = ''

SPAWN_PADDING = 0.5
START_PADDING = 0.25

parser = argparse.ArgumentParser(description='Process JSON file and convert to line format')
parser.add_argument('file', type=str, help='JSON file to process')
args = parser.parse_args()

with open(args.file, 'r') as file:
    notes = json.load(file)

current_row = 0
lines = []
for note in notes:
    current_row = current_row % 4 + 1
    spawn_time = note['start_time'] - SPAWN_PADDING
    start_time = note['start_time'] - START_PADDING
    end_time = note['start_time'] + note['length']
    despawn_time = end_time + SPAWN_PADDING
    lines.append(Line(current_row, spawn_time, start_time, end_time, despawn_time))

file, extension = os.path.splitext(args.file)
args.file = f'{file}-lines{extension}'

with open(args.file, 'w') as file:
    file.write(json.dumps([line.__dict__ for line in lines], indent=4))