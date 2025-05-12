import pygame # Import the pygame, sys, time, os, numpy & .csv libraries
import sys
import csv
import time
import os
import random
import numpy
import shared # Import the shared.py file to access the shared variables
from shared import home_team_colour, away_team_colour

pygame.init() # Initialize pygame
state = {"last": None}
print(f"Received Data -> Home: {shared.home_team}, Away: {shared.away_team}, Location: {shared.match_location}") # Testing reciept of score
state["first_innings_score"] = 0 # Make the scores zero by default at the start of the game
state["second_innings_score"] = 0 
history = []  # Stores (overs, runs, wickets, extras) in that format for undo function later on

# Set default colours to refer to later on
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
homecolour = home_team_colour
awaycolour = away_team_colour
# Check if the colours are black, if so change them to red and green 
if awaycolour == pygame.Color(0, 0, 0, 255):
    awaycolour = red
if homecolour == pygame.Color(0, 0, 0, 255):
    homecolour = green
# Sets up various pre-game variables that are refered to and used throught the program, most of these global variables act as 'flags' for potnetial logic error i.e. 3rd innings
noball_status = False
bye_status = False
innings = 1
runs1 = 0
innings1 = 0
outcomes = [1, 2] # Set the possible outcomes for the first innings this simulates a coin flip as no one carrys a coin to games anymore
random_outcome = random.choice(outcomes) # Randomly selects a team to bat first
if random_outcome == 1:
    innings1 = 1
elif random_outcome == 2:
    innings1 = 2


# Sets up the display for Pygame as well as getting the dimensions of the display to go fullscreen
screen = pygame.display.set_mode()
screen_surface = pygame.display.get_surface()
x = screen_surface.get_width()
y = screen_surface.get_height()

screen = pygame.display.set_mode((x, y)) #Fullscreen


inningschange = True
# Set up font
font_regular = pygame.font.Font("fonts/PublicSans-Bold.ttf", 24)
font_bold = pygame.font.Font("fonts/PublicSans-Black.ttf", 30)
font = font_regular  # Start with regular rather than bold

# Game variables
runs = 0
extras = 0
wickets = 0
overs = 0.0
innings = 1 # Innings starts at 1 by default as there is no "0th" innings

storage = {"Ball":"Score"}

