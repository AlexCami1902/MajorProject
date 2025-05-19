import pygame # Install required libs
import sys
import pygame_gui
import shared
import random
import time

# Set up pygame
pygame.init()
screen_width, screen_height = 600, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Coin Toss")

clock = pygame.time.Clock()
ui_manager = pygame_gui.UIManager((screen_width, screen_height))

# Fonts
font = pygame.font.Font("fonts/PublicSans-Bold.ttf", 24)

# Team colours (set elsewhere)
home_team_colour = shared.home_team_colour
away_team_colour = shared.away_team_colour

# Text rendering helper
def draw_text(text, font, colour, surface, x, y):
    textobj = font.render(text, True, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Basic button class
class Button:
    def __init__(self, text, x, y, w, h, colour, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = colour
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        draw_text(self.text, font, pygame.Color("azure"), screen, self.rect.x + 10, self.rect.y + 10)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(event.pos):
            if self.action:
                self.action()

# Coin toss logic
def cointossoutcome():
    global coinresult
    coinresult = random.choice(["Heads", "Tails"])
    print(f"Coin Toss Result: {coinresult}")
    if coinresult == "Heads":
        shared.first_batting_team = shared.home_team
        shared.second_batting_team = shared.away_team
        draw_text(f"{shared.home_team} won the toss", font, pygame.Color("orangered1"), screen, 50, 100)
        pygame.display.flip()
        time.sleep(1)

    else:
        shared.first_batting_team = shared.away_team
        shared.second_batting_team = shared.home_team
        draw_text(f"{shared.away_team} won the toss", font, pygame.Color("orangered1"), screen, 50, 100)
        pygame.display.flip()
        time.sleep(1)

    # Import main to continue (assuming main.py handles the switch)
    import main

# Create buttons
heads = Button("Heads", 450, 100, 120, 40, pygame.Color("dodgerblue"), cointossoutcome)
tails = Button("Tails", 450, 200, 120, 40, pygame.Color("orangered"), cointossoutcome)

# Main loop
running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        heads.handle_event(event)
        tails.handle_event(event)
        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    screen.fill(pygame.Color("gray1"))
    draw_text("Away team calls the toss", font, pygame.Color("orangered1"), screen, 50, 50)
    heads.draw(screen)
    tails.draw(screen)
    ui_manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
