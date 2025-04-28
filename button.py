import pygame 
import sys
import random
import datetime


pygame.init()

screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MyCricket Scoring System")

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
gray = (200, 200, 200)

# Sets font
font = pygame.font.Font(None, 36)

def start_match():
    home_team = inputs()

# Original Button class
class Button:
    def __init__(self, text, colour, pos, action=None):
        self.text = text
        self.colour = colour
        self.pos = pos
        self.action = action
        self.rect = pygame.Rect(pos[0], pos[1], 150, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

StartButton = Button("Start Match", red, (50,200))
EndButton = Button("End Match", red, (250,200))



# Main loop
display_text = ""
while True:
    screen.fill(white)
    # Draw buttons
    StartButton.draw(screen)
    EndButton.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if StartButton.is_clicked(event.pos):
                import inputs as inputs
            elif EndButton.is_clicked(event.pos):
                screen.fill(blue)

    pygame.display.flip()