# Function to draw text
def draw_text(text, font, colour, surface, x, y):
    textobj = font.render(text, True, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Button class
class Button:
    HOVER_COLOUR = (200, 200, 200)  # Sets the colour for all buttons when they are hovered over

    def __init__(self, text, x, y, w, h, colour, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.default_colour = colour
        self.action = action

    def draw(self, screen): # Function to draw all of the buttons including the hover over colour
        mouse_pos = pygame.mouse.get_pos()
        draw_colour = Button.HOVER_COLOUR if self.rect.collidepoint(mouse_pos) else self.default_colour
        pygame.draw.rect(screen, draw_colour, self.rect)
        draw_text(self.text, font, white, screen, self.rect.x + 10, self.rect.y + 10)

    def is_clicked(self, pos): # If the button is clicked
        return self.rect.collidepoint(pos)

    def handle_event(self, event): # What to do when the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_clicked(event.pos):
                if self.action:
                    self.action()

# Actions for the various buttons, to be implemented as part of the class later on

def byes():
    global runs
    global extras
    global bye_status
    bye_status = True # Sets the bye status to true to let the code know to trigger the various events

def wide():
    global runs
    global extras
    global bye_status
    global noball_status
    bye_status = False # Sets the bye status to false to let the code know to trigger the various events
    noball_status = False # Sets the no-ball status to false to let the code know to trigger the various events
    runs += 1
    extras += 1

def noball():
    global runs
    global overs
    global extras
    global noball_status
    global bye_status
    bye_status = False # Sets the bye status to false to let the code know to trigger the various events
    noball_status = True # Sets the no-ball status to true to let the code know to trigger the various events
    runs += 1
    extras += 1
    
def start_innings():
    global extras
    global wickets
    global overs
    global innings
    global required
    global runs
    global inningschange

    # Sets the scores to 0
    extras = 0
    runs = 0
    wickets = 0
    overs = 0.0    
    innings += 1

def end_game():
    pygame.quit()

def scoring(ballscore):
    global runs
    global bye_status
    global extras
    int(ballscore)
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before changing
    if bye_status == True:
        extras += ballscore
        runs += ballscore
        bye_status = False
    else:
        runs += ballscore
    add_ball()

def add_wicket():
    global wickets
    global bye_status
    global noball_status
    bye_status = False # Sets the bye status to false to let the code know to trigger the various events
    noball_status = False # Sets the no-ball status to false to let the code know to trigger the various events
    if wickets < 10:
        history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before making any changes
        wickets += 1
        add_ball()
        if wickets == 10:
            read_score()
        
def add_ball():
    global overs, runs, wickets, extras
    global bye_status
    global noball_status
    bye_status = False # Sets the bye status to false to let the code know to trigger the various events
    noball_status = False # Sets the no-ball status to false to let the code know to trigger the various events
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Appends the history list for the undo fucntion with the new ball

    if overs % 1 == 0.5: # Uses the modulous operator to figure out the remainder of the overs
        overs += 0.5 # If the remainder is 0.5, it is the last ball of the over therefore, the code needs to add 0.5 to make it a new over
    else:
        overs += 0.1
    overs = round(overs, 1) # Round to 1 d.p. to correct for any very small errors in the division that can be multiplied and made larger

    backup(overs, runs, wickets)  # Send the results from this ball to the backup function

def undo():
    global overs, runs, wickets, extras, noball_status, bye_status

    for i in range(2):
        if history:  # Check that there is a pervious ball otherwise the function will not work
            prev_overs, prev_runs, prev_wickets, prev_extras, prev_noball, prev_bye = history.pop() # Gets the state of everything as recoreded in the history list. (Runs, extras, noballs, byes etc.)

            # If the last action was a no-ball or wide, just remove the extra without undoing the ball count
            if overs == prev_overs:  
                extras = prev_extras  # Remove the extra runs
                runs = prev_runs      # Remove the extra from the total runs
                noball_status = prev_noball
                bye_status = prev_bye
                print(f"Undo (extra): Extras={extras}, Runs={runs}")  # Debugging output REMOVE BEFORE SUBMISSION
            else:
                # Otherwise, undo everything (normal ball case)
                overs, runs, wickets, extras, noball_status, bye_status = prev_overs, prev_runs, prev_wickets, prev_extras, prev_noball, prev_bye
                print(f"Undo: Overs={overs}, Runs={runs}, Wickets={wickets}, Extras={extras}")  # Debugging output REMOVE BEFORE SUBMISSION

def result():
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script to place the .csv file in the same directory
    result_file_path = os.path.join(script_dir, 'result.py')  # Construct the full path to result.py
    try:
        with open(result_file_path) as f:
            code = f.read()
            exec(code)
    except FileNotFoundError:
        print("result.py not found. Please ensure the file exists in the directory.") # Making sure that all files are accesible in the directory

def backup(ball, runs, wicket):
    pass
    score = f"{wicket}/{runs}"
    storage[ball] = score
    make_a_csv() # Sends the backup of the file to the make_a_csv function to write the data to a .csv file

def make_a_csv():
    global innings
    if innings == 1: # Make 2 different .csv files for each innings
        with open('Innings1.csv', mode='w') as csvfile:
                fieldnames = ["Ball", "Score", f"Innings: {innings}"] # Set the column headers
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader() # Write the headers
                writer.writerows([{"Ball": k, "Score": v} for k, v in storage.items()]) # Convert storage dictionary to a list of dictionaries
    elif innings == 2:
        with open('Innings2.csv', mode='w') as csvfile:
                fieldnames = ["Ball", "Score", f"Innings: {innings}"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows([{"Ball": k, "Score": v} for k, v in storage.items()]) 

def read_score(): # The following code was modified by ChatGPT (See notes) as it was broken and was fixed by splitting the dictioanry, the intrinsic documentation is my own based on my understanding of the code
    # ChatGPT Modification Begins
    global storage
    storage.pop('Ball', None)

    if storage:
        # Get the last score entry for both innings
        last_entry = storage[max(storage.keys())]  # Get value from the highest ball key
        last_score = int(last_entry.split('/')[1])
        # ChatGPT Modification Ends
        print(f"Total Score: {last_score}")
        
        if innings == 1:
            state["first_innings_score"] = last_score # Set the innings score to the last score recorded by the system
        elif innings == 2:
            state["second_innings_score"] = last_score
            
        
        # Write the scores to a file so result.py can read them, this was the easiest way to transfer the scores accross the files.
        with open("final_scores.txt", "w") as f:
            f.write(f"{state['first_innings_score']},{state['second_innings_score']}")

    start_innings()

def toggle_bold(): # Function to toggle between regular and bold font
    global font
    global bold_enabled
    bold_enabled = not bold_enabled
    if bold_enabled:
        font = font_bold
    else:
        font = font_regular

# Create buttons for the various actions using the Button class created earlier

buttons = [ # (text, x, y, w, h, colour, action=None)
    Button("1", 50, 200, 40, 50, homecolour, lambda: scoring(1)),
    Button("2", 100, 200, 40, 50, homecolour, lambda: scoring(2)),
    Button("3", 150, 200, 40, 50, homecolour, lambda: scoring(3)),
    Button("4", 200, 200, 40, 50, homecolour, lambda: scoring(4)),
    Button("5", 250, 200, 40, 50, homecolour, lambda: scoring(5)),
    Button("6", 300, 200, 40, 50, homecolour, lambda: scoring(6)),
    Button("0", 350, 200, 40, 50, homecolour, add_ball),
    Button("N.B.",310, 300, 75, 50, awaycolour, noball),
    Button("Wide",395,300,90,50,awaycolour,wide),
    Button("Bye",495,300,90,50,awaycolour,byes),
    Button("Undo", 595, 300, 90, 50, awaycolour, undo),
    Button("Fudge Runs", 695, 300, 180, 50, awaycolour, wide),
    Button("Bold", 50, 400, 80, 50, black, toggle_bold)
]

bold_enabled = False

# Main game loop


while True:
    # If it's the second innings, set the required score to the runs scored by team 1 then add 1 to win
    if overs == 20:
        read_score()

    if bold_enabled == True: # Testing revealed that when the bold function is enabled the Wicket bututon would not display fully, this aims to fix this issue.
        WicketButton = Button("Wicket", 150, 300, 150, 50, awaycolour, add_wicket)
    elif bold_enabled == False:
        WicketButton = Button("Wicket", 200, 300, 100, 50, awaycolour, add_wicket)

    if overs < 1:
        run_rate = 0
    else:
        run_rate = runs/numpy.round(overs, 1) # Makes the runrate (1 d.p.)
        if run_rate > 36:
            run_rate = 36
    if overs % 1 == 0:
        if run_rate >= 36:
            run_rate = 36
        else:
            predicted = (run_rate * (20 - numpy.round(overs, 1)))+runs # Calculates the projected total at the end of every over
    
    final_score = state["last"]
    if innings == 2:
        final_score = state["first_innings_score"] + 1  # Target = first innings score + 1

    if innings == 1:
        if innings1 == 1:
            pygame.display.set_caption(f"{shared.home_team}'s Innings")
            innings2 = 1
            shared.first_batting_team = shared.home_team
            shared.second_batting_team = shared.away_team
        elif innings1 == 2:
            pygame.display.set_caption(f"{shared.away_team}'s Innings")
            innings2 = 2
            shared.first_batting_team = shared.away_team
            shared.second_batting_team = shared.home_team
    elif innings == 2:
        if innings2 == 1:
            pygame.display.set_caption(f"{shared.away_team}'s Innings")
        elif innings2 == 2:
            pygame.display.set_caption(f"{shared.home_team}'s Innings")

        
    if innings > 2:
        result()
    screen.fill(white)
    
    if innings == 2:
        if runs > state["first_innings_score"]:
            print(f"Innings: {innings}, Runs: {runs}, First Innings Score: {state['first_innings_score']}") # Debugging
            with open("final_scores.txt", "w") as f:
                f.write(f"{state['first_innings_score']},{runs}")
            time.sleep(.5)
            result()

    if noball_status:
        draw_text("Batter can only be out run out, hitting the ball twice or obstructing the field", font, red, screen, 200, 50) # Prints a warning about the quirks of a noball

    if bye_status:
        draw_text("How many byes?", font, red, screen, 200, 50) # Asks the user how many byes were scored
            

    
    draw_text(f"Run Rate: {round(run_rate, 2)}", font, black, screen, 50, 700) # Print the various calculations made
    
    draw_text(f"Predicted Score: {round(predicted, 0)}", font, black, screen, 50, 600)

    draw_text(f"Required: {final_score}", font, black, screen, 50, 500)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            noball_status = False
            # Check if buttons are clicked
            WicketButton.handle_event(event)
            for button in buttons:
                button.handle_event(event)

    # Draw the score display
    draw_text(f"Runs: {runs}", font, black, screen, 50, 0)
    draw_text(f"Innings: {innings}", font, black, screen, 1000, 0)
    if innings == 1:
        draw_text(f"{shared.first_batting_team}'s Innings", font, black, screen, 1000, 50)
    elif innings == 2:
        draw_text(f"{shared.second_batting_team}'s Innings", font, black, screen, 1000, 50)
    draw_text(f"Wickets: {wickets}", font, black, screen, 50, 50)
    draw_text(f"Overs: {overs}", font, black, screen, 50, 100)
    draw_text(f"Extras: {extras}", font, black, screen, 50, 150)

    # Draw buttons
    for button in buttons:
        button.draw(screen)
        WicketButton.draw(screen)

    # Update display
    pygame.display.update()
