import pygame
from random import randint
from constants import *

class Food:
    def __init__(self):
        self.x = randint(0, NMBRE_CASE_X - 1)
        self.y = randint(0, NMBRE_CASE_Y - 1)
        self.color = (0, 255, 0)

def affichage_food(screen, food):
    pygame.draw.rect(screen, food.color, pygame.Rect(food.x*LONG_CASE_X, food.y*LONG_CASE_Y, LONG_CASE_X, LONG_CASE_Y))