from all_colors import *
from pygame.constants import *
import pygame
pygame.init()

import pygame.mixer
pygame.mixer.init()

import pygame.font
pygame.font.init()

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Моя игра')
background_color = (255, 255, 255)
screen.fill(background_color)

GAME_OVER_COLOR = BLACK
WIN_COLOR = GREEN

pygame.mixer.music.load('resours/sonar.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

shot_sound = pygame.mixer.Sound('resours/shot.mp3')
explosion_sound = pygame.mixer.Sound('resours/explosion.mp3')

volume = 0.5
shot_sound.set_volume(volume)
explosion_sound.set_volume(volume)

screen_rect = screen.get_rect()

ship = pygame.Rect(300, 200, 50, 100)
ship.right = screen_rect.right
ship.centery = screen_rect.centery

missile = pygame.Rect(50, 50, 10, 10)
missile.left = screen_rect.left
missile.centery = screen_rect.centery


missile_speed_x = 0
missile_speed_y = 0

ship_speed_y = 1

ship_alive = True
missile_alive = True

missile_launched = False

hp_ship = 10
hp_missile = 10

FPS = 60
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not missile_launched:
                missile_launched = True
                missile_speed_x = 3
                missile_speed_y = 0
                pygame.mixer.music.stop()
                shot_sound.play()

            elif event.key == pygame.K_w and not missile_launched:
                missile_speed_y = -2
            elif event.key == pygame.K_s and not missile_launched:
                missile_speed_y = 2


            elif event.key == pygame.K_UP:
                volume += 0.1
                volume = min(volume, 1)
                shot_sound.set_volume(volume)
                explosion_sound.set_volume(volume)

            elif event.key == pygame.K_DOWN:
                volume -= 0.1
                volume = max(volume, 1)
                shot_sound.set_volume(volume)
                explosion_sound.set_volume(volume)


    screen.fill(background_color)
    if ship_alive:
        pygame.draw.rect(screen, BLUE, ship)
        ship.move_ip(0, ship_speed_y)
        if ship.bottom > screen_rect.bottom or ship.top < screen_rect.top:
            ship_speed_y = - ship_speed_y

    if missile_alive:
        pygame.draw.rect(screen, RED, missile)
        missile.move_ip(missile_speed_x, missile_speed_y)
        if not missile.colliderect(screen_rect):
            missile.x = 0
            missile_speed_x = 0
            missile_launched = False
            hp_missile -= 1
            pygame.mixer.music.play(-1)

        if ship_alive and missile.colliderect(ship):
            missile.x = 0
            missile_speed_x = 0
            missile_launched = False
            hp_missile -= 1
            hp_ship -= 1
            explosion_sound.play()
            pygame.mixer.music.play(-1)

        if hp_missile == 0 and hp_ship != 0:
            missile_alive = False
            ship_alive = False
            background_color = GAME_OVER_COLOR

        if hp_ship == 0:
            ship_alive = False
            missile_alive = False
            background_color = WIN_COLOR

    hp_ship_text = font.render(f"hp_ship: {hp_ship}", True, BLACK)
    hp_missile_text = font.render(f"hp_missile: {hp_missile}", True, BLACK)
    screen.blit(hp_missile_text, (10, 10))
    screen.blit(hp_ship_text, (size[0] - 135, 10))



    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()