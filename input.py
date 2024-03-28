from dualshock4_button import DualShock4Button
from button_state import ButtonState

class Input:
    def __init__(self, button: DualShock4Button, time: int, state: ButtonState, rapid: bool = False):
        self.button = button
        self.time = time
        self.state = state
        self.rapid = rapid