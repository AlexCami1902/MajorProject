import pygame # Importing libraries
import sys
import pygame_gui
import shared
import random
import time

pygame.init() # Initialize Pygame and Pygame GUI

# Fullscreen to get actual screen size
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_surface = pygame.display.get_surface()
x, y = screen_surface.get_width(), screen_surface.get_height()

ui_manager = pygame_gui.UIManager((x, y))
# Set default colours to refer to later on
white = (255, 255, 255) 
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Temporary smaller screen for UI
screen = pygame.display.set_mode([600, 500]) 
pygame.display.set_caption("Team Selector & Colour Picker") # Set the window title

clock = pygame.time.Clock() # Sets the clock for the game
base_font = pygame.font.Font("fonts/PublicSans-Bold.ttf", 24) # Load the base font for text rendering this is he same font used for the rest of the game
font = base_font  # Start with regular

global home_team_colour # Colour for the home team
global away_team_colour # Colour for the away team
home_team_colour = pygame.Color(0, 0, 0) # Default home team colour
away_team_colour = pygame.Color(0, 0, 0) # Default away team colour

def varpass(home, away, location): # Function to pass data to shared variables
    shared.home_team = home # Set the home team in shared variables
    shared.away_team = away # Set the away team in shared variables
    shared.match_location = location # Set the match location in shared variables

# ---------------------------------------------------------------------------------------------------------------------
# InputBox class for handling text input
# ---------------------------------------------------------------------------------------------------------------------

class InputBox:
    def __init__(self, x, y, w, h, placeholder="", name=""):
        self.rect = pygame.Rect(x, y, w, h) # Sets the rectangle for the input box
        self.color_passive = pygame.Color('chartreuse4') # Sets the passive colour for the input box i.e. the colour when the text is not actually in use
        self.color_active = pygame.Color('lightskyblue3') # Sets the active colour for the input box i.e. the colour when the text is being typed in
        self.color = self.color_passive # Sets the initial colour to the passive colour
        self.text = "" # The text that the user types in
        self.placeholder = placeholder # Placeholder text to show when the input box is empty
        self.name = name # Name of the input box, used for identification
        self.active = False # Whether the input box is active (being edited)
        self.cursor_visible = True # Whether the cursor is visible
        self.cursor_counter = 0 # Counter for cursor blinking
        self.cursor_position = 0 # Current position of the cursor

    def handle_event(self, event): # Defines how the input box handles events
        if event.type == pygame.MOUSEBUTTONDOWN: # If the mouse button is pressed
            self.active = self.rect.collidepoint(event.pos) # Check if the mouse is over the input box
            self.color = self.color_active  # Set the colour to active if the input box is clicked
            if self.active == True: # If the input box is active i.e. the text is being typed in
                self.color = self.color_active  # Set the colour to active
            else: # If the input box is not active
                self.color = self.color_passive # Set the colour to passive

        if self.active and event.type == pygame.KEYDOWN: # If the input box is active and a key is pressed
            if event.key == pygame.K_BACKSPACE: # If the backspace key is pressed
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_LEFT: # If the left arrow key is pressed
                self.cursor_position = max(0, self.cursor_position - 1) # Move the cursor left
            elif event.key == pygame.K_RIGHT: # If the right arrow key is pressed
                self.cursor_position = min(len(self.text), self.cursor_position + 1) # Move the cursor right 
            else:
                self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:] # Set the position of the cursor for easier viewing
                self.cursor_position += 1 # Add the typed character at the cursor position

    def update(self):
        # Update blinking cursor
        if self.active:
            self.cursor_counter += 1 # Increment the cursor counter
            if self.cursor_counter >= 30: # Blink every 30 frames
                self.cursor_counter = 0
                self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = False
            self.cursor_counter = 0

        # Width adapt to text
        # The following code was modified with the help of ChatGPT to adapt the width of the input box to the text length ***************
        text_surface = base_font.render(self.text or self.placeholder, True, (200, 0, 0) if self.text else (180, 180, 180)) # The surface for the text, using a different colour if the text is empty
        width = max(140, text_surface.get_width() + 10) # The width of the input box is set to a minimum of 140 pixels, or the width of the text plus some padding
        self.rect.w = width # Update the rectangle width to fit the text
        # End of ChatGPT modification *****************

    def draw(self, screen): # Draw the input box on the screen
        display_text = self.text if self.text else self.placeholder # Display the text or placeholder if the text is empty
        text_color = (255, 0, 0) if self.text else (150, 150, 150) # Set the text colour to red if the text is empty, otherwise set it to a light grey
        text_surface = base_font.render(display_text, True, text_color) # Render the text surface with the appropriate colour
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5)) # Draw the text on the screen at the input box position

        # Draw cursor (ChatGPT)
        if self.active and self.cursor_visible: # If the input box is active and the cursor is visible
            cursor_x = self.rect.x + 5 + base_font.size(self.text[:self.cursor_position])[0] # Calculate the x position of the cursor based on the text length
            cursor_y = self.rect.y + 5 # Calculate the y position of the cursor based on the input box position
            cursor_height = base_font.get_height() # Get the height of the font for the cursor height
            pygame.draw.line(screen, black, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2) # Draw the cursor as a vertical line
        # ChatGPT End
        pygame.draw.rect(screen, self.color, self.rect, 2) # Draw the input box rectangle with the current colour
