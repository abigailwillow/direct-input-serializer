from typing import List
from . import Settings, Line, Note

class Project:
    def __init__(self, *, settings: Settings, lines: List[Line], notes: List[Note]):
        self.settings = settings
        self.lines = lines
        self.notes = notes