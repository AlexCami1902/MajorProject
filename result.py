import pygame # Import multiple libraries to run the result screen
import sys
import time
import shared
pygame.init() # Initialize pygame
screen = pygame.display.set_mode([600, 500]) # Set the size of the window
pygame.display.set_caption(f"Result") # Set the title of the window

white = (255, 255, 255) # Define colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
font = font = pygame.font.Font("fonts/Roboto-Bold.ttf", 24) # Load the font for text rendering


def draw_text(text, font, color, surface, x, y): # Function to draw text on the screen
    textobj = font.render(text, True, color) # Render the text with the specified font and color
    textrect = textobj.get_rect() # Get the rectangle of the text object
    textrect.topleft = (x, y) # Set the position of the text rectangle
    surface.blit(textobj, textrect)     # Draw the text on the surface at the specified position

while True:
    # Read the scores on every loop iteration
    # Various try/execpt statements to weed out potential errors that could occur and interfere with scoring system
    try:
        with open("final_scores.txt", "r") as f:  # Open the file to read the final scores
            first_innings_score, second_innings_score = map(int, f.read().strip().split(",")) # Read the scores and convert them to integers
    except FileNotFoundError: # If the file does not exist (i.e. it is the first innings), set scores to 0
        first_innings_score = 0 # Set first innings score to 0
        second_innings_score = 0   # Set second innings score to 0
    except ValueError:
        print("Error: Could not parse final_scores.txt") # If there is an error parsing the file, set scores to 0
        first_innings_score = 0 # Set first innings score to 0
        second_innings_score = 0 # Set second innings score to 0

    screen.fill(white) # Fill the screen with white color

    # Constantly monotoring the scores to see if there is a winner
    if first_innings_score > second_innings_score:
        draw_text(f" {shared.first_batting_team} Wins! ({first_innings_score} Runs vs {second_innings_score} Runs) ", font, green, screen, 50, 50) # If first innings score is greater, display the winner
    elif second_innings_score > first_innings_score:
        draw_text(f" {shared.second_batting_team} Wins! ({second_innings_score} Runs vs {first_innings_score} Runs) ", font, green, screen, 50, 50) # If second innings score is greater, display the winner
    else:
        draw_text(f" It's a Draw! ({first_innings_score} Runs vs {second_innings_score} Runs) ", font, green, screen, 50, 50) # If scores are equal, display a draw

    for event in pygame.event.get(): # Check for events in the pygame window
        if event.type == pygame.QUIT: # If the window is closed, exit the game
            pygame.quit()
            sys.exit()

    pygame.display.update()
    time.sleep(1)  # Wait 1 second before rechecking the file
