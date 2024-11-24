import pygame
import sys
from utils import load_photos
from level1 import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4
from level5 import Level5

# Global variables to track sound and music settings
global_sound_on = True
global_music_on = True

# Initialize constants and settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

class LevelPage:
    def __init__(self, game):
        pygame.init()
        pygame.mixer.init()
        
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Level Selection")
        
        # Load background
        self.background = load_photos("first", False)
        
        # Initialize fonts
        self.heading_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 40, bold=True)
        
        # Create buttons
        self.back_button_rect = pygame.Rect(30, 470, 100, 50)
        self.level_buttons = [
            pygame.Rect(375, 150, 150, 50),  # Level 1
            pygame.Rect(375, 220, 150, 50),  # Level 2
            pygame.Rect(375, 290, 150, 50),  # Level 3
            pygame.Rect(375, 360, 150, 50),  # Level 4
            pygame.Rect(375, 430, 150, 50)   # Level 5
        ]
        self.level_texts = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
        
        # Load sounds
        try:
            self.button_click_sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")
        except:
            print("Warning: Button click sound not found")
            global_sound_on = False

    def render_text(self, text, rect, font, color=(255, 255, 255)):
        """Renders text centered inside a rectangle."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_rounded_button(self, rect, color, border_radius=20):
        """Draw a rounded rectangle button with a specified color."""
        pygame.draw.rect(self.screen, color, rect, border_radius=border_radius)

    def start_level(self, level_num):
        """Start and run a specific level."""
        if level_num == 1:
            level = Level1(self.game)
        elif level_num == 2:
            level = Level2(self.game)
        elif level_num == 3:
            level = Level3(self.game)
        elif level_num == 4:
            level = Level4(self.game)
        elif level_num == 5:
            level = Level5(self.game)
        else:
            return

        running = True
        while running:
            # Handle level input
            level.handle_input()
            
            # Update game state
            level.update()
            
            # Draw everything
            level.draw(self.screen)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)

            # Check for game state changes
            if level.state in ["won", "lost"]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            running = False
                            return  # Return to level selection

    def show_level_page(self):
        """Show and handle the level selection page."""
        running = True
        while running:
            # Draw background
            self.screen.blit(self.background, (0, 0))
            
            # Render heading
            heading_rect = pygame.Rect((SCREEN_WIDTH - 400) // 2, 50, 400, 100)
            self.render_text("Select Level", heading_rect, self.heading_font, color=(255, 165, 0))
            
            # Handle hover effects and render buttons
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw level buttons
            for i, rect in enumerate(self.level_buttons):
                button_rect = rect.copy()
                
                # Apply hover effect
                if button_rect.collidepoint(mouse_pos):
                    button_rect.inflate_ip(20, 20)
                    self.draw_rounded_button(button_rect, (255, 100, 0))
                else:
                    self.draw_rounded_button(button_rect, (50, 50, 50))
                
                self.render_text(self.level_texts[i], button_rect, self.button_font, color=(255, 255, 255))
            
            # Draw back button
            self.draw_rounded_button(self.back_button_rect, (0, 0, 0))
            self.render_text("Back", self.back_button_rect, self.button_font, color=(255, 255, 255))
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check level button clicks
                    for i, rect in enumerate(self.level_buttons):
                        if rect.collidepoint(event.pos):
                            if global_sound_on:
                                self.button_click_sound.play()
                            self.start_level(i + 1)
                    
                    # Check back button click
                    if self.back_button_rect.collidepoint(event.pos):
                        if global_sound_on:
                            self.button_click_sound.play()
                        running = False
                        return  # Return to main menu
            
            pygame.display.flip()
            self.clock.tick(60)
