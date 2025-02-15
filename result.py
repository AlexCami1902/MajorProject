import pygame # Import the pygame, sys & .csv libraries
import sys
import csv
import time
from main import state


pygame.init() # Initialize pygame
storage.pop('Ball', None)
# Get the last score entry
last_entry = storage[max(storage.keys())]  # Get value from the highest ball key

# Extract the score after the slash
last_score = int(last_entry.split('/')[1])
print(f"Total Score:  {last_score}")
state["last"] = last_score
print(state["last"])
screen = pygame.display.set_mode([600, 500])
base_font = pygame.font.Font(None, 32)
screen = pygame.display.set_mode()
screen_surface = pygame.display.get_surface()
# Set default colours to refer to later on
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
font = pygame.font.SysFont(None, 40)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# e.g draw_text("Batter Can Only Be Out [Run Out, etc,]", font, red, screen, 200, 50)
while True:
    screen.fill(white) # Sets the background colour to white.

    draw_text(f"Congratulations Team 1, You Win!", font, green, screen, 50,50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()