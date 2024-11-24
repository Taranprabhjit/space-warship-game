import pygame
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
PLANE_SPEED = 5

def load_photos(name, with_alpha=True):
    path = f"./assets/photos/{name}.png"
    loaded_photos = pygame.image.load(path)

    if with_alpha:
        return loaded_photos.convert_alpha()
    else:
        return loaded_photos
#############################################################################


def load_sound(name):
    path = f"./assets/sounds/{name}.mp3"
    loaded_sound = pygame.mixer.Sound(path)
    return loaded_sound


#############################################################################


def get_random_position():
    return (random.randint(0, SCREEN_WIDTH - 150), 0)


#############################################################################


def bomb_collides_with_enemy(bomb, enemy):
    x1 = enemy.rect.topleft[0]
    y1 = enemy.rect.topleft[1]

    x2 = enemy.rect.topright[0]
    y2 = enemy.rect.topright[1]

    x3 = enemy.rect.centerx
    y3 = enemy.rect.bottom

    px = bomb.rect.centerx
    py = bomb.rect.centery

    areaEnemy = abs( (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1) )

    area1 = abs( (x1-px)*(y2-py) - (x2-px)*(y1-py) )
    area2 = abs( (x2-px)*(y3-py) - (x3-px)*(y2-py) )
    area3 = abs( (x3-px)*(y1-py) - (x1-px)*(y3-py) )

    areaCurrent = area1 + area2 + area3
    return areaCurrent == areaEnemy


#############################################################################


def remove_off_the_screen_height(lst, enemy=False, lives=None):
    for element in lst[:]:
        if element.rect.top > SCREEN_HEIGHT:
                lst.remove(element)
                if enemy == True:
                    lives -= 1


#############################################################################


def get_text_surface(text, size):
    font = pygame.font.SysFont(None, size)
    surface_with_text = font.render(text, True, (255, 255, 255))
    return surface_with_text

    
