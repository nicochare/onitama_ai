import sys
import math
import copy

class Nodo:
    def __init__(self, tablero, tarjetas, turno, player_id):
        self.tablero = tablero
        self.tarjetas = tarjetas
        self.turno = turno
        self.player_id = player_id

class Tarjeta:
    def __init__(self, owner, cardId, dx_1,dy_1, dx_2,dy_2, dx_3,dy_3, dx_4,dy_4):
        self.owner = owner
        self.card_id = cardId
        self.casillas = [[dx_1, dy_1], [dx_2, dy_2], [dx_3, dy_3], [dx_4, dy_4]]

def transformarTablero(tablero):
    for i in range(5):
        tablero[i] = list(tablero[i])

def encontrarMaster(tablero, masterCaracter):
    for i in range(5):
        for j in range(5):
            if tablero[i][j] == masterCaracter:
                return [i, j]
    return [-1, -1]

def distancia_manhattan(i, i2, j, j2):
    return abs(i-i2) + abs(j-j2)

def distancia_manhattan_shrine(i, j, shrine):
    return distancia_manhattan(i, shrine[0], j, shrine[1])

def traducirCaracter(caracter):
    if caracter.isdigit():
        return ord('5')-ord(caracter)
    else:
        return ord(caracter)-ord('A')

def traducirMovimientoAPosicion(movimiento):
    posIni = [traducirCaracter(movimiento[1]), traducirCaracter(movimiento[0])]
    posFin = [traducirCaracter(movimiento[3]), traducirCaracter(movimiento[2])]

    return posIni, posFin

def traducirPosicionAMovimiento(posicion):
    accion = ""
    for coord in posicion:
        cod_numero, cod_letra = coord
        
        letra = chr(cod_letra + ord('A')) # Convierte 0->'A', 1->'B', ...
        numero = chr(ord('5') - cod_numero) # Convierte 0->'5', 1->'4', ...

        accion += letra + numero

    return accion

def esPosible(pieza, casilla, tablero, turno):
    nueva_fila = pieza[0] - casilla[1]
    nueva_columna = pieza[1] + casilla[0] 

    if not (0 <= nueva_fila < 5 and 0 <= nueva_columna < 5):
        return False
    
    if turno == 0 and tablero[nueva_fila][nueva_columna] in ('w', 'W'):
        return False
    if turno == 1 and tablero[nueva_fila][nueva_columna] in ('b', 'B'):
        return False

    return True

def calcularMovimientosPosibles(nodo):
    master = "W" if nodo.turno == 0 else "B"
    peon = "w" if nodo.turno == 0 else "b"

    movimientos = []
    piezas = [(i, j) for i in range(5) for j in range(5) if nodo.tablero[i][j] in (master, peon)]
    tarjetas_disponibles = [t for t in nodo.tarjetas if t.owner == nodo.turno]

    for i, j in piezas:
        for tarjeta in tarjetas_disponibles:
            for casilla in tarjeta.casillas:
                if esPosible([i, j], casilla, nodo.tablero, nodo.turno):
                    movimientos.append([tarjeta.owner, tarjeta.card_id, [[i, j], [i - casilla[1], j + casilla[0]]]])
    
    return movimientos

def esFinal(nodo):
    if nodo.tablero[0][2] == "W" or nodo.tablero[4][2] == "B":
        return True
    
    cantMasters = 0
    
    for fila in nodo.tablero:
        cantMasters += fila.count("B")
        cantMasters += fila.count("W")

    return cantMasters != 2

def jugar_carta(cards, cardId, owner):
    new_cards = []
    for c in cards:
        if c.card_id == cardId: # Tarjeta a jugar
            new_cards.append(Tarjeta(
                -1,
                c.card_id,
                -c.casillas[0][0], -c.casillas[0][1],
                -c.casillas[1][0], -c.casillas[1][1],
                -c.casillas[2][0], -c.casillas[2][1],
                -c.casillas[3][0], -c.casillas[3][1]
            ))
        elif c.owner == -1:     # Tarjeta del medio
            new_cards.append(Tarjeta(
                owner,
                c.card_id,
                c.casillas[0][0], c.casillas[0][1],
                c.casillas[1][0], c.casillas[1][1],
                c.casillas[2][0], c.casillas[2][1],
                c.casillas[3][0], c.casillas[3][1]
            ))
        else:
            new_cards.append(Tarjeta(
                c.owner,
                c.card_id,
                c.casillas[0][0], c.casillas[0][1],
                c.casillas[1][0], c.casillas[1][1],
                c.casillas[2][0], c.casillas[2][1],
                c.casillas[3][0], c.casillas[3][1]
            ))
    return new_cards

