import pygame
import sys
from utils import load_photos
from level import LevelPage

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

# Global variables to keep track of sound state
global_sound_on = True
global_music_on = True

class Game:
    def __init__(self):
        self.state = None
    
    def change_state(self, new_state):
        self.state = new_state

pygame.init()
pygame.mixer.init()

# Set up the screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Warship Combat")
clock = pygame.time.Clock()

# Load background image
background = load_photos("first", False)
heading_font = pygame.font.SysFont("Arial", 80, bold=True)
button_font = pygame.font.SysFont("Arial", 50, bold=True)

# Define the buttons for the main page
start_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 60)
settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 60)
exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 60)

# Load sounds
try:
    button_click_sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")
    background_music = "assets/sounds/background_music.mp3"
    
    # Play background music on loop if music is on
    if global_music_on:
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(loops=-1, start=0.0)
except:
    print("Warning: Sound files not found. Continuing without sound.")
    global_music_on = False

# Function to render text
def render_text(text, rect, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Function to lighten a color
def lighten_color(color, factor=1.2):
    return tuple(min(int(c * factor), 255) for c in color)

# Function to render a gradient effect on a button
def render_gradient_button(button_rect, color1, color2):
    if button_rect.width <= 0 or button_rect.height <= 0:
        return  
    gradient_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
    for i in range(button_rect.height):
        color = [
            int(color1[j] * (1 - i / button_rect.height) + color2[j] * (i / button_rect.height))
            for j in range(3)
        ]
        pygame.draw.line(gradient_surface, color, (0, i), (button_rect.width, i))
    screen.blit(gradient_surface, button_rect)

# Function to show settings page
def show_settings_page():
    from game_setting import GameSetting
    settings_page = GameSetting()
    settings_page.show_settings()

def main():
    game = Game() 
    running = True

    # Define the colors for the buttons and heading
    color1 = (255, 165, 0)  # Orange
    color2 = (255, 0, 0)    # Red
    
    # Create  colors for buttons
    start_button_color = lighten_color(color1)
    settings_button_color = lighten_color(color2)
    exit_button_color = lighten_color(color1, 1.1)

    while running:
        screen.blit(background, (0, 0))

        # Render heading with larger font size
        render_text("Space Warship Combat", 
                   pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 250, 400, 80),
                   heading_font, (255, 165, 0))

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Define the size increase for hover effect
        enlarge_size = 5

        # Button hover states
        start_button_enlarge = start_button.collidepoint(mouse_pos)
        settings_button_enlarge = settings_button.collidepoint(mouse_pos)
        exit_button_enlarge = exit_button.collidepoint(mouse_pos)

        # Handle Start button hover effect
        if start_button_enlarge:
            start_button_inflated = start_button.inflate(enlarge_size, enlarge_size)
        else:
            start_button_inflated = start_button

        # Handle Settings button hover effect
        if settings_button_enlarge:
            settings_button_inflated = settings_button.inflate(enlarge_size, enlarge_size)
        else:
            settings_button_inflated = settings_button

        # Handle Exit button hover effect
        if exit_button_enlarge:
            exit_button_inflated = exit_button.inflate(enlarge_size, enlarge_size)
        else:
            exit_button_inflated = exit_button

        # Draw gradient buttons
        render_gradient_button(start_button_inflated, color1, color2)
        render_text("Start Game", start_button_inflated, button_font, (0, 0, 0))

        render_gradient_button(settings_button_inflated, color2, color1)
        render_text("Settings", settings_button_inflated, button_font, (0, 0, 0))

        render_gradient_button(exit_button_inflated, color1, color2)
        render_text("Exit", exit_button_inflated, button_font, (0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    if global_music_on:
                        button_click_sound.play()
                    level_page = LevelPage(game)
                    level_page.show_level_page()
                elif settings_button.collidepoint(event.pos):
                    if global_music_on:
                        button_click_sound.play()
                    show_settings_page()
                elif exit_button.collidepoint(event.pos):
                    if global_music_on:
                        button_click_sound.play()
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

