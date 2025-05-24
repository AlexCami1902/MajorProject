import pygame
import sys
import time
import shared
pygame.init()
screen = pygame.display.set_mode([600, 500])
pygame.display.set_caption(f"Result")
print(f"Received Data -> Home: {shared.home_team}, Away: {shared.away_team}, Location: {shared.match_location}") # Testing reciept of score

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
font = font = pygame.font.Font("fonts/Roboto-Bold.ttf", 24)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

while True:
    # Read the scores on every loop iteration
    # Various try/execpt statements to weed out potential errors that could occur and interfere with scoring system
    try:
        with open("final_scores.txt", "r") as f:  # Fix: Removed space in filename
            first_innings_score, second_innings_score = map(int, f.read().strip().split(","))
    except FileNotFoundError:
        first_innings_score = second_innings_score = 0  
    except ValueError:
        print("Error: Could not parse final_scores.txt")
        first_innings_score = second_innings_score = 0  

    screen.fill(white)

    # Constantly monotoring the scores to see if there is a winner
    if first_innings_score > second_innings_score:
        draw_text(f" {shared.first_batting_team} Wins! ({first_innings_score} Runs vs {second_innings_score} Runs) ", font, green, screen, 50, 50)
    elif second_innings_score > first_innings_score:
        draw_text(f" {shared.second_batting_team} Wins! ({second_innings_score} Runs vs {first_innings_score} Runs) ", font, green, screen, 50, 50)
    else:
        draw_text(f" It's a Draw! ({first_innings_score} Runs vs {second_innings_score} Runs) ", font, green, screen, 50, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    time.sleep(1)  # Wait 1 second before rechecking the file
