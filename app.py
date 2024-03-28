import json
import pygame
from datetime import datetime
from dualshock4_button import DualShock4Button
from button_state import ButtonState
from input import Input

start_time = datetime.now()
inputs = []

def handle_input(button, state):
    print(f'{button.name} {state.name}')
    inputs.append(Input(button, datetime.now() - start_time, state))

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
            with open(f'inputs-{datetime.now()}.json', 'w') as file:
                file.write(json.dumps([input.__dict__ for input in inputs]))
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
