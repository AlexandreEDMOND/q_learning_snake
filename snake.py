import pygame
from constants import *

class Body:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
    
    def mouvement_body(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


class Snake:

    def __init__(self):
        self.list_body = [Body(10, 10)]
        self.longueur = 1
        self.direction = 0
    
    def movement(self, food):
        for i in range(self.longueur - 1, 0, -1):
            x = self.list_body[i-1].x
            y = self.list_body[i-1].y
            self.list_body[i].mouvement_body(x, y)
        
        x, y = self.list_body[0].x , self.list_body[0].y
        d_x, d_y = 0, 0
        if self.direction == 0:
            d_x -= 1
        elif self.direction == 1:
            d_y -= 1
        elif self.direction == 2:
            d_x += 1
        elif self.direction == 3:
            d_y += 1
        
        self.list_body[0].mouvement_body(x + d_x, y + d_y)

        if self.list_body[0].x == food.x and self.list_body[0].y == food.y:
            last_body = self.list_body[-1]
            self.list_body.append(Body(last_body.x, last_body.y))
            self.longueur += 1
    
    def actualisation_direction(self, keys):
        if keys[pygame.K_LEFT]:
            self.direction = 0
        if keys[pygame.K_UP]:
            self.direction = 1
        if keys[pygame.K_RIGHT]:
            self.direction = 2
        if keys[pygame.K_DOWN]:
            self.direction = 3 



def affichage_snake(screen, snake):
    for body in snake.list_body:
        pygame.draw.rect(screen, body.color, pygame.Rect(body.x*LONG_CASE_X, body.y*LONG_CASE_Y, LONG_CASE_X, LONG_CASE_Y))