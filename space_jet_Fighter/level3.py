import pygame
import sys
import time
from utils import load_photos, bomb_collides_with_enemy, remove_off_the_screen_height, get_text_surface
from models import PlayerPlane, EnemyPlane, Bomb, AmmoDrop

# Initialize constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
PLANE_SPEED = 6.0  # Increased speed for Level 3
AMMO_SPEED = 10
ENEMY_SPEED = 1.5  # Increased speed for Level 3

class Level3:
    def __init__(self, game=None):
        pygame.init()
        pygame.mixer.init()
        
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Level 3")
        
        # Load background and images
        self.background = load_photos("level_3", False)
        self.heart_image = load_photos("lives")
        self.ammo_image = load_photos("bomb")
        
        # Initialize fonts
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        
        # Player setup
        self.player = PlayerPlane(self.create_bomb)
        self.player.lives = 3
        self.player.ammo = 7  # Default ammo for Level 3
        self.player.bombs = []  # Initialize bombs list for the player
        
        # Enemy setup
        self.enemies = []
        self.enemy_spawn_delay = 2000  # Spawn new enemy every 2 seconds
        pygame.time.set_timer(pygame.USEREVENT + 1, self.enemy_spawn_delay)
        
        # Ammo drop setup
        self.ammo_drops = []
        self.ammo_drop_spawn_delay = 8000  # Spawn new ammo drop every 8 seconds
        pygame.time.set_timer(pygame.USEREVENT + 2, self.ammo_drop_spawn_delay)
        
        # Game state
        self.score = 0
        self.enemies_remaining = 15  # Increased number of enemies for Level 3
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

    def draw_gradient(self, rect, color1, color2):
        """Draw a gradient-filled rectangle."""
        for y in range(rect.height):
            blend_ratio = y / rect.height
            blended_color = (
                int(color1[0] * (1 - blend_ratio) + color2[0] * blend_ratio),
                int(color1[1] * (1 - blend_ratio) + color2[1] * blend_ratio),
                int(color1[2] * (1 - blend_ratio) + color2[2] * blend_ratio)
            )
            pygame.draw.line(self.screen, blended_color, (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))

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
            elif event.type == pygame.USEREVENT + 2 and self.state == "playing":  # Spawn an ammo drop
                new_ammo_drop = AmmoDrop()
                new_ammo_drop.rect.top = 0
                self.ammo_drops.append(new_ammo_drop)
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
        """Update game state including player, enemies, bombs, and ammo drops movements."""
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
                        self.player.bombs.remove(bomb)
                        self.enemies.remove(enemy)
                        break

        # Update ammo drop movement and handle collection
        for ammo_drop in self.ammo_drops[:]:
            ammo_drop.move()
            if ammo_drop.rect.bottom > SCREEN_HEIGHT:
                self.ammo_drops.remove(ammo_drop)
            elif ammo_drop.rect.colliderect(self.player.rect):
                self.player.ammo += 3
                self.ammo_drops.remove(ammo_drop)

        # Win/lose condition checks
        if len(self.enemies) == 0 and self.enemies_remaining == 0:
            self.state = "won"
        elif self.player.lives <= 0:
            self.state = "lost"

    def draw(self, screen):
        """Draw the player, enemies, bombs, ammo drops, and UI elements."""
        # Draw background scaled to the screen size
        scaled_background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_background, (0, 0))
        
        if self.state == "waiting":
            self.render_text("Level 3", SCREEN_WIDTH // 2 - self.font.size("Level 3")[0] // 2, 20, (255, 255, 255))
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

            # Draw ammo drops
            for ammo_drop in self.ammo_drops:
                ammo_drop.draw(screen)

            # Draw UI elements (hearts for lives, ammo for remaining ammo)
            for i in range(self.player.lives):
                screen.blit(self.heart_image, (10 + i * 40, 10))
            for i in range(self.player.ammo):
                screen.blit(self.ammo_image, (10 + i * 20, 60))

            # Draw pause button with gradient
            self.pause_button = pygame.Rect(SCREEN_WIDTH - 150, 10, 120, 40)
            self.draw_gradient(self.pause_button, (25, 25, 112), (0, 0, 255))
            self.render_text("Pause", SCREEN_WIDTH - 140 + 60 - self.font.size("Pause")[0] // 2, 15, (0, 0, 0))

        if self.state == "paused":
            self.show_pause_menu()
        elif self.state == "won" or self.state == "lost":
            self.show_game_over()

        pygame.display.flip()

    def run(self):
        """Main game loop for Level 3."""
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
        self.resume_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        self.restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
        
        # Draw resume button with gradient
        self.draw_gradient(self.resume_button, (255, 223, 0), (255, 165, 0))
        self.render_text("Resume", SCREEN_WIDTH // 2 - self.font.size("Resume")[0] // 2, SCREEN_HEIGHT // 2 + 10, (0, 0, 0))
        
        # Draw restart button with gradient
        self.draw_gradient(self.restart_button, (255, 223, 0), (255, 165, 0))
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
            message = "Game Over! Press Enter to continue."
            self.render_text(message, SCREEN_WIDTH // 2 - self.font.size(message)[0] // 2, SCREEN_HEIGHT // 2 - 150, (255, 255, 255))

            # Display final score
            final_score_message = f"Your Score: {self.score}"
            self.render_text(final_score_message, SCREEN_WIDTH // 2 - self.font.size(final_score_message)[0] // 2, SCREEN_HEIGHT // 2 - 100, (255, 255, 255))

            # Define buttons
            try_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 50, 150, 50)
            level_select_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50)
            next_level_button = pygame.Rect(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 50, 150, 50)

            # Draw try again button with gradient
            self.draw_gradient(try_again_button, (255, 223, 0), (255, 165, 0))
            self.render_text("Try Again", SCREEN_WIDTH // 2 - 300 + 75 - self.font.size("Try Again")[0] // 2, SCREEN_HEIGHT // 2 + 65, (0, 0, 0))
            
            # Draw level select button with gradient
            self.draw_gradient(level_select_button, (255, 223, 0), (255, 165, 0))
            self.render_text("Level Select", SCREEN_WIDTH // 2 - 75 + 75 - self.font.size("Level Select")[0] // 2, SCREEN_HEIGHT // 2 + 65, (0, 0, 0))
            
            # Draw next level button with gradient
            self.draw_gradient(next_level_button, (255, 223, 0), (255, 165, 0))
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
                            from level4 import Level4
                            level4 = Level4(self.game)
                            level4.run()
                            return
