# Codigo optimizado
import sys
import time

INF = 1000000

class Nodo:
    def __init__(self, tablero, tarjetas, turno, player_id, vivasTotal, vivasMias, vivasRival):
        self.tablero = tablero
        self.tarjetas = tarjetas
        self.turno = turno
        self.player_id = player_id
        self.vivasTotal = vivasTotal
        self.vivasMias = vivasMias
        self.vivasRival = vivasRival

class Tarjeta:
    def __init__(self, owner, cardId, dx_1,dy_1, dx_2,dy_2, dx_3,dy_3, dx_4,dy_4):
        self.owner = owner
        self.card_id = cardId
        self.casillas = [[dx_1, dy_1], [dx_2, dy_2], [dx_3, dy_3], [dx_4, dy_4]]

caracter_a_pos = {'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, '5' : 0, '4' : 1, '3' : 2, '2' : 3, '1' : 4}

def traducirMovimientoAPosicion(movimiento):
    posIni = [caracter_a_pos[movimiento[1]], caracter_a_pos[movimiento[0]]]
    posFin = [caracter_a_pos[movimiento[3]], caracter_a_pos[movimiento[2]]]
    return posIni, posFin

def traducirPosicionAMovimiento(posicion):
    letras = 'ABCDE'
    numeros = '54321'
    
    return ''.join([letras[cod_letra] + numeros[cod_numero] for cod_numero, cod_letra in posicion])

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
    # Determinar qué piezas buscar según el turno (caching en variables locales)
    master = "W" if nodo.turno == 0 else "B"
    peon = "w" if nodo.turno == 0 else "b"
    
    # Pre-almacenar el tablero para acceso rápido
    tablero = nodo.tablero
    turno = nodo.turno
    
    # Lista pre-asignada para mejor manejo de memoria
    movimientos = []
    
    # Filtrar tarjetas disponibles una sola vez
    tarjetas_disponibles = [t for t in nodo.tarjetas if t.owner == turno]
    
    # Encontrar piezas una sola vez y guardarlas - usando comprensión de listas optimizada
    piezas = []
    for i in range(5):
        for j in range(5):
            if tablero[i][j] == master or tablero[i][j] == peon:
                piezas.append((i, j))
    
    # Optimización de bucles anidados
    for tarjeta in tarjetas_disponibles:
        owner = tarjeta.owner
        card_id = tarjeta.card_id
        casillas = tarjeta.casillas
        
        for i, j in piezas:
            origen = [i, j]
            
            for casilla in casillas:
                # Calcular coordenadas destino una sola vez
                dx, dy = casilla
                x, y = i - dy, j + dx
                
                # Verificar límites antes de llamar a esPosible (evita llamadas innecesarias)
                if 0 <= x < 5 and 0 <= y < 5:
                    destino = [x, y]
                    
                    # Verificación rápida: si es una pieza propia, no es válido (inlined)
                    pieza_destino = tablero[x][y]
                    piezas_propias = ["W", "w"] if turno == 0 else ["B", "b"]
                    
                    if pieza_destino not in piezas_propias:
                        # Solo llamar a esPosible si pasó las verificaciones básicas
                        if esPosible(origen, casilla, tablero, turno):
                            movimientos.append([owner, card_id, [origen, destino]])
    
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

def intercambio(tablero, posIni, posFin, player_id, vivas):
    tableroAux = [fila.copy() for fila in tablero]
    
    if tableroAux[posFin[0]][posFin[1]] != '-':
        vivas[0] -= 1
        if tableroAux[posFin[0]][posFin[1]].lower() == "b" and player_id == 0:
            vivas[2] -= 1
        elif tableroAux[posFin[0]][posFin[1]].lower() == "b":
            vivas[1] -= 1
        tableroAux[posFin[0]][posFin[1]] = '-'

    tableroAux[posIni[0]][posIni[1]], tableroAux[posFin[0]][posFin[1]] = tableroAux[posFin[0]][posFin[1]], tableroAux[posIni[0]][posIni[1]]
    
    return tableroAux

def aplica(mov, nodo):
    # mov[0] owner, mov[1] cardId, mov[2] [posIni, posFin]
    listaVivas = [nodo.vivasTotal, nodo.vivasMias, nodo.vivasRival]
    tableroAux = intercambio(nodo.tablero, mov[2][0], mov[2][1], player_id, listaVivas)
    tarjetasAux = jugar_carta(nodo.tarjetas, mov[1], mov[0])
    turnoAux = 1 - nodo.turno

    return Nodo(tableroAux, tarjetasAux, turnoAux, nodo.player_id, listaVivas[0], listaVivas[1], listaVivas[2])

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

    # Posiciones centrales
    posiciones_centrales = {(2,2), (2,1), (2,3)}

    # Bucle principal para encontrar piezas
    for i in range(len(nodo_param.tablero)): 
        for j in range(len(nodo_param.tablero)):
            pos = nodo_param.tablero[i][j]
            if pos == master_propio:
                xm, ym = i, j
                piezas_propias += 1
            elif pos == master_rival:
                xr, yr = i, j
                piezas_rival += 1
            elif pos == peon_propio:
                piezas_propias += 1
            elif pos == peon_rival:
                piezas_rival += 1
            
            if (i,j) in posiciones_centrales:
                if pos == peon_propio: centro_propio += 1
                elif pos == peon_rival: centro_rival += 1
                
    # Si no se encuentra alguno de los masters
    if xm == -1: return -INF
    if xr == -1: return INF

    dm_m = abs(xm-shrine_rival[0]) + abs(ym-shrine_rival[1])
    dm_r = abs(xr-shrine_propio[0]) + abs(yr-shrine_propio[1])
    
    # Si alguno de los masters llego a la shrine
    if dm_m == 0: return INF
    if dm_r == 0: return -INF
    
    # Suma de puntuacion
    score += (piezas_propias - piezas_rival)*0.6
    score += (centro_propio - centro_rival)*0.1

    return score

# Funcion simple para ordenar calcularMovimientosPosibles() de forma rapida
def eval_simplified(mov, nodo):
    return nodo.vivasMias-nodo.vivasRival

def alpha_beta(nodo, profundidad, alfa, beta, jugadorMAX, tiempo_inicio, limite_ms):
    if profundidad == 0 or esFinal(nodo):
        return eval(nodo), None

    movimientos = sorted(calcularMovimientosPosibles(nodo), # Lista movimientos
                   key=lambda m: eval_simplified(m, nodo),  # Para cada uno ordenar por eval_simplified()
                   reverse=jugadorMAX)                      # Si MAX, descendente. Si MIN, ascendente.

    if jugadorMAX:
        valor = -INF-1
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
        valor = INF+1
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

player_id = int(input())
turno = 0 if player_id == 0 else 1

# game loop
while True:
    board = []
    vivasMias = 0
    vivasRival = 0
    for i in range(5):
        row = input()
        vivasMias += row.count("w")
        vivasMias += row.count("W")
        vivasRival += row.count("b")
        vivasRival += row.count("B")
        board.append(list(row))
    vivasTotal = vivasMias+vivasRival

    cards = []
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        card = Tarjeta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        cards.append(card)

    actions = []
    action_count = int(input())

    for i in range(action_count):
        inputs = input().split()

    nodoInicial = Nodo(board, cards, turno, player_id, vivasTotal, vivasMias, vivasRival)

    if (action_count > 0):
        start_time = time.time()
        valor, movimiento = alpha_beta(nodoInicial, 3, -INF, INF, True, start_time, 45) # movimiento como posicion -> [posIni, posFin], tiempo limite 45ms
        print(valor, file=sys.stderr, flush=True)
        card_id = movimiento[1]
        move = traducirPosicionAMovimiento(movimiento[2])
        print(card_id, move) # cardID MOVE
    else:
        print('PASS')