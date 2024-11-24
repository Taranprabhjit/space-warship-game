import pygame
import sys
from utils import load_photos

# Initialize constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

class Level5:
    def __init__(self, game=None):
        pygame.init()
        pygame.mixer.init()
        
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Level 5")
        
        # Load background
        self.background = load_photos("space_background", False)
        
        # Initialize fonts
        self.font = pygame.font.SysFont("Arial", 60, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 40, bold=True)
        
        # Sounds
        try:
            self.background_music = "assets/sounds/background_music.mp3"
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.play(loops=-1, start=0.0)
        except:
            print("Warning: Sound files not found. Continuing without sound.")

        # Buttons setup
        self.back_button_rect = pygame.Rect(30, 470, 150, 50)
        self.main_menu_button_rect = pygame.Rect(720, 470, 150, 50)
        
        # Game state
        self.state = "coming_soon"

    def render_text(self, text, x, y, color=(255, 255, 255)):
        """Render text centered at the given position."""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, rect, text, hover=False):
        """Draw a button with text."""
        color = (70, 70, 70) if hover else (50, 50, 50)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_input(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button_rect.collidepoint(event.pos):
                    from level import LevelPage
                    level_page = LevelPage(self.game)
                    level_page.show_level_page()
                

    def update(self):
        """Update game state. (Placeholder for future use)"""
        pass

    def draw(self, screen):
        """Draw the screen elements."""
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Render "Coming soon..."
        self.render_text("Coming soon...", SCREEN_WIDTH // 2 - self.font.size("Coming soon...")[0] // 2, SCREEN_HEIGHT // 2)
        
        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(self.back_button_rect, "Back", hover=self.back_button_rect.collidepoint(mouse_pos))

    def run(self):
        """Main game loop for Level 5."""
        while True:
            self.handle_input()
            self.update()
            self.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
