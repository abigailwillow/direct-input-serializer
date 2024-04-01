import os
import json
import atexit
import pygame
import tkinter
from typing import List, Dict
from tkinter import filedialog
from datetime import datetime
from dotenv import load_dotenv

from models import DualShock4Button
from models import ButtonState
from models import Note
from models import NoteType

load_dotenv()

notes: List[Note] = []
last_pressed: Dict[DualShock4Button, int] = {button: 0 for button in DualShock4Button}

def handle_input(button: DualShock4Button, state: ButtonState):
    if state == ButtonState.PRESSED:
        last_pressed[button] = pygame.mixer.music.get_pos()
        print(f'({pygame.mixer.music.get_pos()} MS) {button.name.upper()} PRESSED')

    if state == ButtonState.RELEASED:
        hold_time = pygame.mixer.music.get_pos() - last_pressed[button]

        start_time = last_pressed[button]

        note = Note(NoteType.NORMAL if hold_time < int(os.getenv('HOLD_TRESHOLD', 500)) else NoteType.HOLD, button, start_time, hold_time)
        notes.append(note)
        print(f'({pygame.mixer.music.get_pos()} MS) {note.button.upper()} RELEASED (TYPE: {note.type.upper()}, START: {start_time} MS, LENGTH: {hold_time} MS)')

def serialize_inputs():
    if not notes:
        return
    
    if not os.path.exists('output'):
        os.makedirs('output')

    file_name = f'output/{os.path.splitext(os.path.basename(audio_file))[0]}-{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    with open(file_name, 'w') as file:
        file.write(json.dumps([input.__dict__ for input in notes], indent=4))

atexit.register(serialize_inputs)

running = True

root = tkinter.Tk()
root.withdraw()
audio_file = filedialog.askopenfilename(filetypes=[('Audio Files', '*.mp3 *.wav *.ogg')])

pygame.init()

pygame.joystick.init()

pygame.mixer.init()
pygame.mixer.music.load(audio_file)
pygame.mixer.music.set_volume(float(os.getenv('VOLUME', 1)))
pygame.mixer.music.play()
print(f'Playing {os.path.basename(audio_file)}')

window = pygame.display.set_mode((256, 256))
pygame.display.set_caption("DirectInput Serializer")

font = pygame.font.Font('fonts/FOT-RodinPro-DB.otf', 24)

joystick = pygame.joystick.Joystick(0)
print(f'{joystick.get_name()} Connected')

previous_values = {i: 0 for i in range(joystick.get_numbuttons())}

while running:
    window.fill((0, 0, 0))

    music_s = pygame.mixer.music.get_pos() // 1000
    music_min, music_sec = divmod(music_s, 60)
    
    pressed_buttons = []
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            try:
                pressed_buttons.append(DualShock4Button(i).name)
            except ValueError:
                continue

    music_text = font.render(f'{music_min:02}:{music_sec:02}', True, (255, 255, 255))
    ms_text = font.render(f'{pygame.mixer.music.get_pos()}', True, (255, 255, 255))

    window.blit(music_text, (16, 16))
    window.blit(ms_text, (16, 48))

    for i, button in enumerate(pressed_buttons):
        button_text = font.render(button, True, (255, 255, 255))
        window.blit(button_text, (16, 96 + i * 32))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()


    for i in range(joystick.get_numbuttons()):
        value = joystick.get_button(i)
        if value != previous_values[i]:
            try:
                handle_input(DualShock4Button(i), ButtonState(value))
            except ValueError:
                continue
            previous_values[i] = value

pygame.quit()

