import pygame
import sys
from utils import load_photos

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
PLANE_SPEED = 5

class GameSetting:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for sound

        self.screen = pygame.display.set_mode((900, 550))  # Screen dimensions
        pygame.display.set_caption("Settings")

        # Load the background image
        self.background = pygame.image.load("C:\\Users\\taran\\Desktop\\SpaceWarshipCombat-Game\\assets\\photos\\first.png")
        self.background = pygame.transform.scale(self.background, (900, 550))  # Scale to fit the screen

        # Define font sizes
        self.heading_font = pygame.font.SysFont("Arial", 80, bold=True)  # Larger font for the heading
        self.button_font = pygame.font.SysFont("Arial", 40, bold=True)  # Font for button text
        self.normal_font = pygame.font.SysFont("Arial", 30, bold=True)  # Normal font for the label text (Sound)

        # Define the back button rectangle (black background)
        self.back_button_rect = pygame.Rect(30, 470, 100, 50)  # Bottom-left corner, 100x50 size

        # Define the sound toggle buttons (ON/OFF)
        self.sound_button_rect = pygame.Rect(450, 250, 100, 50)  # Button for ON/OFF sound toggle
        self.mute_button_rect = pygame.Rect(450, 320, 100, 50)  # Button for ON/OFF mute toggle
        self.sound_on = True  # Default state for sound (ON)
        self.music_on = True  # Default state for music (playing)
        self.click_sound_muted = False  # Default state for mute button (OFF, meaning sound is not muted)

        # Load the sound effect for button click
        self.button_click_sound = pygame.mixer.Sound("C:\\Users\\taran\\Desktop\\SpaceWarshipCombat-Game\\assets\\sounds\\button_click.mp3")

        # Load background music and play it initially
        self.background_music = "C:\\Users\\taran\\Desktop\\SpaceWarshipCombat-Game\\assets\\sounds\\background_music.mp3"
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(loops=-1, start=0.0)  # Play indefinitely

        # Initially unmute the click sound if the mute button is OFF
        if self.click_sound_muted == False:
            pygame.mixer.Sound.set_volume(self.button_click_sound, 1.0)  # Unmute the click sound

    def render_text(self, text, rect, font, color=(255, 255, 255)):
        """Renders text centered inside a rectangle."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def show_settings(self):
        """This method shows the settings page and handles interactions."""
        running = True
        while running:
            # Display background
            self.screen.blit(self.background, (0, 0))

            # Render heading with larger font size (centered at top of the screen)
            self.render_text("Settings", pygame.Rect(0, 50, SCREEN_WIDTH, 100), self.heading_font, color=(255, 165, 0))  # Orange heading

            # Render the "Sound" label (black color)
            self.render_text("Sound", pygame.Rect(350, 250, 100, 50), self.normal_font, color=(0, 0, 0))  # Black color for text

            # Draw the sound button with "ON" or "OFF" state, placed next to the "Sound" label
            pygame.draw.rect(self.screen, (0, 0, 0), self.sound_button_rect, border_radius=10)  # Black background
            sound_text = "ON" if self.sound_on else "OFF"
            self.render_text(sound_text, self.sound_button_rect, self.button_font, color=(255, 255, 255))  # White text

            # Render the "Mute" label for the second button
            self.render_text("Mute", pygame.Rect(350, 320, 100, 50), self.normal_font, color=(0, 0, 0))  # Black color for text

            # Draw the mute button with "ON" or "OFF" state
            pygame.draw.rect(self.screen, (0, 0, 0), self.mute_button_rect, border_radius=10)  # Black background
            mute_text = "OFF" if self.click_sound_muted else "ON"  # Mute depends on whether click sound is muted
            self.render_text(mute_text, self.mute_button_rect, self.button_font, color=(255, 255, 255))  # White text

            # Draw the back button (black background with white text)
            pygame.draw.rect(self.screen, (0, 0, 0), self.back_button_rect)  # Black background
            self.render_text("Back", self.back_button_rect, self.button_font, color=(255, 255, 255))  # White text

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                    if self.sound_button_rect.collidepoint(event.pos):
                        # Toggle background music state (ON/OFF)
                        self.sound_on = not self.sound_on
                        if self.sound_on:
                            pygame.mixer.music.unpause()  # Unpause background music if it's turned on
                        else:
                            pygame.mixer.music.pause()  # Pause background music if it's turned off
                        if not self.click_sound_muted:  # Only play button click sound if it's not muted
                            self.button_click_sound.play()  # Play the button click sound

                    elif self.mute_button_rect.collidepoint(event.pos):
                        # Toggle click sound mute/unmute
                        self.click_sound_muted = not self.click_sound_muted
                        if self.click_sound_muted:
                            pygame.mixer.Sound.set_volume(self.button_click_sound, 0)  # Mute the click sound
                        else:
                            pygame.mixer.Sound.set_volume(self.button_click_sound, 1.0)  # Unmute the click sound
                        if not self.click_sound_muted:  # Only play button click sound if it's not muted
                            self.button_click_sound.play()  # Play the button click sound

                    elif self.back_button_rect.collidepoint(event.pos):
                        # Exit settings and return to the main menu
                        running = False  # Close settings page and go back to main menu

            # Update the display
            pygame.display.flip()

        # Return to the main menu
        return

# Create an instance of GameSetting and show settings page
# settings_page = GameSetting()  # Create an instance of GameSetting
# settings_page.show_settings()  # Display the settings page
