from random import randint

class Food:
    def __init__(self, taille_board, board):
        self.x = 0
        self.y = 0
        self.taille_board = taille_board
        self.change_position(board)
    
    def change_position(self, board):
        not_good = True
        while not_good:
            self.x = randint(0, self.taille_board - 1)
            self.y = randint(0, self.taille_board - 1)
            if board[self.x][self.y] != -1:
                not_good = False