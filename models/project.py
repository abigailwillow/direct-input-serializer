from models import Settings
from models import Line
from models import Note
from typing import List

class Project:
    def __init__(self, settings: Settings, lines: List[Line], notes: List[Note]):
        self.settings = settings
        self.lines = lines
        self.notes = notes