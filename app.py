import json
import atexit
import pygame
import time
from datetime import datetime
from dualshock4_button import DualShock4Button
from button_state import ButtonState
from input import Input

start_time = time.time_ns()
inputs = []

def handle_input(button, state):
    current_time = (time.time_ns() - start_time) // 1_000_000
    input = Input(button, current_time, state)
    inputs.append(input)
    print(f'({input.time} ms) {input.button} {input.state}')

def save_inputs():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f'output/inputs-{timestamp}.json', 'w') as file:
        file.write(json.dumps([input.__dict__ for input in inputs]))

atexit.register(save_inputs)

running = True

pygame.init()

pygame.joystick.init()

pygame.mixer.init()
pygame.mixer.music.load('karaoke.mp3')
pygame.mixer.music.play()

joystick = pygame.joystick.Joystick(0)
print(f'{joystick.get_name()} Connected')

previous_values = {i: 0 for i in range(joystick.get_numbuttons())}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(joystick.get_numbuttons()):
        value = joystick.get_button(i)
        if value != previous_values[i]:
            try:
                handle_input(DualShock4Button(i), ButtonState(value))
            except ValueError:
                continue
            previous_values[i] = value

pygame.quit()
