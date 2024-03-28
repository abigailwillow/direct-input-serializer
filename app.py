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
    print(inputs[-1].__dict__)

running = True

pygame.init()

pygame.display.set_mode((1280, 720))
pygame.display.set_caption('DirectInput Serializer')

pygame.mixer.init()
pygame.mixer.music.load('karaoke.mp3')
pygame.mixer.music.play()

pygame.joystick.init()

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
            handle_input(DualShock4Button(i), ButtonState(value))
            previous_values[i] = value

pygame.quit()