def intercambio(tablero, posIni, posFin):
    tableroAux = copy.deepcopy(tablero)
    
    if tableroAux[posFin[0]][posFin[1]] != '-':
        tableroAux[posFin[0]][posFin[1]] = '-'

    tableroAux[posIni[0]][posIni[1]], tableroAux[posFin[0]][posFin[1]] = tableroAux[posFin[0]][posFin[1]], tableroAux[posIni[0]][posIni[1]]
    
    return tableroAux

def aplica(mov, nodo):
    # mov[0] owner, mov[1] cardId, mov[2] [posIni, posFin]
    tableroAux = intercambio(nodo.tablero, mov[2][0], mov[2][1])
    tarjetasAux = jugar_carta(nodo.tarjetas, mov[1], mov[0])   
    turnoAux = 1 - nodo.turno

    return Nodo(tableroAux, tarjetasAux, turnoAux, nodo.player_id)

def eval(nodo_param):
    score = 0
    
    master_propio = "W" if nodo_param.player_id == 0 else "B"
    master_rival = "B" if master_propio == "W" else "W"
    peon_propio = "w" if nodo_param.player_id == 0 else "b"
    peon_rival = "b" if peon_propio == "w" else "w"

    piezas_propias = 0
    piezas_rival = 0

    for i in range(len(nodo_param.tablero)): 
        for j in range(len(nodo_param.tablero)): 
            if nodo_param.tablero[i][j] == master_propio:
                piezas_propias += 10
            elif nodo_param.tablero[i][j] == master_rival:
                piezas_rival += 10
            elif nodo_param.tablero[i][j] == peon_propio:
                piezas_propias += 1
            elif nodo_param.tablero[i][j] == peon_rival:
                piezas_rival += 1
    score += (piezas_propias - piezas_rival)*0.6

    xm, ym = encontrarMaster(nodo_param.tablero, master_propio)
    xr, yr = encontrarMaster(nodo_param.tablero, master_rival)
    
    shrine_propio = (4,2) if nodo_param.player_id == 0 else (0,2)
    shrine_rival = (0,2) if nodo_param.player_id == 0 else (4,2)

    dm_m = distancia_manhattan_shrine(xm, ym, shrine_rival)
    if dm_m == 0:
        return math.inf

    dm_r = distancia_manhattan_shrine(xr, yr, shrine_propio)
    if dm_r == 0:
        return -math.inf
    
    score += (dm_m - dm_r)*0.3

    centro = [(2,2), (2,1), (2,3)]
    piezas_propias_centro = 0
    piezas_rival_centro = 0
    for i, j in centro:
        if nodo_param.tablero[i][j] == master_propio.lower():
            piezas_propias_centro += 1
        elif nodo_param.tablero[i][j] == master_rival.lower():
            piezas_rival_centro += 1
    score += (piezas_propias_centro - piezas_rival_centro)*0.1

    return score

def alpha_beta(nodo, profundidad, alfa, beta, jugadorMAX):
    if profundidad == 0 or esFinal(nodo):
        return eval(nodo), None
    
    movimientos = calcularMovimientosPosibles(nodo)

    if jugadorMAX:
        valor = -math.inf
        mejorMov = None
        for mov in movimientos:
            nuevoNodo = aplica(mov, nodo)
            valNuevoNodo, sigMov = alpha_beta(nuevoNodo, profundidad-1, alfa, beta, False)
            if valNuevoNodo > valor:
                valor = valNuevoNodo
                mejorMov = mov
                alfa = max(alfa, valor)
            if alfa >= beta:
                break
        return valor, mejorMov
    
    else:
        valor = math.inf
        mejorMov = None
        for mov in movimientos:
            nuevoNodo = aplica(mov, nodo)
            valNuevoNodo, sigMov = alpha_beta(nuevoNodo, profundidad-1, alfa, beta, True)
            if valNuevoNodo < valor:
                valor = valNuevoNodo
                mejorMov = mov
                beta = min(beta, valor)
            if alfa >= beta:
                break
        return valor, mejorMov

player_id = int(input())

# game loop
while True:
    board = []
    for i in range(5):
        row = input()
        board.append(list(row))

    cards = []
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        card = Tarjeta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        cards.append(card)

    # estas acciones siempre van a ser posibles
    actions = []
    action_count = int(input())

    for i in range(action_count):
        inputs = input().split()
        card_id = int(inputs[0])
        move = inputs[1]
        posIni, posFin = traducirMovimientoAPosicion(move)
        actions.append([player_id, card_id, [posIni, posFin]])
    
    nodoInicial = Nodo(board, cards, 0, player_id)

    if (len(actions) > 0):
        valor, movimiento = alpha_beta(nodoInicial, 3, -math.inf, math.inf, True) # movimiento como posicion -> [posIni, posFin]
        card_id = movimiento[1]
        move = traducirPosicionAMovimiento(movimiento[2])
        print(card_id, move) # cardID MOVE
    else:
        print('PASS')
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)