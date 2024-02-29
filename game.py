from snake import *
from food import *
from constants import *

class Game:

    def __init__(self, w=SIZE_SCREEN[0], h=SIZE_SCREEN[1]):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption('Snake')
        self.snake = Snake()
        self.food = Food()
    
    
