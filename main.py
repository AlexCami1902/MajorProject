import pygame # Import the pygame, sys, time, os, numpy & .csv libraries
import sys
import csv
import time
import os
import random
import numpy
import shared # Import the shared.py file to access the shared variables
from datetime import datetime
from shared import home_team_colour, away_team_colour

pygame.init() # Initialize pygame
state = {"last": None} # This sets the state of the game's dictionaty, this is used to store the last score of the game
pitch_background = pygame.image.load('Background2.jpg')    # Loads the background image
state["first_innings_score"] = 0 # Make the scores zero by default at the start of the game
state["second_innings_score"] = 0 
history = []  # Stores (overs, runs, wickets, extras) in that format for undo function later on
StartTime = datetime.now() # Gets the current time to display on the screen
# Set default colours to refer to later on
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
homecolour = home_team_colour # Sets the home team colour to the home_team_colour variable imported from shared.py
awaycolour = away_team_colour
# Check if the colours are black, if so change them to red and green 
if awaycolour == pygame.Color(0, 0, 0, 255):
    awaycolour = red
if homecolour == pygame.Color(0, 0, 0, 255):
    homecolour = green
# Sets up various pre-game variables that are refered to and used throught the program, most of these global variables act as 'flags' for potnetial logic error i.e. 3rd innings
noball_status = False # Sets the no-ball status to false by default, this is used to determine if a no-ball has been bowled
bye_status = False # Sets the bye status to false by default, this is used to determine if a bye has been scored
innings = 1 # Sets the innings to 1 by default, this is used to determine which innings is being played
runs1 = 0 # Sets the runs for the first innings to 0 by default
outcomes = [1, 2] # Set the possible outcomes for the first innings this simulates a coin flip as no one carrys a coin to games anymore


# Sets up the display for Pygame as well as getting the dimensions of the display to go fullscreen
screen = pygame.display.set_mode() # This sets the "screen" to the display
screen_surface = pygame.display.get_surface() # Gets the surface of the display
x = screen_surface.get_width() # Gets the width of the display
y = screen_surface.get_height() # Gets the height of the display

screen = pygame.display.set_mode((x, y)) # Sets the system to Fullscreen


inningschange = True # This is used to determine if the innings has changed, this is used to change the teams batting and bowling
# Set up font
font_regular = pygame.font.Font("fonts/PublicSans-Bold.ttf", 24) # Sets the regular font to PublicSans at size 24
font_bold = pygame.font.Font("fonts/PublicSans-Black.ttf", 30) # Sets the bold font to PublicSans at size 30
font = font_regular  # Start with regular rather than bold

# Game variables
runs = 0 # Sets the runs to 0
extras = 0 # Sets the extras to 0
wickets = 0 # Sets the wickets to 0
overs = 0.0 # Sets the overs to 0.0, this is used to determine the number of overs bowled
innings = 1 # Innings starts at 1 by default as there is no "0th" innings

storage = {"Ball":"Score"} # This is the format of the storage dictionary, this is used to store the score of each ball bowled in the innings

