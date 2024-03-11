

class Snake:

    def __init__(self, position_init_body):
        self.list_body = position_init_body
        self.longueur = 1
        self.direction = 0


    def change_direction(self, decision):
        if decision not in [-1, 0, 1]:
            print("Erreur entrée change_direction")
            exit(0)
        self.direction += decision
        if self.direction == -1:
            self.direction = 3
        if self.direction == 4:
            self.direction = 0

    def mouvement_snake(self, food, board):

        for i in range(self.longueur - 1, 0, -1):
            x = self.list_body[i-1][0]
            y = self.list_body[i-1][1]
            self.list_body[i][0] = x
            self.list_body[i][1] = y
        

        x, y = self.list_body[0][0] , self.list_body[0][1]
        d_x, d_y = 0, 0
        if self.direction == 0:
            d_x -= 1
        elif self.direction == 1:
            d_y -= 1
        elif self.direction == 2:
            d_x += 1
        elif self.direction == 3:
            d_y += 1
        
        self.list_body[0][0] = x + d_x
        self.list_body[0][1] = y + d_y

        if self.list_body[0][0] == food.x and self.list_body[0][1] == food.y:
            last_body = self.list_body[-1]
            self.list_body.append([last_body[0], last_body[1]])
            self.longueur += 1
            food.change_position(board)