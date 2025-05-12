import time

INF = 1000000 # 10 ^ 6	

class Nodo:
    def __init__(self, tablero, tarjetas, turno, player_id, vivas_total, vivas_mias, vivas_rival):
        self.tablero = tablero
        self.tarjetas = tarjetas
        self.turno = turno
        self.player_id = player_id
        self.vivas_total = vivas_total
        self.vivas_mias = vivas_mias
        self.vivas_rival = vivas_rival

class Tarjeta:
    def __init__(self, owner, card_id, dx_1,dy_1, dx_2,dy_2, dx_3,dy_3, dx_4,dy_4):
        self.owner = owner
        self.card_id = card_id
        self.casillas = [[dx_1, dy_1], [dx_2, dy_2], [dx_3, dy_3], [dx_4, dy_4]]

def traducir_posicion_a_movimiento(posicion):
    letras = 'ABCDE'
    numeros = '54321'
    
    return ''.join([letras[cod_letra] + numeros[cod_numero] for cod_numero, cod_letra in posicion])

def es_posible(pieza, casilla, tablero, turno):
    nueva_fila = pieza[0] - casilla[1]
    nueva_columna = pieza[1] + casilla[0] 

    if not (0 <= nueva_fila < 5 and 0 <= nueva_columna < 5):
        return False
    if turno == 0 and tablero[nueva_fila][nueva_columna] in ('w', 'W'):
        return False
    if turno == 1 and tablero[nueva_fila][nueva_columna] in ('b', 'B'):
        return False

    return True

def calcular_movimientos_posibles(nodo):
    master = "W" if nodo.turno == 0 else "B"
    peon = "w" if nodo.turno == 0 else "b"    
    tablero = nodo.tablero
    turno = nodo.turno
    movimientos = []
    piezas = []
    tarjetas_disponibles = [t for t in nodo.tarjetas if t.owner == turno]
    
    for i in range(5):
        for j in range(5):
            if tablero[i][j] == master or tablero[i][j] == peon:
                piezas.append((i, j))
    
    for tarjeta in tarjetas_disponibles:
        owner = tarjeta.owner
        card_id = tarjeta.card_id
        casillas = tarjeta.casillas
        
        for i, j in piezas:
            origen = [i, j]

            for casilla in casillas:
                dx, dy = casilla
                x, y = i - dy, j + dx

                if 0 <= x < 5 and 0 <= y < 5:
                    destino = [x, y]                    
                    pieza_destino = tablero[x][y]
                    piezas_propias = ["W", "w"] if turno == 0 else ["B", "b"]
                    
                    if pieza_destino not in piezas_propias:
                        if es_posible(origen, casilla, tablero, turno):
                            movimientos.append([owner, card_id, [origen, destino]])
    
    return movimientos

def es_final(nodo):
    if nodo.tablero[0][2] == "W" or nodo.tablero[4][2] == "B":
        return True
    
    cant_masters = 0
    
    for fila in nodo.tablero:
        cant_masters += fila.count("B")
        cant_masters += fila.count("W")

    return cant_masters != 2

def jugar_carta(cards, card_id, owner):
    new_cards = []
    for c in cards:
        if c.card_id == card_id: # Tarjeta a jugar
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

def intercambio(tablero, pos_ini, pos_fin, player_id, vivas):
    tablero_aux = [fila.copy() for fila in tablero]
    
    if tablero_aux[pos_fin[0]][pos_fin[1]] != '-':
        vivas[0] -= 1
        if tablero_aux[pos_fin[0]][pos_fin[1]].lower() == "b" and player_id == 0:
            vivas[2] -= 1
        elif tablero_aux[pos_fin[0]][pos_fin[1]].lower() == "b":
            vivas[1] -= 1
        tablero_aux[pos_fin[0]][pos_fin[1]] = '-'

    tablero_aux[pos_ini[0]][pos_ini[1]], tablero_aux[pos_fin[0]][pos_fin[1]] = tablero_aux[pos_fin[0]][pos_fin[1]], tablero_aux[pos_ini[0]][pos_ini[1]]
    
    return tablero_aux

