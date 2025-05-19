import pygame
import sys
import pygame_gui
import shared
import random

pygame.init()

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

# Temporary smaller screen for UI (adjust as needed)
screen = pygame.display.set_mode([600, 500])
pygame.display.set_caption("Team Selector & Colour Picker")

clock = pygame.time.Clock()
base_font = pygame.font.Font("fonts/PublicSans-Bold.ttf", 24)
font = base_font  # Start with regular

global home_team_colour, away_team_colour
home_team_colour = pygame.Color(0, 0, 0)
away_team_colour = pygame.Color(0, 0, 0)

def varpass(home, away, location):
    shared.home_team = home
    shared.away_team = away
    shared.match_location = location
    print(f"Passing Data -> Home: {home}, Away: {away}, Location: {location}")

class InputBox:
    def __init__(self, x, y, w, h, placeholder="", name=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_passive = pygame.Color('chartreuse4')
        self.color_active = pygame.Color('lightskyblue3')
        self.color = self.color_passive
        self.text = ""
        self.placeholder = placeholder
        self.name = name
        self.active = False
        self.cursor_visible = True
        self.cursor_counter = 0
        self.cursor_position = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_passive

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f"{self.name}: {self.text}")
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_LEFT:
                self.cursor_position = max(0, self.cursor_position - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_position = min(len(self.text), self.cursor_position + 1)
            else:
                self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                self.cursor_position += 1

    def update(self):
        # Update blinking cursor
        if self.active:
            self.cursor_counter += 1
            if self.cursor_counter >= 30:
                self.cursor_counter = 0
                self.cursor_visible = not self.cursor_visible
        else:
            self.cursor_visible = False
            self.cursor_counter = 0

        # Width adapt to text
        text_surface = base_font.render(self.text or self.placeholder, True, (200, 0, 0) if self.text else (180, 180, 180))
        width = max(140, text_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        display_text = self.text if self.text else self.placeholder
        text_color = (255, 0, 0) if self.text else (150, 150, 150)
        text_surface = base_font.render(display_text, True, text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        # Draw cursor (ChatGPT)
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + base_font.size(self.text[:self.cursor_position])[0]
            cursor_y = self.rect.y + 5
            cursor_height = base_font.get_height()
            pygame.draw.line(screen, black, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
        #ChatGPT End
        pygame.draw.rect(screen, self.color, self.rect, 2)


# Input boxes (x, y, w, h, placeholder, name)
input_boxes = [
    InputBox(100, 100, 140, 40, "Home Team", "Home"),
    InputBox(100, 200, 140, 40, "Away Team", "Away"),
    InputBox(100, 300, 140, 40, "Match Location", "Location"),
]

# Defines actions for buttons
def pick_home_colour():
    global current_picker_target, colour_picker
    colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),ui_manager,window_title="Pick Home Team Colour",initial_colour=home_team_colour    )
    current_picker_target = "home"

def pick_away_colour():
    global current_picker_target, colour_picker
    colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),ui_manager,window_title="Pick Away Team Colour",initial_colour=away_team_colour)
    current_picker_target = "away"


def submit_form():    
    home_team = input_boxes[0].text
    away_team = input_boxes[1].text
    match_location = input_boxes[2].text
    if home_team == "" or away_team == "" or match_location == "":
        return
    else:
        varpass(home_team, away_team, match_location)
        import coinflip

# Function to draw text
def draw_text(text, font, colour, surface, x, y):
    textobj = font.render(text, True, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Button:
    def __init__(self, text, x, y, w, h, colour, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = colour
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
        draw_text(self.text, font, white, screen, self.rect.x + 10, self.rect.y + 10)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_clicked(event.pos):
                if self.action:
                    self.action()

# UI Buttons
# (text, x, y, w, h, colour, action=None)

home_colour_button = Button("Home Colour", 450, 100, 180, 40, pygame.Color("dodgerblue"), pick_home_colour)
away_colour_button = Button("Away Colour", 450, 200, 180, 40, pygame.Color("orangered"), pick_away_colour)
submit_button = Button("Submit", 100, 400, 120, 50, pygame.Color("green"), submit_form)

colour_picker = None
current_picker_target = None

running = True
while running:
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        for box in input_boxes:
            box.handle_event(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            home_colour_button.handle_event(event)
            away_colour_button.handle_event(event)
            submit_button.handle_event(event)


        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            if current_picker_target == "home":
                shared.home_team_colour = event.colour
            elif current_picker_target == "away":
                shared.away_team_colour = event.colour
            current_picker_target = None

        ui_manager.process_events(event)

    screen.fill((255, 255, 255))
    home_colour_button.draw(screen)
    away_colour_button.draw(screen)
    submit_button.draw(screen)


    for box in input_boxes:
        box.update()
        box.draw(screen)

    pygame.draw.rect(screen, home_team_colour, (370, 100, 30, 30))
    pygame.draw.rect(screen, away_team_colour, (370, 200, 30, 30))
    home_colour_button.handle_event(event)
    away_colour_button.handle_event(event)
    submit_button.handle_event(event)
    ui_manager.process_events(event)

    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    pygame.display.flip()
