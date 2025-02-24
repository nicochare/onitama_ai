import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
MAX_TURNOS = 200 # Turnos totales, 100 por jugador
player_id = int(input())


class nodo:
    def __init__(self, estado):
        self.estado = estado
    
        

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
                nuevoNodo = aplica(movimiento, nodo)
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
while True:
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
