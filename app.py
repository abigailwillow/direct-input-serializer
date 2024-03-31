import os
import json
import atexit
import pygame
import time
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from dualshock4_button import DualShock4Button
from button_state import ButtonState
from input import Input

COLOR_WHITE = (255, 255, 255)
START_TIME = time.time_ns()

inputs = []
ms_elapsed = 0

def handle_input(button, state):
    input = Input(button, ms_elapsed, state)
    inputs.append(input)
    print(f'({input.time} ms) {input.button} {input.state}')

def serialize_inputs():
    if not inputs:
        return
    
    if not os.path.exists('output'):
        os.makedirs('output')

    file_name = f'output/{os.path.splitext(os.path.basename(audio_file))[0]}-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    with open(file_name, 'w') as file:
        file.write(json.dumps([input.__dict__ for input in inputs]))

atexit.register(serialize_inputs)

running = True

root = tk.Tk()
root.withdraw()
audio_file = filedialog.askopenfilename(filetypes=[('Audio Files', '*.mp3 *.wav *.ogg')])

pygame.init()

pygame.joystick.init()

pygame.mixer.init()
pygame.mixer.music.load(audio_file)
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
    
    ms_elapsed = (time.time_ns() - START_TIME) // 1_000_000

    pressed_buttons = []
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            try:
                pressed_buttons.append(DualShock4Button(i).name)
            except ValueError:
                continue

    music_text = font.render(f'{music_min:02}:{music_sec:02}', True, COLOR_WHITE)
    ms_text = font.render(f'{ms_elapsed} ms', True, COLOR_WHITE)

    window.blit(music_text, (16, 16))
    window.blit(ms_text, (16, 48))

    for i, button in enumerate(pressed_buttons):
        button_text = font.render(button, True, COLOR_WHITE)
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
