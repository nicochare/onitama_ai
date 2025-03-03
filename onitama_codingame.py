import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

player_id = int(input()) # Jugador 0

class tarjeta:
    def __init__(self, owner, cardId, dx_1,dy_1, dx_2,dy_2, dx_3,dy_3, dx_4,dy_4):
        self.owner = owner
        self.cardId = cardId
        self.dx_1 = dx_1
        self.dy_1 = dy_1
        self.dx_2 = dx_2
        self.dy_2 = dy_2
        self.dx_3 = dx_3
        self.dy_3 = dy_3
        self.dx_4 = dx_4
        self.dy_4 = dy_4
    def devolverDatos(self):
        return self.owner, self.cardId, self.dx_1,self.dy_1, self.dx_2,self.dy_2, self.dx_3,self.dy_3, self.dx_4,self.dy_4
    def devMov1(self):
        return dx_1, dy_1
    def devMov2(self):
        return dx_2, dy_2
    def devMov3(self):
        return dx_3, dy_3
    def devMov4(self):
        return dx_4, dy_4

def transformarTablero(tablero):
    for i in range(5):
        board[i] = list(board[i])

def encontrarMaster(tablero):
    for i in range(5):
        for j in range(5):
            if tablero[i][j] == "B":
                return i, j
    return -1, -1

def distancia_manhattan(i, j):
    i2, j2 = 0, 2
    return abs(i-i2) + abs(j-j2)    

def evaluarTablero(board, numAcciones, distancia_master):
    vivasMias = 0
    vivasRival = 0
    for i in range(5):
        vivasMias += ''.join(board[i]).count("b")
        vivasRival += ''.join(board[i]).count("w")
    return (vivasMias-vivasRival)*0.55 + distancia_master*0.35 + numAcciones*0.1

# game loop
while True:
    # Tablero
    board = []
    for i in range(5):
        row = input()
        board.append(row)
    
    transformarTablero(board)

    # print(board, file=sys.stderr, flush=True)


    # 5 Tarjetas
    tarjetas = []
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        card = tarjeta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        tarjetas.append(card)

    # Acciones posibles
    acciones = []
    action_count = int(input())
    for i in range(action_count):
        inputs = input().split()
        card_id = int(inputs[0])
        move = inputs[1]
        acciones.append([card_id, move])

    x_master, y_master = encontrarMaster(board)
    distancia_master = distancia_manhattan(x_master, y_master)
    puntuacion = evaluarTablero(board, len(acciones), distancia_master)

    if len(acciones) > 0:
        print(puntuacion, file=sys.stderr, flush=True)
        print(acciones[0][0], acciones[0][1])
    else:
        print("PASS")