import sys
import math
import copy

class Nodo:
    def __init__(self, tablero, tarjetas, turno):
        self.tablero = tablero
        self.tarjetas = tarjetas
        self.turno = turno

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

    for i in range(len(nodo.tablero)):
        for j in range(len(nodo.tablero)):
            if (nodo.tablero[i][j] == master or nodo.tablero[i][j] == peon):
                for tarjeta in nodo.tarjetas:
                    if tarjeta.owner == nodo.turno:
                        for casilla in tarjeta.casillas:
                            if esPosible([i, j], casilla, nodo.tablero, nodo.turno):
                                movimientos.append(
                                    [tarjeta.owner,
                                    tarjeta.card_id,
                                    [[i, j], [i-casilla[1],j+casilla[0]]]]
                                    )
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
        elif c.owner == -1:         # Tarjeta del medio
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

    aux = tableroAux[posIni[0]][posIni[1]]
    tableroAux[posIni[0]][posIni[1]] = tableroAux[posFin[0]][posFin[1]]
    tableroAux[posFin[0]][posFin[1]] = aux
    
    return tableroAux

def aplica(mov, nodo):
    # mov[0] owner, mov[1] cardId, mov[2] [posIni, posFin]
    tableroAux = intercambio(nodo.tablero, mov[2][0], mov[2][1])
    tarjetasAux = jugar_carta(nodo.tarjetas, mov[1], mov[0])   
    turnoAux = 1 - nodo.turno

    return Nodo(tableroAux, tarjetasAux, turnoAux)

def eval(nodo_param):
    score = 0
    
    master_propio = "W" if nodo_param.turno == 0 else "B"
    master_rival = "B" if master_propio == "W" else "W"
    peon_propio = "w" if nodo_param.turno == 0 else "b"
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
    score += (piezas_propias - piezas_rival)

    xm, ym = encontrarMaster(nodo_param.tablero, master_propio)
    xr, yr = encontrarMaster(nodo_param.tablero, master_rival)
    
    shrine_propio = (4,2) if nodo_param.turno == 0 else (0,2)
    shrine_rival = (0,2) if nodo_param.turno == 0 else (4,2)

    dm_m = distancia_manhattan_shrine(xm, ym, shrine_rival)
    dm_r = distancia_manhattan_shrine(xr, yr, shrine_propio)
    valor_distancia = (dm_m - dm_r)
    score += valor_distancia

    '''
    # Si estoy en la shrine o si no hay master rival
    if (xm, ym) == shrine_rival: #or (xr, yr) == (-1, -1):
        return math.inf
    # Si el rival está en la shrine o si no tengo master
    if (xr, yr) == shrine_propio: #or (xm, ym) == (-1, -1):
        return -math.inf

    
    # Distancia shrine TODO: darle peso a la distancia segun la cantidad de piezas en el tablero
    dm_m = distancia_manhattan_shrine(xm, ym, shrine_rival)
    dm_r = distancia_manhattan_shrine(xr, yr, shrine_propio)
    valor_distancia = (dm_m - dm_r)
    score += valor_distancia

    # Control centro
    valor_centro_propio = 0
    valor_centro_rival = 0

    centro = [(2,2), (2,1), (2,3)]
    for i, j in centro:
        if nodo_param.tablero[i][j] == master_propio.lower():
            valor_centro_propio += 1
        elif nodo_param.tablero[i][j] == master_rival.lower():
            valor_centro_rival += 1
    score += (valor_centro_propio - valor_centro_rival)
    '''

    return score

def alpha_beta(nodo, profundidad, alfa, beta, jugadorMAX):
    if profundidad == 0 or esFinal(nodo):
        return eval(nodo), None

    movimientos = calcularMovimientosPosibles(nodo)
    print(movimientos, file=sys.stderr, flush=True)
    
    if jugadorMAX:
        valor = -math.inf
        mejorMov = None
        for mov in movimientos:
            nuevoNodo = aplica(mov, nodo)
            valNuevoNodo, sigMov = alpha_beta(nuevoNodo, profundidad, alfa, beta, False)
            if valNuevoNodo > valor:
                valor = valNuevoNodo
                mejorMov = mov
                alfa = valor
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
                beta = valor
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
    
    nodoInicial = Nodo(board, cards, player_id)

    if (len(actions) > 0):
        valor, movimiento = alpha_beta(nodoInicial, 2, -math.inf, math.inf, True) # movimiento como posicion -> [posIni, posFin]
        print(valor, movimiento[2], file=sys.stderr, flush=True)
        card_id = movimiento[1]
        move = traducirPosicionAMovimiento(movimiento[2])
        print(card_id, move) # cardID MOVE
    else:
        print('PASS')
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
