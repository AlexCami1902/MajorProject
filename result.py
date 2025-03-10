import pygame
import sys

pygame.init()

# Read both innings' scores from the file
try:
    with open("final_scores.txt", "r") as f: # Opens the main.py file and reads the score from the first innings
        first_innings_score, second_innings_score = map(int, f.read().strip().split(",")) # Splits & Strips the score into a format that the computer can read
except FileNotFoundError:
    first_innings_score = second_innings_score = 0  # Default score if file is missing (In the case that the first innings has not been played)

screen = pygame.display.set_mode([600, 500])
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

while True:
    screen.fill(white)

    # Compares the two scores to determine the winner
    if first_innings_score > second_innings_score:
        draw_text(f"Team 1 Wins! ({first_innings_score} vs {second_innings_score})", font, green, screen, 50, 50) # Outcome 1: Team 1 Wins
    elif second_innings_score > first_innings_score:
        draw_text(f"Team 2 Wins! ({second_innings_score} vs {first_innings_score})", font, green, screen, 50, 50) # Outcome 2: Team 2 Wins
    else:
        draw_text(f"It's a Draw! ({first_innings_score} vs {second_innings_score})", font, green, screen, 50, 50) # Outcome 3: Tie

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
