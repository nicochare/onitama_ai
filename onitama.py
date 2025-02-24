import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
MAX_TURNOS = 200 # Turnos totales, 100 por jugador
player_id = int(input())


class nodo:
    def __init__(self, estado):
        self.estado = estado
    def imprimir(self):
        for fila in self.estado:
            print(fila)

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

# Tarjeta medio    
tarjeta1 = tarjeta(-1, 1, 0,1, -1,-1, 1,-1, 0,0)

# Tarjetas jugador abajo
tarjeta4 = tarjeta(0, 4, -1,0, 0,1, 1,0, 0,0)
tarjeta15 = tarjeta(0, 15, 0,-1, 0,2, 0,0, 0,0)

# Tarjetas jugador arriba
tarjeta9 = tarjeta(1, 9, 1,1, -1,-1, -2,0, 0,0)
tarjeta11 = tarjeta(1, 11, -1,1, 1,1, 1,-1, -1,-1)

listamovimientos = [tarjeta1, tarjeta4, tarjeta9, tarjeta11, tarjeta15]
        
def aplica(funcion, nodo):
    funcion(nodo)

def esPosible(movimiento, nodo):
    if movimiento.

def esFinal(nodo):
    # estadoFinal = 
    return nodo.estado == 1#estadoFinal


def alpha_beta(nodo, profundidad, alfa, beta, jugadorMAX):
    if profundidad == 0 or esFinal(nodo):
        return eval(nodo)
    
    if jugadorMAX:
        value = -math.inf
        for mov in listamovimientos:
            if esPosible(nodo, mov):
                nuevoNodo = aplica(mov, nodo)
                valNuevoNodo, sigMov = alpha_beta(nuevoNodo, profundidad, alfa, beta, False)
                if valNuevoNodo > value:
                    value = valNuevoNodo
                    mejorMov = mov
                    alfa = value
                if alfa >= beta:
                    break
        return value, mejorMov
    else:
        value = math.inf
        for mov in listamovimientos:
            if esPosible(nodo, mov):
                nuevoNodo = aplica(movimiento, nodo)
                valNuevoNodo, sigMov = alpha_beta(nuevoNodo, profundidad-1, alfa, beta, False)
                if valNuevoNodo < value:
                    value = valNuevoNodo
                    mejorMov = mov
                    beta = value
                if alfa >= beta:
                    break
        return value, mejorMov

# game loop
cantJugadas = 0
while cantJugadas <= 200:
    cantJugadas += 1

    for i in range(5):
        board = input()
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
    action_count = int(input())
    for i in range(action_count):
        inputs = input().split()
        card_id = int(inputs[0])
        move = inputs[1]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    print("1 A1B2 moving the student")
