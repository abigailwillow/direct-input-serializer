from .dualshock4_button import DualShock4Button
from .note_type import NoteType

class Note:
    def __init__(self, *, type: NoteType, button: DualShock4Button, start_time: float, length: int):
        self.type = type.name.lower()
        self.button = button.name.lower()
        self.start_time = start_time
        self.length = length