from typing import List
from .settings import Settings
from .line import Line
from .note import Note

class Project:
    def __init__(self, *, settings: Settings, lines: List[Line], notes: List[Note]):
        self.settings = settings
        self.lines = lines
        self.notes = notes