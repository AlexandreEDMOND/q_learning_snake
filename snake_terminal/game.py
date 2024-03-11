from snake import *
from food import *
from network import *
import torch
import torch.nn as nn

class Game:

    def __init__(self, taille_board):
        self.board = []
        self.taille_board = taille_board
        self.snake = Snake([[taille_board//2, taille_board//2]])
        self.init_board()
        self.food = Food(taille_board, self.board)
        self.network = Network(taille_board**2, 3)

    def init_board(self):
        # Remplissage de case vide
        for _ in range(self.taille_board):
            new_board = [0 for _ in range(self.taille_board)]
            self.board.append(new_board)
        
        # Ajout du snake
        for position_snake in self.snake.list_body:
            self.board[position_snake[0]][position_snake[1]] = -1
    

    def affichage_board(self):

        for i in range(self.taille_board):
            for j in range(self.taille_board):
                self.board[i][j] = 0

        # Ajout de la pomme
        self.board[self.food.x][self.food.y] = 1

        # Ajout du snake
        for position_snake in self.snake.list_body:
            self.board[position_snake[0]][position_snake[1]] = -1

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
        tenseur_entree = torch.FloatTensor(self.board).view(1, -1)
        sortie = self.network(tenseur_entree)
        return sortie.argmax().item()


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

    def main_loop(self):

        allowed_keys = ["q", "z", "d", "e"]

        running = True
        while running:

            self.affichage_board()

            # decision = " "
            # while decision not in allowed_keys:
            #    decision = input()
            #    if decision == "e":
            #        running = False
            #        break

            # if decision in allowed_keys:
            #     value = 0
            #     if decision == "q":
            #         value = 1
            #     if decision == "d":
            #         value = -1
            #     self.snake.change_direction(value)
            
            decision = self.decision_network() - 1
            self.snake.change_direction(decision)

            self.snake.mouvement_snake(self.food, self.board)
            if self.end_game() == 1:
                running = False
            

            