# ---------------------------------------------------------------------------------------------------------------------


# Input boxes (x, y, w, h, placeholder, name)
input_boxes = [
    InputBox(100, 100, 140, 40, "Home Team", "Home"), # Input box for home team
    InputBox(100, 200, 140, 40, "Away Team", "Away"), # Input box for away team
    InputBox(100, 300, 140, 40, "Match Location", "Location"), # Input box for match location
]

# Defines actions for buttons
def pick_home_colour(): # Function to pick home team colour
    global current_picker_target
    global colour_picker
    colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),ui_manager,window_title="Pick Home Team Colour",initial_colour=home_team_colour   ) # Create a colour picker dialog for home team colour
    current_picker_target = "home" # Set the current picker target to home team

def pick_away_colour(): # Function to pick away team colour
    global current_picker_target
    global colour_picker
    colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),ui_manager,window_title="Pick Away Team Colour",initial_colour=away_team_colour) # Create a colour picker dialog for away team colour
    current_picker_target = "away" # Set the current picker target to away team


def submit_form(): # Function to submit the form
    home_team = input_boxes[0].text # Get the home team name from the input box
    away_team = input_boxes[1].text # Get the away team name from the input box
    match_location = input_boxes[2].text # Get the match location from the input box
    if home_team == "": # If the home team name is empty
        draw_text("Please enter a home team name.", font, red, screen, 100, 450) # Display an error message for thje user
        pygame.display.flip() # Update the display to show the error message
        time.sleep(1) # Wait for 1 second before clearing the message
        return # Restart the loop to allow the user to enter a home team name
    elif away_team == "": # If the away team name is empty
        draw_text("Please enter an away team name.", font, red, screen, 100, 450) # Display an error message for the user
        pygame.display.flip() # Update the display to show the error message
        time.sleep(1) # Wait for 1 second before clearing the message
        return
    elif match_location == "":
        draw_text("Please enter a match location.", font, red, screen, 100, 450) # Display an error message for the user
        pygame.display.flip() # Update the display to show the error message
        time.sleep(1) # Wait for 1 second before clearing the message
        return
    else:
        varpass(home_team, away_team, match_location) # If the imputs are valid, pass the data to shared variables
        import coinflip # Import the coinflip.py file to proceed to the next step

# ----------------------------------------------------------------------------
def draw_text(text, font, colour, surface, x, y): # Function to draw text on the screen
    textobj = font.render(text, True, colour) # Render the text with the specified font and colour
    textrect = textobj.get_rect() # Get the rectangle for the text object
    textrect.topleft = (x, y) # Set the position of the text rectangle to the specified x and y coordinates
    surface.blit(textobj, textrect) # Draw the text object on the surface at the specified position

