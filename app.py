import argparse
from pathlib import Path
from commands import open_project
from commands import create_project

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=Path)
parser.add_argument('-o', '--output', type=Path)
parser.set_defaults(callback=open_project)

subparsers = parser.add_subparsers()

create_parser = subparsers.add_parser('create')
create_parser.add_argument('-f', '--file', type=Path, required=True)
create_parser.add_argument('-o', '--output', type=Path)
create_parser.set_defaults(callback=create_project)

arguments = parser.parse_args()
parser.callback(arguments)
