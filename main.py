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

screen = pygame.display.set_mode()
screen_surface = pygame.display.get_surface()
x = screen_surface.get_width()
y = screen_surface.get_height()

screen = pygame.display.set_mode((x, y))


inningschange = True
# Set up font
font = pygame.font.SysFont(None, 40)

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
    def __init__(self, text, x, y, w, h, colour, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = colour
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        draw_text(self.text, font, white, screen, self.rect.x + 10, self.rect.y + 10)

    def click(self):
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
    runs += 1
    extras += 1

def noball():
    global runs
    global overs
    global extras
    global noball_status
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

    extras = 0
    runs = 0
    wickets = 0
    overs = 0.0    
    innings += 1

def end_game():
    pygame.quit()

def run_1():
    global runs
    global bye_status
    global extras
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before changing
    if bye_status == True:
        extras += 1
        runs += 1
        bye_status = False
    else:
        runs += 1
    add_ball()

def run_2():
    global runs
    global bye_status
    global extras
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before changing
    if bye_status == True:
        extras += 2
        runs += 2
        bye_status = False
    else:
        runs += 2
    add_ball()

def run_3():
    global runs
    global bye_status
    global extras
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before changing
    if bye_status == True:
        extras += 3
        runs += 3
        bye_status = False
    else:
        runs += 3
    add_ball()

def run_4():
    global runs
    global bye_status
    global extras
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before changing
    if bye_status == True:
        extras += 4
        runs +=4
        bye_status = False
    else:
        runs += 4
    add_ball()

def run_5():
    global runs
    global bye_status
    global extras
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before changing
    if bye_status == True:
        extras += 5
        runs +=5
        bye_status = False
    else:
        runs += 5
    add_ball()

def run_6():
    global runs
    global extras
    global bye_status
    history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before changing
    if bye_status == True:
        extras += 6
        runs += 6
        bye_status = False
    else:
        runs += 6
    add_ball()

def add_wicket():
    global wickets
    if wickets < 10:
        history.append((overs, runs, wickets, extras, noball_status, bye_status)) # Saves the current state of play before making any changes
        wickets += 1
        add_ball()
        if wickets == 10:
            read_score()
        
def add_ball():
    global overs, runs, wickets, extras

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

# Create buttons for the various actions using the Button class created earlier

buttons = [ # (self, text, x, y, w, h, colour, action=None)
    Button("1", 50, 200, 40, 50, homecolour, run_1),
    Button("2", 100, 200, 40, 50, homecolour, run_2),
    Button("3", 150, 200, 40, 50, homecolour, run_3),
    Button("4", 200, 200, 40, 50, homecolour, run_4),
    Button("5", 250, 200, 40, 50, homecolour, run_5),
    Button("6", 300, 200, 40, 50, homecolour, run_6),
    Button("0", 350, 200, 40, 50, homecolour, add_ball),
    Button("Wicket", 220, 300, 100, 50, awaycolour, add_wicket),
    Button("N.B.",380, 300, 75, 50, awaycolour, noball),
    Button("Wide",500,300,90,50,awaycolour,wide),
    Button("Bye",600,300,90,50,awaycolour,byes),
    Button("Undo", 700, 300, 90, 50, awaycolour, undo)
]

# Main game loop
while True:
    # If it's the second innings, set the required score to the runs scored by team 1 then add 1 to win
    if overs < 1:
        run_rate = 0
    else:
        run_rate = runs/numpy.round(overs, 1) # Makes the runrate (1 d.p.)
    if overs % 1 == 0:
        predicted = (run_rate * (20 - numpy.round(overs, 1)))+runs # Calculates the projected total at the end of every over
    
    final_score = state["last"]
    if innings == 2:
        final_score = state["first_innings_score"] + 1  # Target = first innings score + 1

    if innings == 1:
        if innings1 == 1:
            pygame.display.set_caption(f"{shared.home_team}'s Innings") # Sets the title of the Pygame window to the team name for some customisation
            innings2 = 1
        elif innings1 == 2:
            pygame.display.set_caption(f"{shared.away_team}'s Innings")
            innings2 = 2
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
        draw_text("Batter Can Only Be Out [Run Out, etc,]", font, red, screen, 200, 50) # Prints a warning about the quirks of a noball

    if bye_status:
        draw_text("How Many Byes?", font, red, screen, 200, 50) # Asks the user how many byes were scored

    
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
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    button.click()

    # Draw the score display
    draw_text(f"Runs: {runs}", font, black, screen, 50, 0)
    draw_text(f"Innings: {innings}", font, black, screen, 1000, 0)
    draw_text(f"Wickets: {wickets}", font, black, screen, 50, 50)
    draw_text(f"Overs: {overs}", font, black, screen, 50, 100)
    draw_text(f"Extras: {extras}", font, black, screen, 50, 150)

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Update display
    pygame.display.update()
