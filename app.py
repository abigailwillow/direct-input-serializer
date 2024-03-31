import json
import atexit
import pygame
import time
from datetime import datetime
from dualshock4_button import DualShock4Button
from button_state import ButtonState
from input import Input

WHITE = (255, 255, 255)

start_time = time.time_ns()
inputs = []

def handle_input(button, state):
    current_time = (time.time_ns() - start_time) // 1_000_000
    input = Input(button, current_time, state)
    inputs.append(input)
    print(f'({input.time} ms) {input.button} {input.state}')

def save_inputs():
    if not inputs:
        return
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

window = pygame.display.set_mode((256, 256))
pygame.display.set_caption("DirectInput Serializer")

font = pygame.font.Font('fonts/FOT-RodinPro-DB.otf', 24)

joystick = pygame.joystick.Joystick(0)
print(f'{joystick.get_name()} Connected')

previous_values = {i: 0 for i in range(joystick.get_numbuttons())}

while running:
    window.fill((0, 0, 0))

    music_ms = pygame.mixer.music.get_pos()
    music_s = music_ms // 1000
    music_min, music_sec = divmod(music_s, 60)
    
    ms_elapsed = (time.time_ns() - start_time) // 1_000_000

    pressed_buttons = []
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            try:
                pressed_buttons.append(DualShock4Button(i).name)
            except ValueError:
                continue

    music_text = font.render(f'{music_min:02}:{music_sec:02}', True, WHITE)
    ms_text = font.render(f'{ms_elapsed} ms', True, WHITE)

    window.blit(music_text, (16, 16))
    window.blit(ms_text, (16, 48))

    for i, button in enumerate(pressed_buttons):
        button_text = font.render(button, True, WHITE)
        window.blit(button_text, (16, 96 + i * 32))

    pygame.display.flip()

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
