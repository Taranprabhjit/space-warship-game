# from pygame import Rect, Surface, Vector2
import pygame
from utils import load_photos, get_random_position

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
PLANE_SPEED = 5

class GameObject:
    def __init__(self, position, photos):
        # rectangular sprite
        self.sprite = photos
        self.rect = photos.get_rect(bottomleft = (position[0], position[1]))

    def draw(self, surface):
        surface.blit(self.sprite, self.rect)

    def move(self):
        self.rect.move_ip(0, 2)


#############################################################################


class PlayerPlane(GameObject):
    previous_time = pygame.time.get_ticks()
    current_time = previous_time
    def __init__(self, create_bomb_callback):
        super().__init__(
            (0, SCREEN_HEIGHT), 
            load_photos("plane_center"))
        self.create_bomb_callback = create_bomb_callback
        self.lives = 3
        self.ammo = 5
        

    def move(self, pressed_keys):
        self.sprite = load_photos("plane_center")
       
        if pressed_keys[pygame.K_LEFT]:
            self.sprite = load_photos("plane_left")
            self.rect.move_ip(-PLANE_SPEED, 0)
        elif pressed_keys[pygame.K_RIGHT]:
            self.sprite = load_photos("plane_right")
            self.rect.move_ip(PLANE_SPEED, 0)

        if pressed_keys[pygame.K_SPACE]:
            PlayerPlane.current_time = pygame.time.get_ticks()
            if PlayerPlane.current_time - PlayerPlane.previous_time > 250 and self.ammo > 0:
                PlayerPlane.previous_time = PlayerPlane.current_time
                self.shoot()
                self.ammo -= 1
            
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    

    def shoot(self):
        new_bomb = Bomb(self)
        self.create_bomb_callback(new_bomb)
        # self.bomb_sound.play()


#############################################################################


class EnemyPlane(GameObject):
    def __init__(self):
        super().__init__(get_random_position(), load_photos("enemy_plane"))
        self.speed = 2
    

    def move(self):
        self.rect.move_ip(0, self.speed)


#############################################################################


class Bomb(GameObject):
    LEFTRIGHT = 1
    def __init__(self, plane):
        xy = [(35,76), (98,74)][self.LEFTRIGHT]
        Bomb.LEFTRIGHT = (Bomb.LEFTRIGHT + 1) % 2

        super().__init__(
            (plane.rect.topleft[0] + xy[0], plane.rect.topleft[1] + xy[1]), 
            load_photos("bomb")
        )
        self.speed = 5


    def move(self):
        self.rect.move_ip(0, -self.speed)


#############################################################################


class AmmoDrop(GameObject):
    def __init__(self):
        super().__init__(get_random_position(), load_photos("ammo_drop"))
        
#################################################################################

