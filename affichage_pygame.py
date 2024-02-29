import pygame
from snake import *
from food import *
from constants import *

def init_pygame():

    pygame.init()
    screen = pygame.display.set_mode(SIZE_SCREEN)

    return screen


def main_loop_pygame(screen):

    snake = Snake()
    food = Food()

    # Créer un objet Clock pour contrôler le FPS
    clock = pygame.time.Clock()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN: 
                # Récupérer les touches enfoncées
                keys = pygame.key.get_pressed()
                snake.actualisation_direction(keys)
        
        snake.movement(food)

        screen.fill((0, 0, 0))
        affichage_quadrillage(screen)
        
        affichage_food(screen, food)
        affichage_snake(screen, snake)

        pygame.display.flip()

        clock.tick(FPS)

def affichage_quadrillage(screen):
    for i in range(NMBRE_CASE_Y):
        pygame.draw.line(screen, (255, 255, 255), (0, i*LONG_CASE_Y), (SIZE_SCREEN[0], i*LONG_CASE_Y), 1)
    for i in range(NMBRE_CASE_X):
        pygame.draw.line(screen, (255, 255, 255), (i*LONG_CASE_X, 0), (i*LONG_CASE_X, SIZE_SCREEN[1]), 1)