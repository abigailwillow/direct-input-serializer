import argparse
from pathlib import Path
from commands import read_project, create_project

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

create_parser = subparsers.add_parser('create')
create_parser.add_argument('-f', '--file', type=Path)
create_parser.add_argument('-o', '--output', type=Path)
create_parser.set_defaults(function=create_project)

read_parser = subparsers.add_parser('read')
read_parser.add_argument('-f', '--file', type=Path)
read_parser.set_defaults(function=read_project)

arguments = parser.parse_args()
arguments.function(arguments) if hasattr(arguments, 'function') else parser.print_help()
