from snake import *
from food import *
from constants import *
from affichage_pygame import *
from q_network import *
import numpy as np

class Game:

    def __init__(self):
        self.w = SIZE_SCREEN[0]
        self.h = SIZE_SCREEN[1]
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.snake = Snake()
        self.food = Food()
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.Q_network = QNetwork(5, 3)
    
    def main_loop(self):
        pygame.init()

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN: 
                    # Récupérer les touches enfoncées
                    keys = pygame.key.get_pressed()
                    self.snake.actualisation_direction(keys)

            # Générer des données d'entrée aléatoires
            input_data = np.random.rand(5)
            input_tensor = torch.FloatTensor(input_data)
            output_tensor = self.Q_network(input_tensor)
            output_data = output_tensor.detach().numpy()
            print(output_data)

            self.snake.movement(self.food)

            self.screen.fill((0, 0, 0))

            self.affichage_quadrillage()
        
            affichage_food(self.screen, self.food)
            affichage_snake(self.screen, self.snake)
            pygame.display.flip()

            self.clock.tick(self.fps)
    
    def affichage_quadrillage(self):
        for i in range(NMBRE_CASE_Y):
            pygame.draw.line(self.screen, COLOR_QUADRILLAGE, (0, i*LONG_CASE_Y), (SIZE_SCREEN[0], i*LONG_CASE_Y), 1)
        for i in range(NMBRE_CASE_X):
            pygame.draw.line(self.screen, COLOR_QUADRILLAGE, (i*LONG_CASE_X, 0), (i*LONG_CASE_X, SIZE_SCREEN[1]), 1)


