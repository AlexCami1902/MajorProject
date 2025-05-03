import pygame
import sys
import pygame_gui
import shared
import random
n = 0
pygame.init() # THIS MUST BE CALLED FIRST TO AVOID ERRORS
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
screen_surface = pygame.display.get_surface()
x, y = screen_surface.get_width(), screen_surface.get_height()

# Ensure UI manager uses correct size
ui_manager = pygame_gui.UIManager((x, y))
global home_team_colour, away_team_colour
home_team_colour = pygame.Color(0, 0, 0)
away_team_colour = pygame.Color(0, 0, 0)

screen = pygame.display.set_mode([600, 500])
pygame.display.set_caption("Team Input and Colour Picker")

clock = pygame.time.Clock()

base_font = pygame.font.Font("fonts/PublicSans-Bold.ttf", 24)

def varpass(home, away, location):
    shared.home_team = home
    shared.away_team = away
    shared.match_location = location
    print(f"Passing Data -> Home: {home}, Away: {away}, Location: {location}")
class InputBox:
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
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_passive
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"{self.name}: {self.text}")
                n = n+1
                if n == 3:
                    home_team = input_boxes[0].text
                    away_team = input_boxes[1].text
                    match_location = input_boxes[2].text
                    varpass(home_team, away_team, match_location)  # Pass all three variables
                    import main  # Run main.py
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    
    def update(self):
        width = max(100, base_font.render(self.text, True, (255, 0, 0)).get_width() + 10)
        self.rect.w = width
    
    def draw(self, screen):
        text_surface = base_font.render(self.text, True, (255, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

input_boxes = [
    InputBox(100, 100, 140, 32, "Home Team", "Home"),
    InputBox(100, 200, 140, 32, "Away Team", "Away"),
    InputBox(100, 300, 140, 32, "Match Location", "Location"),
]

home_colour_picker_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(400, 100, 100, 30), text='Pick Colour', manager=ui_manager)
away_colour_picker_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(400, 200, 100, 30), text='Pick Colour', manager=ui_manager)
colour_picker = None
current_picker_target = None  # Track which team's color is being changed
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
            if event.ui_element == home_colour_picker_button:
                colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400), ui_manager, window_title="Pick Home Team Colour", initial_colour=home_team_colour)
                current_picker_target = "home"
            elif event.ui_element == away_colour_picker_button:
                colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400), ui_manager, window_title="Pick Away Team Colour", initial_colour=away_team_colour)
                current_picker_target = "away"
        
        
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            if current_picker_target == "home":
                shared.home_team_colour = event.colour
            elif current_picker_target == "away":
                shared.away_team_colour = event.colour
            current_picker_target = None
        
        ui_manager.process_events(event)
    
    screen.fill((255, 255, 255))
    for box in input_boxes:
        box.update()
        box.draw(screen)
    
    pygame.draw.rect(screen, home_team_colour, (370, 100, 30, 30))
    pygame.draw.rect(screen, away_team_colour, (370, 200, 30, 30))
    
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    pygame.display.flip()
