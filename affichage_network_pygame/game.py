from snake import *
from food import *
from network import *
import torch
import torch.nn as nn
import pygame

SIZE_SCREEN = (600, 600)

class Game:

    def __init__(self, taille_board):
        self.board = []
        self.taille_board = taille_board
        self.long_case = SIZE_SCREEN[0]//taille_board
        self.snake = Snake([[taille_board//2, taille_board//2]])
        self.init_board()
        self.food = Food(taille_board, self.board)
        self.network = Network(33, 3)
        self.network.load_state_dict(torch.load('network_trained\model_trained.pth'))
        self.network.eval()
        self.screen = pygame.display.set_mode(SIZE_SCREEN)
        pygame.display.set_caption('Snake')

    def init_board(self):
        # Remplissage de case vide
        for _ in range(self.taille_board):
            new_board = [0 for _ in range(self.taille_board)]
            self.board.append(new_board)
        
        # Ajout du snake
        for position_snake in self.snake.list_body:
            self.board[position_snake[0]][position_snake[1]] = -1
    
    def actualisation_board(self):
        for i in range(self.taille_board):
            for j in range(self.taille_board):
                self.board[i][j] = 0

        # Ajout de la pomme
        self.board[self.food.x][self.food.y] = 1

        # Ajout du snake
        for position_snake in self.snake.list_body:
            self.board[position_snake[0]][position_snake[1]] = -1

    def affichage_board(self):

        self.actualisation_board()

        for i in range(self.taille_board):
            for j in range(self.taille_board):
                if j == 0:
                    print("|", end=" ")
                if self.board[i][j] != -1:
                    print(self.board[i][j], end=" ")
                else:
                    print("*", end=" ")
            print("|")
        for _ in range(self.taille_board+2):
            print("_", end=" ")
        
        print()

    def decision_network(self):
        vision_centre = torch.tensor(self.get_vision_centre(2), dtype=torch.float32)
        info_vision = self.get_info_network()
        info_vision = [int(boolean) for boolean in info_vision]
        info_vision = torch.tensor(info_vision, dtype=torch.float32)

        tenseur_entree = torch.cat((vision_centre.view(-1), info_vision), dim=0)
        sortie = self.network(tenseur_entree)
        return sortie.argmax().item()

    def get_vision_centre(self, rayon_vision=2):
        long_vision = rayon_vision*2 + 1
        vision = []
        x, y = self.snake.list_body[0][0], self.snake.list_body[0][1]
        for i in range(long_vision):
            vision_append = []
            for j in range(long_vision):
                value_to_append = -1
                if x+i-rayon_vision < 0 or y+j-rayon_vision < 0 or x+i-rayon_vision > self.taille_board-1 or y+j-rayon_vision > self.taille_board-1:
                    value_to_append = -1
                else:
                    value_to_append = self.board[x + i-rayon_vision][y + j-rayon_vision]
                vision_append.append(value_to_append)
            vision.append(vision_append)
        return vision

    def get_info_network(self):
        # Calcul des variables booléennes
        variables_bool = [
            self.snake.direction == 0,  # face_top
            self.snake.direction == 2,  # face_down
            self.snake.direction == 3,  # face_right
            self.snake.direction == 1,  # face_left
            self.food.x - self.snake.list_body[0][0] < 0,  # apple_top
            self.food.x - self.snake.list_body[0][0] > 0,  # apple_down
            self.food.y - self.snake.list_body[0][1] > 0,  # apple_right
            self.food.y - self.snake.list_body[0][1] < 0   # apple_left
        ]

        # Affichage des résultats
        # for i, variable in enumerate(variables_bool):
        #     print(f"{['face_top', 'face_down', 'face_right', 'face_left', 'apple_top', 'apple_down', 'apple_right', 'apple_left'][i]} : {variable}")
        return variables_bool


    def end_game(self):
        snake_without_head = []

        if self.snake.longueur != 1:
            snake_without_head = self.snake.list_body[2:]
        head = self.snake.list_body[0]
        if head in snake_without_head:
            return 1
        
        if head[0] == -1 or head[0] >= self.taille_board or head[1] == -1 or head[1] >= self.taille_board:
            return 1
        
        return 0

    def affichage_quadrillage(self):
        for i in range(self.taille_board):
            pygame.draw.line(self.screen, (255, 255, 255), (0, i*self.long_case), (SIZE_SCREEN[0], i*self.long_case), 1)
        for i in range(self.taille_board):
            pygame.draw.line(self.screen, (255, 255, 255), (i*self.long_case, 0), (i*self.long_case, SIZE_SCREEN[1]), 1)

    def affichage_food(self):
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food.x*self.long_case, self.food.y*self.long_case, self.long_case, self.long_case))

    def affichage_snake(self):
        for body in self.snake.list_body:
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(body[0]*self.long_case, body[1]*self.long_case, self.long_case, self.long_case))

    def main_loop(self):

        print("Début Boucle Principal")

        turn_limit = 10000

        running = True
        turn = 0
        while running:

            self.actualisation_board()
            
            decision = self.decision_network() - 1
            self.snake.change_direction(decision)

            self.snake.mouvement_snake(self.food, self.board)


            self.screen.fill((0, 0, 0))

            self.affichage_quadrillage()
            self.affichage_food()
            self.affichage_snake()


            if self.end_game() == 1:
                running = False
            
            turn += 1
            if turn == turn_limit:
                running = False
            
            pygame.display.flip()
        
        # Enregistrement du modèle
        torch.save(self.network.state_dict(), 'network_trained/model_trained.pth')
        

            
