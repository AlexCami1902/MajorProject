import pygame # Import the pygame, sys & .csv libraries
import sys
import csv
import time
import os
import numpy

pygame.init() # Initialize pygame
state = {"last": None}
# Initialize the scores in state
state["first_innings_score"] = 0
state["second_innings_score"] = 0

# Set default colours to refer to later on
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
noball_status = False
bye_status = False
innings = 1
required = 50
runs1 = 0

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
innings = 1

storage = {"Ball":"Score"}

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Button class
class Button:
    def __init__(self, text, x, y, w, h, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        draw_text(self.text, font, white, screen, self.rect.x + 10, self.rect.y + 10)

    def click(self):
        if self.action:
            self.action()

# Actions

def byes():
    global runs
    global extras
    global bye_status
    bye_status = True

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
    noball_status = True
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
        wickets += 1
        add_ball()
        if wickets == 10:
            read_score()
        
def add_ball():
    global overs
    global runs
    global wickets
    if overs % 1 == 0.5: # Use the modulous operator to figure out the remainder of the overs
        overs += 0.5 # If the remainder is 0.5, it is the last ball of the over therefore, add 0.5 to make it a new over
        overs = round(overs, 1) # Round to 1 d.p. to correct for any very small errors in the division
        backup(overs, runs, wickets) # Send the results from this ball to the backup function
    else:
        overs += 0.1
        overs = round(overs, 1)
        backup(overs, runs, wickets)

def result():
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    result_file_path = os.path.join(script_dir, 'result.py')  # Construct the full path to result.py
    try:
        with open(result_file_path) as f:
            code = f.read()
            exec(code)
    except FileNotFoundError:
        print("result.py not found. Please ensure the file exists in the directory.")

def backup(ball, runs, wicket):
    pass
    score = f"{wicket}/{runs}"
    storage[ball] = score
    print(storage)
    if ball > 10.0:
        make_a_csv()

def make_a_csv():
    pass
    with open('score_test.csv', mode='w') as csvfile:
            fieldnames = ["Ball", "Score"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(storage)

def read_score(): # The following code was modified by ChatGPT as it was broken
    global storage
    storage.pop('Ball', None)

    if storage:
        # Get the last score entry for both innings
        last_entry = storage[max(storage.keys())]  # Get value from the highest ball key
        last_score = int(last_entry.split('/')[1])
        print(f"Total Score: {last_score}")
        
        # Assuming we track both innings, for example:
        if innings == 1:
            state["first_innings_score"] = last_score
        elif innings == 2:
            state["second_innings_score"] = last_score
            
        
        # Write the scores to a file so result.py can read them
        with open("final_scores.txt", "w") as f:
            f.write(f"{state['first_innings_score']},{state['second_innings_score']}")

    start_innings()

# Create buttons

buttons = [ # (self, text, x, y, w, h, color, action=None)
    Button("1", 50, 200, 40, 50, green, run_1),
    Button("2", 100, 200, 40, 50, green, run_2),
    Button("3", 150, 200, 40, 50, green, run_3),
    Button("4", 200, 200, 40, 50, green, run_4),
    Button("5", 250, 200, 40, 50, green, run_5),
    Button("6", 300, 200, 40, 50, green, run_6),
    Button("0", 350, 200, 40, 50, green, add_ball),
    Button("Wicket", 220, 300, 100, 50, red, add_wicket),
    Button("N.B.",380, 300, 75, 50, red, noball),
    Button("Wide",500,300,90,50,red,wide),
    Button("Bye",600,300,90,50,red,byes)
]

# Main game loop
while True:
    # If it's the second innings, set the final score to the target
    if overs < 1:
        run_rate = 0
    else:
        run_rate = runs/numpy.round(overs, 1)
    if overs % 1 == 0:
        predicted = (run_rate * (20 - numpy.round(overs, 1)))+runs
    
    final_score = state["last"]
    if innings == 2:
        final_score = state["first_innings_score"] + 1  # Target = first innings score + 1

    if innings == 1:
        pygame.display.set_caption(f"First Innings")
    elif innings == 2:
        pygame.display.set_caption(f"Second Innings")
        
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
        draw_text("Batter Can Only Be Out [Run Out, etc,]", font, red, screen, 200, 50)

    if bye_status:
        draw_text("How Many Byes?", font, red, screen, 200, 50)

    
    draw_text(f"Run Rate: {round(run_rate, 2)}", font, black, screen, 50, 700)
    
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