def aplica(mov, nodo):
    # mov = [owner, card_id, [pos_ini, pos_fin]]
    lista_vivas = [nodo.vivas_total, nodo.vivas_mias, nodo.vivas_rival]
    tablero_aux = intercambio(nodo.tablero, mov[2][0], mov[2][1], player_id, lista_vivas)
    tarjetas_aux = jugar_carta(nodo.tarjetas, mov[1], mov[0])
    turno_aux = 1 - nodo.turno

    return Nodo(tablero_aux, tarjetas_aux, turno_aux, nodo.player_id, lista_vivas[0], lista_vivas[1], lista_vivas[2])

def eval(nodo_param):
    score = 0
    (master_propio, master_rival) = ("W","B") if nodo_param.player_id == 0 else ("B","W")
    (shrine_propio, shrine_rival) = ((4,2),(0,2)) if nodo_param.player_id == 0 else ((0,2),(4,2))
    
    peon_propio = master_propio.lower()
    peon_rival = master_rival.lower()

    piezas_propias = piezas_rival = 0
    centro_propio = centro_rival = 0

    xm = ym = xr = yr = -1

    posiciones_centrales = {(2,2), (2,1), (2,3)}

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
                
    if xm == -1: return -INF
    if xr == -1: return INF

    dm_m = abs(xm-shrine_rival[0]) + abs(ym-shrine_rival[1])
    dm_r = abs(xr-shrine_propio[0]) + abs(yr-shrine_propio[1])
    
    if dm_m == 0: return INF
    if dm_r == 0: return -INF
    
    score += (piezas_propias - piezas_rival)*0.6
    score += (centro_propio - centro_rival)*0.1

    return score

# Funcion simple para ordenar calcular_movimientos_posibles() de forma rapida
def eval_simplified(movimiento, nodo):
    nodoCopiado = aplica(movimiento, nodo)
    return nodoCopiado.vivas_mias-nodoCopiado.vivas_rival

def alpha_beta(nodo, profundidad, alfa, beta, jugadorMAX, tiempo_inicio, limite_ms):
    if profundidad == 0 or es_final(nodo):
        return eval(nodo), None

    movimientos = sorted(calcular_movimientos_posibles(nodo),
                key=lambda m: eval_simplified(m, nodo),
                reverse=jugadorMAX)

    if jugadorMAX:
        valor = -INF-1
        mejor_mov = None
        for mov in movimientos:
            nuevo_nodo = aplica(mov, nodo)
            val_nuevo_nodo, _ = alpha_beta(nuevo_nodo, profundidad-1, alfa, beta, False, tiempo_inicio, limite_ms)
            if val_nuevo_nodo > valor:
                valor = val_nuevo_nodo
                mejor_mov = mov
                alfa = max(alfa, valor)
            if alfa >= beta or (time.time() - tiempo_inicio) * 1000 >= limite_ms:
                break
        return valor, mejor_mov
    
    else:
        valor = INF+1
        mejor_mov = None
        for mov in movimientos:
            nuevo_nodo = aplica(mov, nodo)
            val_nuevo_nodo, _ = alpha_beta(nuevo_nodo, profundidad-1, alfa, beta, True, tiempo_inicio, limite_ms)
            if val_nuevo_nodo < valor:
                valor = val_nuevo_nodo
                mejor_mov = mov
                beta = min(beta, valor)
            if alfa >= beta or (time.time() - tiempo_inicio) * 1000 >= limite_ms:
                break
        return valor, mejor_mov

player_id = int(input())
turno = 0 if player_id == 0 else 1

while True:
    board = []
    vivas_mias = 0
    vivas_rival = 0
    for i in range(5):
        row = input()
        vivas_mias += row.count("w")
        vivas_mias += row.count("W")
        vivas_rival += row.count("b")
        vivas_rival += row.count("B")
        board.append(list(row))
    vivas_total = vivas_mias+vivas_rival

    cards = []
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        card = Tarjeta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        cards.append(card)

    actions = []
    action_count = int(input())

    for i in range(action_count):
        inputs = input().split()

    nodoInicial = Nodo(board, cards, turno, player_id, vivas_total, vivas_mias, vivas_rival)

    if (action_count > 0):
        start_time = time.time()
        valor, movimiento = alpha_beta(nodoInicial, 3, -INF, INF, True, start_time, 45)
        card_id = movimiento[1]
        move = traducir_posicion_a_movimiento(movimiento[2])
        print(card_id, move)
    else:
        print('PASS')