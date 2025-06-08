import pygame # Install required libs
import sys
import pygame_gui
import shared
import random
import time

# Set up pygame
pygame.init()
screen_width, screen_height = 600, 500 # Set the screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height)) # Create the screen
pygame.display.set_caption("Coin Toss") # Set the window title

clock = pygame.time.Clock() # Create the clock
ui_manager = pygame_gui.UIManager((screen_width, screen_height)) # Create the UI manager for pygame_gui

# Fonts
font = pygame.font.Font("fonts/PublicSans-Bold.ttf", 24)

# Team colours (set elsewhere) and read by this file from the shared.py file
home_team_colour = shared.home_team_colour
away_team_colour = shared.away_team_colour


def draw_text(text, font, colour, surface, x, y): # Function to render text on the screen
    textobj = font.render(text, True, colour) # Render the text with the specified font and colour
    textrect = textobj.get_rect() # Get the rectangle of the rendered text
    textrect.topleft = (x, y) # Set the position of the text rectangle
    surface.blit(textobj, textrect) # Draw the text on the surface at the specified position
# ---------------------------------------------------------------------------------------------------------------------
# Basic button class
# ---------------------------------------------------------------------------------------------------------------------

class Button:
    def __init__(self, text, x, y, w, h, colour, action=None): # Initialize the button with text, position, size, colour, and an optional action
        self.text = text # The text to display on the button
        self.rect = pygame.Rect(x, y, w, h) # The rectangle that defines the button's position and size
        self.colour = colour # The colour of the button
        self.action = action # The action to perform when the button is clicked

    def draw(self, screen): # Draw the button on the screen
        pygame.draw.rect(screen, self.colour, self.rect) # Draw the button rectangle with the specified colour
        draw_text(self.text, font, pygame.Color("azure"), screen, self.rect.x + 10, self.rect.y + 10) # Draw the text on the button with the defult colour 'azure'

    def is_clicked(self, pos): # Check if the button is clicked by checking if the mouse position is within the button's rectangle
        return self.rect.collidepoint(pos) 

    def handle_event(self, event): # Handle events for the button
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_clicked(event.pos): # Check if the mouse button is pressed and if the button is clicked
            if self.action: # If an action is defined, call it when the button is clicked this depends on the function tht is entered in the action seciton of the button
                self.action() # If an action is defined, call it when the button is clicked

# Coin toss logic
def cointossoutcome(): 
    global coinresult  # Global variable to store the result of the coin toss
    coinresult = random.choice(["Heads", "Tails"]) # Randomly choose between "Heads" and "Tails"
    if coinresult == "Heads": # If the result is Heads
        shared.first_batting_team = shared.home_team # Set the first batting team to the home team
        shared.second_batting_team = shared.away_team # Set the second batting team to the away team
        draw_text(f"{shared.home_team} won the toss \n {shared.home_team} are batting first", font, pygame.Color("orangered1"), screen, 50, 100) # Draw the result on the screen with the team name on who is batting first
        pygame.display.flip() # Update the display to show the result of the toss
        time.sleep(5) # Wait for 5 seconds to show the result to the user

    else:
        shared.first_batting_team = shared.away_team # If the result is Tails, set the first batting team to the away team
        shared.second_batting_team = shared.home_team # Set the second batting team to the home team
        draw_text(f"{shared.away_team} won the toss \n {shared.away_team} are batting first", font, pygame.Color("orangered1"), screen, 50, 100) # Draw the result on the screen with the team name on who is batting first
        pygame.display.flip() # Update the display to show the result of the toss
        time.sleep(5) # Wait for 5 seconds to show the result to the user

    # Import main to continue (assuming main.py handles the switch)
    import main

# Create buttons
heads = Button("Heads", 450, 100, 120, 40, pygame.Color("dodgerblue"), cointossoutcome) # Button for Heads with the action to call cointossoutcome
tails = Button("Tails", 450, 200, 120, 40, pygame.Color("orangered"), cointossoutcome) # Button for Tails with the action to call cointossoutcome

# Main loop
running = True # Flag to control the main loop
while running:
    time_delta = clock.tick(60) / 1000.0 # Error handling for the clock tick to ensure a consistent frame rate

    for event in pygame.event.get(): # Process events
        if event.type == pygame.QUIT: # If the quit event is triggered, exit the loop
            running = False # Exit the main loop

        heads.handle_event(event) # Handle events for the Heads button
        tails.handle_event(event) # Handle events for the Tails button
        ui_manager.process_events(event) # Process events for the UI manager

    ui_manager.update(time_delta) # Update the UI manager with the time delta to ensure smooth animations and transitions

    screen.fill(pygame.Color("gray1")) # Fill the screen with a background colour
    draw_text(f"{shared.away_team} calls the toss", font, pygame.Color("orangered1"), screen, 50, 50) # Draw the text indicating which team is calling the toss in an orange-red colour
    heads.draw(screen) # Draw the Heads button on the screen
    tails.draw(screen) # Draw the Tails button on the screen
    ui_manager.draw_ui(screen) # Draw the UI elements managed by pygame_gui

    pygame.display.flip() # Update the display

pygame.quit() # Quit pygame
sys.exit() # Exit the program cleanly