class Button:
    HOVER_COLOUR = (180, 180, 180) # Defines the colour that the buttons are when the mouse is hovered over them, this is treated as an attribute and can be reffere

    def __init__(self, text, x, y, w, h, colour, action=None): # Initialises the button with the text, position, size, colour and action
        self.text = text # Text to be displayed on the button
        self.rect = pygame.Rect(x, y, w, h) # Creates a rectangle for the button with the position and size
        self.default_colour = colour # Colour of the button
        self.action = action # What the button actually does

    def draw(self, screen): # Function to draw all of the buttons including the hover over colour
        mouse_pos = pygame.mouse.get_pos() # Checks the position of the mouse
        draw_colour = Button.HOVER_COLOUR if self.rect.collidepoint(mouse_pos) else self.default_colour
        pygame.draw.rect(screen, draw_colour, self.rect) # Draws the button with the colour based on the mouse position
        draw_text(self.text, font, white, screen, self.rect.x + 10, self.rect.y + 10) # Draws the text on the button, offset by 10 pixels in both x and y directions for better visibility

    def is_clicked(self, pos): # If the button is clicked
        return self.rect.collidepoint(pos) # Checks if the mouse position is within the button's rectangle

    def handle_event(self, event): # What to do when the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN: # If the mouse button is pressed down
            if self.is_clicked(event.pos): # Checks if the button is clicked
                if self.action: # If the button has an action assigned to it
                    self.action() # Calls the action associated with the button
# ----------------------------------------------------------------------------

# UI Buttons
# (text, x, y, w, h, colour, action=None)

home_colour_button = Button("Home Colour", 450, 100, 180, 40, pygame.Color("dodgerblue"), pick_home_colour) # Button for picking home team colour
away_colour_button = Button("Away Colour", 450, 200, 180, 40, pygame.Color("orangered"), pick_away_colour) # Button for picking away team colour
submit_button = Button("Submit", 100, 400, 120, 50, pygame.Color("green"), submit_form) # Button for submitting the form

colour_picker = None # Variable to hold the colour picker dialog
current_picker_target = None # Variable to hold the current picker target (home or away team)
# ----------------------------------------------------------------------------

running = True # Main loop for the program
while running:
    time_delta = clock.tick(60) / 1000 # Limit the frame rate to 60 FPS and calculate time delta for smooth UI updates
    for event in pygame.event.get(): # Loop through all events in the event queue
        if event.type == pygame.QUIT: # If the quit event is triggered
            pygame.quit()   # Quit Pygame
            sys.exit()      # Exit the program

        for box in input_boxes: # Handle events for each input box
            box.handle_event(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED: # If a button is pressed
            home_colour_button.handle_event(event) # Handle events for home colour button
            away_colour_button.handle_event(event) # Handle events for away colour button
            submit_button.handle_event(event) # Handle events for submit button

        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED: # Handle events when the colour is picked by the user
            if current_picker_target == "home": # If the home team colour is picked
                shared.home_team_colour = event.colour # Set the home team colour to the picked colour
            elif current_picker_target == "away": # If the away team colour is picked
                shared.away_team_colour = event.colour # Set the away team colour to the picked colour
            current_picker_target = None # Reset the current picker target
        ui_manager.process_events(event) # Process events for the UI manager

    screen.fill((255, 255, 255)) # Fill the screen with white
    home_colour_button.draw(screen) # Draw home team buttons
    away_colour_button.draw(screen) # Draw away team buttons
    submit_button.draw(screen) # Draw buttons


    for box in input_boxes: # Update and draw input boxes
        box.update() # Update the box state
        box.draw(screen) # Draw the box on the screen

    pygame.draw.rect(screen, home_team_colour, (370, 100, 30, 30)) # Draw home team colour box
    pygame.draw.rect(screen, away_team_colour, (370, 200, 30, 30)) # Draw away team colour box
    home_colour_button.handle_event(event) # Handle button events
    away_colour_button.handle_event(event) # Handle button events
    submit_button.handle_event(event) # Handle button events
    ui_manager.process_events(event) # Process events for the UI manager

    ui_manager.update(time_delta) # Update the UI manager with the time difference
    ui_manager.draw_ui(screen) # Draw the screen UI elements
    pygame.display.flip() # Update the display constantly
