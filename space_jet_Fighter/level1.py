import pygame
import sys
import time
from utils import load_photos, bomb_collides_with_enemy, remove_off_the_screen_height, get_text_surface
from models import PlayerPlane, EnemyPlane, Bomb

# Initialize constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
PLANE_SPEED = 5
AMMO_SPEED = 10
ENEMY_SPEED = 1

class Level1:
    def __init__(self, game=None):
        pygame.init()
        pygame.mixer.init()
        
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Level 1")
        
        # Load background and images
        self.background = load_photos("level_4", False)
        self.heart_image = load_photos("lives")
        self.ammo_image = load_photos("bomb")
        
        # Initialize fonts
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        
        # Player setup
        self.player = PlayerPlane(self.create_bomb)
        self.player.lives = 2
        self.player.ammo = 5
        self.player.bombs = []  # Initialize bombs list for the player
        
        # Enemy setup
        self.enemies = []
        self.enemy_spawn_delay = 3000  # Spawn new enemy every 3 seconds
        pygame.time.set_timer(pygame.USEREVENT + 1, self.enemy_spawn_delay)
        
        # Game state
        self.score = 0
        self.enemies_remaining = 3  # Increased to allow for more continuous gameplay
        self.state = "waiting"
        
        # Sounds
        try:
            self.button_click_sound = pygame.mixer.Sound("assets/sounds/button_click.mp3")
            self.ammo_fire_sound = pygame.mixer.Sound("assets/sounds/ammo_fire.mp3")
            self.background_music = "assets/sounds/background_music.mp3"
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.play(loops=-1, start=0.0)
        except:
            print("Warning: Sound files not found. Continuing without sound.")

    def create_bomb(self, bomb):
        """Create a new bomb and add it to the player's bomb list."""
        self.player.bombs.append(bomb)
        if hasattr(self, 'ammo_fire_sound'):
            self.ammo_fire_sound.play()

    def render_text(self, text, x, y, color=(0, 0, 0)):
        """Render text centered at the given position."""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT + 1 and self.state == "playing":  # Spawn an enemy
                if self.enemies_remaining > 0:
                    new_enemy = EnemyPlane()
                    new_enemy.speed = ENEMY_SPEED  # Set enemy speed
                    new_enemy.rect.top = 0
                    self.enemies.append(new_enemy)
                    self.enemies_remaining -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if self.state == "waiting":
                        self.state = "playing"
                    elif self.state == "playing" and self.pause_button.collidepoint(mouse_pos):
                        self.state = "paused"
                    elif self.state == "paused":
                        if self.resume_button.collidepoint(mouse_pos):
                            self.resume_with_countdown()
                        elif self.restart_button.collidepoint(mouse_pos):
                            self.__init__(self.game)
                            self.run()
                            return

    def handle_input(self):
        self.handle_events()

    def update(self):
        """Update game state including player, enemies, and bombs movements."""
        if self.state != "playing":
            return

        # Update player movement
        pressed_keys = pygame.key.get_pressed()
        self.player.move(pressed_keys)

        # Update enemies' movement
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.rect.top > SCREEN_HEIGHT:
                self.player.lives -= 1
                self.enemies.remove(enemy)

        # Update bomb movement and handle collisions
        for bomb in self.player.bombs[:]:
            bomb.move()
            # Remove bomb if it goes off screen
            if bomb.rect.bottom < 0:
                self.player.bombs.remove(bomb)
            else:
                # Check for collisions with enemies
                for enemy in self.enemies[:]:
                    if bomb.rect.colliderect(enemy.rect):
                        self.score += 50
                        
                        if hasattr(self, 'ammo_fire_sound'):
                            self.ammo_fire_sound.play()

                        self.player.bombs.remove(bomb)
                        self.enemies.remove(enemy)
                        break

        # Win/lose condition checks
        if len(self.enemies) == 0 and self.enemies_remaining == 0:
            self.state = "won"
        elif self.player.lives <= 0:
            self.state = "lost"

    def draw(self, screen):
        """Draw the player, enemies, bombs, and UI elements."""
        # Draw background scaled to the screen size
        scaled_background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_background, (0, 0))
        
        if self.state == "waiting":
            self.render_text("Level 1", SCREEN_WIDTH // 2 - self.font.size("Level 1")[0] // 2, 20, (255, 255, 255))
            self.render_text("Please click to start the game", SCREEN_WIDTH // 2 - self.font.size("Please click to start the game")[0] // 2, SCREEN_HEIGHT // 2, (0, 0, 0))
        elif self.state in ["playing", "won", "lost", "paused"]:
            # Draw player
            self.player.draw(screen)
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(screen)
            
            # Draw bombs
            for bomb in self.player.bombs:
                bomb.draw(screen)

            # Draw UI elements (hearts for lives, ammo for remaining ammo)
            for i in range(self.player.lives):
                screen.blit(self.heart_image, (10 + i * 40, 10))
            for i in range(self.player.ammo):
                screen.blit(self.ammo_image, (10 + i * 20, 60))

            # Draw pause button
            self.pause_button = pygame.draw.rect(screen, (25, 25, 112), (SCREEN_WIDTH - 150, 10, 120, 40))
            self.render_text("Pause", SCREEN_WIDTH - 140 + 60 - self.font.size("Pause")[0] // 2, 15, (0, 0, 0))

        if self.state == "paused":
            self.show_pause_menu()
        elif self.state == "won" or self.state == "lost":
            self.show_game_over()

        pygame.display.flip()

    def run(self):
        """Main game loop for Level 1."""
        while True:
            self.handle_input()
            self.update()
            self.draw(self.screen)
            self.clock.tick(60)

            if self.state == "won" or self.state == "lost":
                break

        self.show_game_over()

    def show_pause_menu(self):
        """Display a pause menu with options to resume or restart."""
        self.resume_button = pygame.draw.rect(self.screen, (255, 223, 0), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50))
        self.restart_button = pygame.draw.rect(self.screen, (255, 223, 0), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50))
        self.render_text("Resume", SCREEN_WIDTH // 2 - self.font.size("Resume")[0] // 2, SCREEN_HEIGHT // 2 + 10, (0, 0, 0))
        self.render_text("Restart", SCREEN_WIDTH // 2 - self.font.size("Restart")[0] // 2, SCREEN_HEIGHT // 2 + 80, (0, 0, 0))
        pygame.display.flip()

    def resume_with_countdown(self):
        """Display a countdown before resuming the game."""
        for i in range(3, 0, -1):
            self.draw(self.screen)
            self.render_text(f"Resuming in {i}...", SCREEN_WIDTH // 2 - self.font.size(f"Resuming in {i}...")[0] // 2, SCREEN_HEIGHT // 2 - 50, (255, 255, 255))
            pygame.display.flip()
            time.sleep(1)
        self.state = "playing"

    def show_game_over(self):
        """Handles the game-over screen."""
        game_over = True

        # Clear event queue to avoid residual key presses
        pygame.event.clear()

        while game_over:
            # Draw background scaled to the screen size
            scaled_background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_background, (0, 0))

            # Update the message based on win/lose state
            if self.state == "won":
                message = "Game Over! You Win"
            else:
                message = "Game Over! You Lose. Try Again"

            self.render_text(message, SCREEN_WIDTH // 2 - self.font.size(message)[0] // 2, SCREEN_HEIGHT // 2 - 150, (255, 255, 255))

            # Define buttons
            try_again_button = pygame.draw.rect(self.screen, (255, 223, 0), (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 50, 150, 50))
            level_select_button = pygame.draw.rect(self.screen, (255, 223, 0), (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50))
            next_level_button = pygame.draw.rect(self.screen, (255, 223, 0), (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 50, 150, 50))

            # Render button texts
            self.render_text("Try Again", SCREEN_WIDTH // 2 - 300 + 75 - self.font.size("Try Again")[0] // 2, SCREEN_HEIGHT // 2 + 65, (0, 0, 0))
            self.render_text("Level Select", SCREEN_WIDTH // 2 - 75 + 75 - self.font.size("Level Select")[0] // 2, SCREEN_HEIGHT // 2 + 65, (0, 0, 0))
            self.render_text("Next Level", SCREEN_WIDTH // 2 + 150 + 75 - self.font.size("Next Level")[0] // 2, SCREEN_HEIGHT // 2 + 65, (0, 0, 0))
            pygame.display.flip()

            # Handle game over events with button interactions
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if try_again_button.collidepoint(mouse_pos):
                            self.__init__(self.game)
                            self.run()
                            return
                        elif level_select_button.collidepoint(mouse_pos):
                            from level import LevelPage
                            level_page = LevelPage(self.game)
                            level_page.show_level_page()
                            return
                        elif next_level_button.collidepoint(mouse_pos):
                            from level2 import Level2
                            level2 = Level2(self.game)
                            level2.run()
                            return
