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

def heuristica(board, tarjetas):
    heur = 0
    x_master, y_master = encontrarMaster(board)
    distancia_master = distancia_manhattan(x_master, y_master)

    vivasMias = 0
    vivasRival = 0
    for i in range(5):
        vivasMias += ''.join(board[i]).count("b")
        vivasRival += ''.join(board[i]).count("w")

    peso_tarjetas = 0.2
    tarjetasMias = []
    for tj in tarjetas:
        if tj.owner == 0:
            tarjetasMias.append(tj)

    for i in range(vivasMias):
        pass
    #valor_tarjetas = movilidad(board, tarjetasMias[0].owner, posicion_actual)

    peso_distancia = 0.45 + (5 - (vivasMias + vivasRival)) * 0.1
    
    heur += (vivasMias-vivasRival)*0.55 
    heur += distancia_master*peso_distancia
    #heur += valor_tarjetas*peso_tarjetas
    return heur

def traducirPosicion(caracter):
    if caracter.isdigit():
        return 5-int(caracter)
    else:
        return ord(caracter)-ord('A')

def swap(board, posInic, posFin):
    aux = board[posInic[0]][posInic[1]]
    board[posInic[0]][posInic[1]] = board[posFin[0]][posFin[1]] 
    board[posFin[0]][posFin[1]] = aux

def traducirAccionATarjeta(accionIni, accionFin):
    return accionFin[0]-accionIni[0], accionFin[1]-accionIni[1]

def jugarCarta(tarjetas, num_tarjeta, posIni, posFin):
    i=0
    tarjeta = tarjetas[i]
    while i <= len(tarjetas) and tarjeta.card_id != num_tarjeta:
        tarjeta = tarjetas[++i]

    i=0
    tarjetaMedio = tarjetas[i]
    while i <= len(tarjetas) and tarjetaMedio.owner != -1:
        tarjetaMedio = tarjetas[++i]
    
    if tarjeta.owner == 0:
        tarjetaMedio.owner = 0
    else:
        tarjetaMedio.owner = 1
    tarjeta.owner = -1


    dx, dy = traducirAccionATarjeta(posIni, posFin)    

    if tarjeta.dx1 == dx and tarjeta.dy1 == dy:
        tarjeta.dx1 *= -1
        tarjeta.dy1 *= -1
    if tarjeta.dx2 == dx and tarjeta.dy2 == dy:
        tarjeta.dx2 *= -1
        tarjeta.dy2 *= -1
    if tarjeta.dx3 == dx and tarjeta.dy3 == dy:
        tarjeta.dx3 *= -1
        tarjeta.dy3 *= -1
    if tarjeta.dx4 == dx and tarjeta.dy4 == dy:
        tarjeta.dx4 *= -1
        tarjeta.dy4 *= -1



def realizarAccion(board, accion, tarjetasCopy):
    posIni = [traducirPosicion(accion[1][0]), traducirPosicion(accion[1][1])]
    posFin = [traducirPosicion(accion[1][2]), traducirPosicion(accion[1][3])]
    swap(board, posIni, posFin)
    jugarCarta(tarjetasCopy, accion[0], posIni, posFin)

def evaluarPuntuacionAccion(accion, board, tarjetas):
    boardCopy = board.copy()
    tarjetasCopy = tarjetas.deepcopy()
    realizarAccion(boardCopy, accion, tarjetasCopy)
    return heuristica(boardCopy, tarjetasCopy)


# game loop
while True:
    # Tablero
    board = []
    for i in range(5):
        row = input()
        board.append(row)
    
    transformarTablero(board)

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

    #puntuacion = heuristica(board)

    if len(acciones) > 0:
        #accion_puntuacion = []
        maxAccion = [[]]
        maxPuntuacion = -math.inf
        
        for ac in acciones:

            points = evaluarPuntuacionAccion(ac, board, tarjetas)
            print(points, file=sys.stderr, flush=True)
            if maxPuntuacion < points:
                maxPuntuacion = points
                maxAccion = ac
        
        print(maxPuntuacion, file=sys.stderr, flush=True)
        
        print(maxAccion[0], maxAccion[1])
    else:
        print("PASS")