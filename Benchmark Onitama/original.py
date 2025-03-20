# Codigo original

import time

INF = 1000000

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

    for tarjeta in tarjetas_disponibles:
        for i, j in piezas:
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
    tableroAux = [fila.copy() for fila in tablero]
    
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
    # Declaracion de variables
    score = 0
    (master_propio, master_rival) = ("W","B") if nodo_param.player_id == 0 else ("B","W")
    (shrine_propio, shrine_rival) = ((4,2),(0,2)) if nodo_param.player_id == 0 else ((0,2),(4,2))
    peon_propio = master_propio.lower()
    peon_rival = master_rival.lower()

    piezas_propias = piezas_rival = 0
    centro_propio = centro_rival = 0

    xm = ym = xr = yr = -1

    # Bucle principal para encontrar piezas
    for i in range(len(nodo_param.tablero)): 
        for j in range(len(nodo_param.tablero)):
            pos = nodo_param.tablero[i][j]
            if pos == master_propio:
                xm, ym = i, j
                piezas_propias += 10
            elif pos == master_rival:
                xr, yr = i, j
                piezas_rival += 10
            elif pos == peon_propio:
                piezas_propias += 1
            elif pos == peon_rival:
                piezas_rival += 1
            
            if (i,j) in [(2,2), (2,1), (2,3)]:
                if pos == peon_propio: centro_propio += 1
                elif pos == peon_rival: centro_rival += 1
                
    # Si no se encuentra alguno de los masters
    if xm == -1: return -INF
    if xr == -1: return INF

    dm_m = distancia_manhattan_shrine(xm, ym, shrine_rival)
    dm_r = distancia_manhattan_shrine(xr, yr, shrine_propio)
    
    # Si alguno de los masters llego a la shrine
    if dm_m == 0: return INF
    if dm_r == 0: return -INF
    
    # Suma de puntuacion
    score += (piezas_propias - piezas_rival)*0.6
    score += (centro_propio - centro_rival)*0.1

    return score

# Funcion simple para ordenar calcularMovimientosPosibles() de forma rapida
def eval_simplified(mov, nodo):
    shrine_rival = (0,2) if nodo.player_id == 0 else (4,2)

    pos_fin = mov[2][1]
    return -distancia_manhattan_shrine(pos_fin[0], pos_fin[1], shrine_rival)


def alpha_beta(nodo, profundidad, alfa, beta, jugadorMAX, tiempo_inicio, limite_ms):
    if (time.time() - tiempo_inicio) * 1000 >= limite_ms:
        return eval(nodo), None

    if profundidad == 0 or esFinal(nodo):
        return eval(nodo), None

    movimientos = sorted(calcularMovimientosPosibles(nodo), # Lista movimientos
                   key=lambda m: eval_simplified(m, nodo),  # Para cada uno ordenar por eval_simplified()
                   reverse=jugadorMAX)                      # Si MAX, descendente. Si MIN, ascendente.

    if jugadorMAX:
        valor = -INF
        mejorMov = None
        for mov in movimientos:
            nuevoNodo = aplica(mov, nodo)
            valNuevoNodo, _ = alpha_beta(nuevoNodo, profundidad-1, alfa, beta, False, tiempo_inicio, limite_ms)
            if valNuevoNodo > valor:
                valor = valNuevoNodo
                mejorMov = mov
                alfa = max(alfa, valor)
            if alfa >= beta or (time.time() - tiempo_inicio) * 1000 >= limite_ms:
                break
        return valor, mejorMov
    
    else:
        valor = INF
        mejorMov = None
        for mov in movimientos:
            nuevoNodo = aplica(mov, nodo)
            valNuevoNodo, _ = alpha_beta(nuevoNodo, profundidad-1, alfa, beta, True, tiempo_inicio, limite_ms)
            if valNuevoNodo < valor:
                valor = valNuevoNodo
                mejorMov = mov
                beta = min(beta, valor)
            if alfa >= beta or (time.time() - tiempo_inicio) * 1000 >= limite_ms:
                break
        return valor, mejorMov