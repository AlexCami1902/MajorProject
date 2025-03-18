import pygame
import sys
import shared
import datetime
n = 0
pygame.init()

clock = pygame.time.Clock()

# it will display on screen 
screen = pygame.display.set_mode([600, 500])

# basic font for user typed 
base_font = pygame.font.Font(None, 32)

def varpass(tobeconfirmed): # A test var
    print(f"{tobeconfirmed} 1")

class InputBox: # Create an inputbox class to be refered to later on
    def __init__(self, x, y, w, h, text="", name=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_passive = pygame.Color('chartreuse4')
        self.color_active = pygame.Color('lightskyblue3')
        self.color = self.color_passive
        self.text = text
        self.name = name
        self.active = False

    def handle_event(self, event):
        global n
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box, toggle the active state which moves the cursor.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box to give the user a visual key that text needs to be entered.
            self.color = self.color_active if self.active else self.color_passive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(f"{self.name}: {self.text}") # Prints the user's input to the terminal for backup
                    n = n+1
                    if n == 3:
                        home_team = input_boxes[0].text
                        away_team = input_boxes[1].text
                        match_location = input_boxes[2].text
                        varpass(home_team, away_team, match_location)  # Pass all three variables
                        import main  # Run main.py

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1] # Builds backspace functionality
                else:
                    self.text += event.unicode

    def update(self):
        # Resize the box if the text entered is too long.
        width = max(100, base_font.render(self.text, True, (255, 0, 0)).get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text to the screen.
        text_surface = base_font.render(self.text, True, (255, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the rectangle.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Create multiple input boxes from the class above


def varpass(home, away, location):
    shared.home_team = home
    shared.away_team = away
    shared.match_location = location
    print(f"Passing Data -> Home: {home}, Away: {away}, Location: {location}")

input_boxes = [
    InputBox(100, 100, 140, 32, "Home Team", "Home"),
    InputBox(100, 200, 140, 32, "Away Team", "Away"),
    InputBox(100, 300, 140, 32, "Match Location", "Location"),
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        for box in input_boxes:
            box.handle_event(event)

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    for box in input_boxes:
        box.update()
        box.draw(screen)

    pygame.display.flip()
    clock.tick(60)
