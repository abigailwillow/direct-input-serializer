import pygame
from dualshock4_buttons import DualShock4Buttons

running = True

pygame.init()
pygame.display.set_mode((1280, 720))
pygame.display.set_caption('DirectInput Serializer')
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
            if value == 0:
                print(f'{DualShock4Buttons(i).name} RELEASED')
                
            if value == 1:
                print(f'{DualShock4Buttons(i).name} PRESSED')      
            previous_values[i] = value

pygame.quit()