# Function to draw text
def draw_text(text, font, colour, surface, x, y):
    textobj = font.render(text, True, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# ----------------------------------------------------------------------------
# Button class
# ----------------------------------------------------------------------------
class Button:
    HOVER_COLOUR = (200, 200, 200)  # Sets the colour for all buttons when they are hovered over

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

    def handle_event(self, event):                                  # What to do when the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:                    # If the mouse button is pressed down
            if self.is_clicked(event.pos):                          # Checks if the button is clicked
                if self.action:                                     # If the button has an action assigned to it
                    self.action()                                   # Calls the action associated with the button
# ----------------------------------------------------------------------------
# Actions for the various buttons, to be implemented as part of the class later on

def byes(): # Byes function, this is used to add byes to the score
    global runs # Global runs, extras and the bye_status
    global extras
    global bye_status
    bye_status = True # Sets the bye status to true to let the code know to trigger the various events

def wide(): # Wides function, this is used to add wides to the score
    global runs # Global runs, extras, noball_status and the bye_status
    global extras
    global bye_status
    global noball_status
    bye_status = False # Sets the bye status to false to let the code know to trigger the various events
    noball_status = False # Sets the no-ball status to false to let the code know to trigger the various events
    runs += 1 # Adds 1 run to the score for the wide
    extras += 1 # Adds 1 extra to the extras for the wide

def noball(): # No-ball function, this is used to add no-balls to the score
    global runs # Global runs, extras, noball_status and the bye_status
    global overs
    global extras
    global noball_status
    global bye_status
    bye_status = False # Sets the bye status to false to let the code know to trigger the various events
    noball_status = True # Sets the no-ball status to true to let the code know to trigger the various events
    runs += 1 # Adds 1 run to the score for the no-ball
    extras += 1 # Adds 1 extra to the extras for the no-ball

def start_innings(): # Function to start a new innings, this is used to reset the variables for a new innings
    global extras # Gets the extras, runs, overs and innings variables for a new innings
    global runs
    global overs
    global innings
    global inningschange
    global storage
    global history
    global wickets
    extras = 0 # Resets the extras to 0
    runs = 0 # Resets the runs to 0
    wickets = 0 # Resets the wickets to 0
    overs = 0.0 # Resets the overs to 0.0
    innings += 1 # Increments the innings by 1
    inningschange = True # Sets the innings change to true so that the code knows to change the teams batting and bowling
    storage = {"Ball": "Score"} # Resets the storage dictionary for the new innings
    history.clear()  # Clear the history for the new innings
        

def end_game(): # When the game is over, this function is called to end the game
    pygame.quit() # Quits the pygame window

def scoring(ballscore):                                                             # Function to add the score of the ball to the runs, this is used to add the score of the ball to the runs
    global runs                                                                     # Global runs, overs, wickets, extras, noball_status and bye_status
    global bye_status
    global extras
    ballscore = int(ballscore)                                                      # Make the score for the ball an integer
    history.append((overs, runs, wickets, extras, noball_status, bye_status))       # Saves the current state of play before changing
    if bye_status == True:                                                          # If the bye status is true, this means that the user has selected to add byes to the score
        extras += ballscore                                                         # Adds the score of the ball to the extras
        runs += ballscore                                                           # Adds the score of the ball to the runs
        bye_status = False                                                          # Sets the bye status to false to let the code know to trigger the various events
    else:                                                                           # If the bye status is false, this means that the user has not selected to add byes to the score
        runs += ballscore                                                           # Adds the score of the ball to the runs
    add_ball()                                                                      # Calls the add_ball function to add a ball to the overs and update the score

def add_wicket():                                                                   # Function to add a wicket to the score, this is used to add a wicket to the score
    global wickets                                                                  # Global wickets, overs, runs, extras, noball_status and bye_status
    global bye_status
    global noball_status
    bye_status = False                                                              # Sets the bye status to false to let the code know to trigger the various events
    noball_status = False                                                           # Sets the no-ball status to false to let the code know to trigger the various events
    if wickets < 9:                                                                # If the number of wickets is less than 10, this means that there are still wickets left to take
        history.append((overs, runs, wickets, extras, noball_status, bye_status))   # Saves the current state of play before making any changes
        wickets += 1                                                                # Adds 1 to the number of wickets
        add_ball()                                                                  # Calls the add_ball function to add a ball to the overs and update the score
    elif wickets == 9:                                                             # If the number of wickets is 10, this means that there are no wickets left to take
        read_score()                                                                # Calls the read_score function to end the innings and display the score

def add_ball():
    global overs, runs, wickets, extras
    global bye_status
    global noball_status
    bye_status = False                                                              # Sets the bye status to false to let the code know to trigger the various events
    noball_status = False                                                           # Sets the no-ball status to false to let the code know to trigger the various events
    history.append((overs, runs, wickets, extras, noball_status, bye_status))       # Appends the history list for the undo function with the new ball
    if overs % 1 == 0.5:                                                            # Uses the modulous operator to figure out the remainder of the overs
        overs += 0.5                                                                # If the remainder is 0.5, it is the last ball of the over therefore, the code needs to add 0.5 to make it a new over
    else:
        overs += 0.1                                                                # If the remainder is not 0.5, it is a normal ball, so add 0.1 to the overs
    overs = round(overs, 1)                                                         # Round to 1 d.p. to correct for any very small errors in the division that can be multiplied and made larger
    backup(overs, runs, wickets)                                                    # Send the results from this ball to the backup function

def undo():                                                                                             # Defines the undo function for the undo button
    global overs # The following variables are all globaled to allow for the system to access them and compare them against the prev_VARIABLE
    global runs
    global wickets
    global extras
    global noball_status
    global bye_status

    for i in range(2):
        if history:                                                                                     # Check that there is a pervious ball to stop known error of the code going accross the innigns and causing many errors
            prev_overs, prev_runs, prev_wickets, prev_extras, prev_noball, prev_bye = history.pop()     # Gets the state of everything as recoreded in the history list. (Runs, extras, noballs, byes etc.)

            # If the last action was a no-ball or wide, just remove the extra without undoing the ball count
            if overs == prev_overs:  
                extras = prev_extras                        # Remove the extra runs
                runs = prev_runs                            # Remove the extra from the total runs
                noball_status = prev_noball
                bye_status = prev_bye
                wickets = prev_wickets                      # Reset the wickets to the previous state
            else:
            # Otherwise, undo everything (normal ball case)
                overs, runs, wickets, extras, noball_status, bye_status = prev_overs, prev_runs, prev_wickets, prev_extras, prev_noball, prev_bye

def result():
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script to place the .csv file in the same directory
    result_file_path = os.path.join(script_dir, 'result.py')  # Construct the full path to result.py
    try: # Try to open the result.py file and execute it
        with open(result_file_path) as f: # Open the result.py file
            code = f.read() # Read the contents of the file
            exec(code) # Execute the code in the file
    except FileNotFoundError: # If the file is not found, print an error message
        print("result.py not found. Please ensure the file exists in the directory.") # Making sure that all files are accesible in the directory

def backup(ball, runs, wicket):             # Function to backup the score of the ball bowled, this is used to store the score of each ball bowled in the innings
    score = f"{wicket}/{runs}"              # The score is stored in the format of wickets/runs, this is used to display the score of each ball bowled in the innings
    storage[ball] = score                   # The score is stored in the storage dictionary with the ball number as the key and the score as the value
    make_a_csv()                            # Sends the backup of the file to the make_a_csv function to write the data to a .csv file

def make_a_csv():                                                                           # Function to make a .csv file of the scores, this is used to write the scores of each ball bowled in the innings to a .csv file
    global innings                                                                          # Global innings to determine which innings is being played
    if innings == 1:                                                                        # Make 2 different .csv files for each innings
        with open('Innings1.csv', mode='w') as csvfile:                                     # Open the .csv file for writing
            fieldnames = ["Ball", "Score", f"Innings: {innings}"]                           # Set the column headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)                         # Create a DictWriter object to write the data to the .csv file
            writer.writeheader()                                                            # Write the headers
            writer.writerows([{"Ball": k, "Score": v} for k, v in storage.items()])         # Convert storage dictionary to a list of dictionaries
    elif innings == 2:
        with open('Innings2.csv', mode='w') as csvfile:
                fieldnames = ["Ball", "Score", f"Innings: {innings}"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows([{"Ball": k, "Score": v} for k, v in storage.items()]) 

def read_score():                                           # The following code was modified by ChatGPT (See notes) as it was broken and was fixed by splitting the dictioanry, the intrinsic documentation is my own based on my understanding of the code
    # ****ChatGPT Modification Begins****
    global storage
    storage.pop('Ball', None)

    if storage:
        # Get the last score entry for both innings, every ball is stored with a key value pair where the ball is stored as Ball:Score with the ball as the key and the score as the value, this helps print to the csv
        last_entry = storage[max(storage.keys())]           # Get value from the highest ball key
        last_score = int(last_entry.split('/')[1])
    # ****ChatGPT Modification Ends****
        print(f"Total Score: {last_score}")                 # Concatenates the last score to the string "Total Score: "
        
        if innings == 1:
            state["first_innings_score"] = last_score       # Set the innings score to the last score recorded by the system
        elif innings == 2:
            state["second_innings_score"] = last_score      # Set the second innings score to the last score recorded by the system
            
        
        # Write the scores to a file so result.py can read them, this was the easiest way to transfer the scores accross the files.
        with open("final_scores.txt", "w") as f:                                            # Open the final_scores.txt file to write the scores
            f.write(f"{state['first_innings_score']},{state['second_innings_score']}")      # Write the scores to the file

    start_innings() # Resets the game for the next innings, this is used to reset the variables for a new innings

def toggle_bold(): # Function to toggle between regular and bold font
    global font
    global bold_enabled
    bold_enabled = not bold_enabled
    if bold_enabled:
        font = font_bold
    else:
        font = font_regular

# Create buttons for the various actions using the Button class created earlier

buttons1 = [ # (text, x, y, w, h, colour, action=None)
    Button("1", 50, 200, 40, 50, homecolour, lambda: scoring(1)),                       # Button for 1 run
    Button("2", 100, 200, 40, 50, homecolour, lambda: scoring(2)),                      # Button for 2 runs
    Button("3", 150, 200, 40, 50, homecolour, lambda: scoring(3)),                      # Button for 3 runs
    Button("4", 200, 200, 40, 50, homecolour, lambda: scoring(4)),                      # Button for 4 runs
    Button("5", 250, 200, 40, 50, homecolour, lambda: scoring(5)),                      # Button for 5 runs
    Button("6", 300, 200, 40, 50, homecolour, lambda: scoring(6)),                      # Button for 6 runs
    Button(".", 350, 200, 40, 50, homecolour, add_ball),                                # Button for a dot ball (no runs scored)
    Button("Wide",410,300,90,50,awaycolour,wide),                                       # Button for wides
    Button("Bye",510,300,90,50,awaycolour,byes),                                        # Button for byes
    Button("Undo", 610, 300, 90, 50, awaycolour, undo),                                 # Button to undo the last action
    Button("Bold", 50, 400, 80, 50, black, toggle_bold)                                 # Button to toggle between regular and bold font
]

bold_enabled = False # Variable to determine if the bold font is enabled or not, this is used to toggle between the regular and the bold font
# Main game loop
while True:
    screen.blit(pitch_background, (0, 0))  # Draws the background
    if overs == 20: # When the innings/game is completed start the read score function to commence calculations
        read_score()
    if bold_enabled == True: # Testing revealed that when the bold function is enabled the Wicket bututon would not display fully, this aims to fix this issue.
        buttons2 = [ # (text, x, y, w, h, colour, action=None)
                Button("Wicket", 50, 300, 150, 50, awaycolour, add_wicket),             # Button for wicket
                Button("No Ball", 250, 300, 150, 50, awaycolour, noball),               # Button for no ball
                Button("Adjustments", 710, 300, 200, 50, awaycolour, wide)              # Button for adjustments (wides, byes, etc.)
        ]
    elif bold_enabled == False:
        buttons2 = [ # (text, x, y, w, h, colour, action=None)
                Button("Wicket", 50, 300, 100, 50, awaycolour, add_wicket),             # Button for wicket
                Button("No Ball", 300, 300, 100, 50, awaycolour, noball),               # Button for no ball
                Button("Adjustments", 710, 300, 180, 50, awaycolour, wide)              # Button for adjustments (wides, byes, etc.)
        ]
    if overs < 1:                                                       # If the overs are less than 1, this means that the game has just started
        run_rate = 0                                                    # Sets the run rate to 0 as no runs have been scored yet
    else:                                                               # If the overs are greater than or equal to 1, this means that the game has started and runs have been scored
        run_rate = runs/numpy.round(overs, 1)                           # Makes the runrate (1 d.p.)
        if run_rate > 36:                                               # If the run rate is greater than 36, this means there is an error so it sets to 36
            run_rate = 36                                               # This is the maximum run rate that can be achieved in a T20 game
    if overs % 1 == 0:                                                  # If the overs are a whole number, this means that the over has just finished
        if run_rate >= 36:                                              # If the run rate is greater than or equal to 36, this means that the game is going too fast
            run_rate = 36                                               # This is the maximum run rate that can be achieved in a T20 game
        else:
            predicted = (run_rate * (20 - numpy.round(overs, 1)))+runs  # Calculates the projected total at the end of every over
    
    final_score = state["last"]
    if innings == 2:
        final_score = state["first_innings_score"] + 1                  # If it's the second innings, set the required score to the runs scored by team 1 then add 1 to win
    
    # ----------------------------------------------------------------
    # Personified Scores Display
    # ----------------------------------------------------------------
    # The following code is used to display the personified scores of the teams, this is used to display the team names in a more readable format
    # The code checks the last letter of the team name and adds an apostrophe or 's' to the end of the team name depending on the last letter
    # If that is true, the team name is displayed correctly with the apostrophe or 's' at the end and then prints this in the caption bar and in the screen
    if innings == 1:
            if shared.first_batting_team.endswith("s"): # If the first batting team ends with an 's', display it without the 's
                personifiedname = f"{shared.first_batting_team}' Innings"
                pygame.display.set_caption(f"{personifiedname}")
            else:
                personifiedname = f"{shared.first_batting_team}'s Innings"
                pygame.display.set_caption(f"{personifiedname}")
    elif innings == 2:
            if shared.second_batting_team.endswith("s"): # If the second batting team ends with an 's', display it without the 's
                personifiedname = f"{shared.second_batting_team}' Innings"
                pygame.display.set_caption(f"{personifiedname}")

            else:
                personifiedname = f"{shared.second_batting_team}'s Innings"
                pygame.display.set_caption(f"{personifiedname}")
            
# ----------------------------------------------------------------
    
    if innings > 2: # If innings 2 has been competed then get the result function
        result()
    
    
    
    if innings == 2: # If it is the second innings, check if the runs scored are greater than the first innings score
        if runs > state["first_innings_score"]: # If the runs scored are greater than the first innings score, the game is over
            with open("final_scores.txt", "w") as f: # Open the final_scores.txt file to write the scores
                f.write(f"{state['first_innings_score']},{runs}")   # Write the scores to the file
            time.sleep(.5) # Sleep for 0.5 seconds to allow the user to see the score before the game ends
            result() # Call the result function to end the game and display the result
        draw_text(f"Required Runs: {final_score}", font, black, screen, 50, 500) # Draws the required runs to win the game
# -----------------------------------------------------------------------------------------------------------------------------
    if noball_status:  # If the system has identified that it is a no-ball
        draw_text("Batter can only be out run out, hitting the ball twice or obstructing the field", font, red, screen, 200, 500) # Prints a warning about the quirks of a noball

    if bye_status:
        draw_text("How many byes?", font, red, screen, 200, 500) # Asks the user how many byes were scored
    
    draw_text(f"Run Rate: {round(run_rate, 2)}", font, black, screen, 50, 700)              # Print the various calculations made
    draw_text(f"{personifiedname}", font, black, screen, 1000, 50)                          # Draw the first batting team name with the proper formatting
    draw_text(f"Predicted Score: {round(predicted, 0)}", font, black, screen, 50, 600)      # Draw the predicted score

    # Event handling
    for event in pygame.event.get(): # Get all the events from pygame
        if event.type == pygame.QUIT: # If the user clicks the close button, quit the game
            pygame.quit() 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: # If the user clicks the mouse button
            noball_status = False # Sets the no-ball status to false to let the code know to trigger the various events
            # Check if buttons are clicked
            for button in buttons1:
                button.handle_event(event) # Handle events for the first set of buttons
            for button in buttons2:
                button.handle_event(event) # Handle events for the second set of buttons
    # ----------------------------------------------------------------
    # Time Display
    # ----------------------------------------------------------------

    current_time = datetime.now() # Get the current time
    duration_td = current_time - StartTime # Calculate the duration of the game by subtracting the start time from the current time
    duration_hours = duration_td.seconds // 3600 # As duration is a 'time delta' in python (A difference between 2 values) it needs to be formatted apropriately, the following lines do just this
    duration_minutes = (duration_td.seconds % 3600) // 60 # Gets the minutes from the duration
    duration_seconds = duration_td.seconds % 60 # Gets the seconds from the duration
    duration_str = f"{duration_hours:02}:{duration_minutes:02}:{duration_seconds:02}" # Formats the duration as HH:MM:SS
    StartTime_string = StartTime.strftime('%H:%M')  # Format the start time for display
    current_time_string = current_time.strftime('%H:%M')  # Format the current time for display
    draw_text(f"Duration: {duration_str}", font, black, screen, 1000, 200) # Draw the duration of the game
    draw_text(f"Current Time: {current_time_string}", font, black, screen, 1000, 150) # Draw the current time of the game
    draw_text(f"Start Time: {StartTime_string}", font, black, screen, 1000, 100) # Draw the start time of the game
    
    # ----------------------------------------------------------------

    # Draw the score display
    draw_text(f"Runs: {runs}", font, black, screen, 50, 0)                          # Draws the runs scored so far
    draw_text(f"Innings: {innings}", font, black, screen, 1000, 0)                  # Draws the innings number
    draw_text(f"Wickets: {wickets}", font, black, screen, 50, 50)                   # Draw the wickets scored so far
    draw_text(f"Overs: {overs}", font, black, screen, 50, 100)                      # Draw the overs bowled so far
    draw_text(f"Extras: {extras}", font, black, screen, 50, 150)                    # Draw the extras scored so far

    # Draw buttons
    for button in buttons1:
        button.draw(screen)
    for button in buttons2:
        button.draw(screen)
    

    # Update display
    pygame.display.update()
