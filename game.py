import sys
import math
import copy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Tarjeta:
    def __init__(self, owner, card_id, dx_1,dy_1, dx_2,dy_2, dx_3,dy_3, dx_4,dy_4):
        self.owner = owner
        self.card_id = card_id
        self.dx_1 = dx_1
        self.dy_1 = dy_1
        self.dx_2 = dx_2
        self.dy_2 = dy_2
        self.dx_3 = dx_3
        self.dy_3 = dy_3
        self.dx_4 = dx_4
        self.dy_4 = dy_4

class Nodo:
    def __init__(self, board, cards, turno):
        self.board = board
        self.cards = cards
        self.turno = turno

    # def generar_acciones_validas(self):
    #     master = "W" if self.turno == 0 else "B"
    #     peon = "w" if self.turno == 0 else "b"

    #     movimientos = []

    #     for i in range(len(self.board)):
    #         for j in range(len(self.board)):
    #             if (self.board[i][j] == master or self.board[i][j] == peon):
    #                 for card in self.cards:
    #                     if card.owner == self.turno:
    #                         casillas = [
    #                             (card.dx_1, card.dy_1),
    #                             (card.dx_2, card.dy_2),
    #                             (card.dx_3, card.dy_3),
    #                             (card.dx_4, card.dy_4)
    #                         ]
    #                         for dx, dy in casillas:
    #                             pos_fin = [i - dy, j + dx]
    #                             mov = [card.owner, card.card_id, [[i, j], pos_fin]]
    #                             if es_posible(self, mov):
    #                                 movimientos.append(mov)

    #     return movimientos
    
    def imprimir_estado(self):
        print("Turno: ", self.turno, file=sys.stderr, flush=True)
        for fila in board:
            print(fila, file=sys.stderr, flush=True)

def alternar_id(id):
    return 1-id

def distancia_manhattan(i, i2, j, j2):
    return abs(i-i2) + abs(j-j2)

def distancia_manhattan_shrine(i, j, shrine):
    return distancia_manhattan(i, shrine[0], j, shrine[1])

def rival_mas_cercano_master(nodo, xm, ym):
    posiciones = []
    pieza = "B" if nodo.turno == 0 else "W"
    distancia = math.inf
    for i in range(len(nodo.board)): # por cada fila
        fila = "".join(nodo.board[i])
        pos_master = find(fila, pieza.upper())
        if len(pos_master) > 0:
            posiciones.append([i, pos_master[0]]) # Master, solo 1
            if distancia > distancia_manhattan(xm, i, ym, pos_master[0]):
                distancia = distancia_manhattan(xm, i, ym, pos_master[0])
        for j in find(fila, pieza.lower()):
            posiciones.append([i, j])
            if distancia > distancia_manhattan(xm, i, j, ym):
                distancia = distancia_manhattan(xm, i, j, ym)
    return distancia


def encontrar_master(nodo_param, master_caracter):
    for i in range(len(nodo_param.board)):
        for j in range(len(nodo_param.board)):
            if nodo_param.board[i][j] == master_caracter:
                return (i, j)
    return (-1, -1)

def eval(nodo_param):
    score = 0
    master_propio = "W" if nodo_param.turno == 0 else "B"
    master_rival = "B" if master_propio == "W" else "W"

    xm, ym = encontrar_master(nodo_param, master_propio)
    xr, yr = encontrar_master(nodo_param, master_rival)
    centro = [(2,2), (2,1), (2,3)]
    
    shrine_propio = (4,2) if nodo_param.turno == 0 else (0,2)
    shrine_rival = (0,2) if nodo_param.turno == 0 else (4,2)
    
    # Si estoy en la shrine o si no hay master rival
    if (xm, ym) == shrine_rival or (xr, yr) == (-1, -1):
        return 999999
    # Si el rival está en la shrine o si no tengo master
    if (xr, yr) == shrine_propio or (xm, ym) == (-1, -1):
        return -999999
         

    # Piezas vivas
    peso_vivas = 0.55
    vivas_mias = 0
    vivas_rival = 0

    for i in range(5):
        vivas_mias += ''.join(nodo_param.board[i]).count(master_propio.lower())
        vivas_rival += ''.join(nodo_param.board[i]).count(master_rival.lower())
    valor_vivas = (vivas_mias-vivas_rival)/10
    score += valor_vivas*peso_vivas


    # Distancia shrine
    dm_m = distancia_manhattan_shrine(xm, ym, shrine_rival)
    dm_r = distancia_manhattan_shrine(xr, yr, shrine_propio)
    valor_distancia = (dm_m - dm_r)/5
    peso_distancia = 0.25 + (10 - (vivas_mias + vivas_rival)) * 0.5
    score += valor_distancia*peso_distancia

    # Control centro
    valor_centro = 0
    for i, j in centro:
        if nodo_param.board[i][j] == master_propio.lower():
            valor_centro += 1
        elif nodo_param.board[i][j] == master_rival.lower():
            valor_centro -= 1
    valor_centro /= 2
    score += valor_centro

    # Piezas amenazantes
    #for i in range(5):
    #    for j in range(5):
    #        if nodo.board[i][j].lower() == master.lower():
    return score

def traducir_caracter(caracter):
    if caracter.isdigit():
        return ord('5')-ord(caracter)
    else:
        return ord(caracter)-ord('A')

def traducir_accion_inversa(posiciones):
    accion = ""
    for pos in posiciones:
        cod_numero, cod_letra = pos
        
        letra = chr(cod_letra + ord('A')) # Convierte 0->'A', 1->'B', ...
        numero = chr(ord('5') - cod_numero) # Convierte 0->'5', 1->'4', ...

        accion += letra + numero

    return accion

def traducir_posicion(accion):
    pos_ini = [traducir_caracter(accion[1]), traducir_caracter(accion[0])]
    pos_fin = [traducir_caracter(accion[3]), traducir_caracter(accion[2])]

    return pos_ini, pos_fin

def swap(nodo, pos_inic, pos_fin):
    if nodo.board[pos_fin[0]][pos_fin[1]] != '-':
        nodo.board[pos_fin[0]][pos_fin[1]] = '-'
    
    aux = nodo.board[pos_inic[0]][pos_inic[1]]
    nodo.board[pos_inic[0]][pos_inic[1]] = nodo.board[pos_fin[0]][pos_fin[1]] 
    nodo.board[pos_fin[0]][pos_fin[1]] = aux
    
def jugar_carta(nodo, card_id):
    carta = nodo.cards[card_id]
    if carta:
        carta.owner = -1
        carta.dx_1 = -carta.dx_1
        carta.dy_1 = -carta.dy_1
        carta.dx_2 = -carta.dx_2
        carta.dy_2 = -carta.dy_2
        carta.dx_3 = -carta.dx_3
        carta.dy_3 = -carta.dy_3
        carta.dx_4 = -carta.dx_4
        carta.dy_4 = -carta.dy_4
        nodo.cards.update({card_id: carta})

    for key in nodo.cards:
        carta = nodo.cards[key]
        if carta.owner == -1:
            carta.owner = nodo.turno
            nodo.cards.update({key: carta})
            break

def generar_acciones_validas(nodo_param):
    acciones = []
    pieza = "W" if nodo_param.turno == 0 else "B"
    posiciones = []
    
    for i in range(len(nodo_param.board)): # por cada fila
        fila = "".join(nodo_param.board[i])
        pos_master = find(fila, pieza.upper())
        if pos_master:
            posiciones.append([i, pos_master[0]]) # Master, solo 1
        for j in find(fila, pieza.lower()):
            posiciones.append([i, j])
    
    for card in nodo_param.cards.values():
        if card.owner == nodo_param.turno:
            movimientos = [
                (card.dx_1, card.dy_1),
                (card.dx_2, card.dy_2),
                (card.dx_3, card.dy_3),
                (card.dx_4, card.dy_4)
            ]
            mov_validos = [m for m in movimientos if m != (0, 0)]
            for (dx, dy) in mov_validos:
                for pos in posiciones:
                    pos_fin = [pos[0] - dy, pos[1] + dx]
                    if es_posible(nodo_param, [card.owner, card.card_id, [pos, pos_fin]]):
                        acciones.append([nodo_param.turno, card.card_id, [pos, pos_fin]])
    return acciones

def aplica(accion, nodo_param):
    (pos_ini, pos_fin) = accion[2]
    
    nodoCopy = Nodo(
        nodo_param.board,
        nodo_param.cards,
        alternar_id(nodo_param.turno)
    )
    
    swap(nodoCopy, pos_ini, pos_fin) 
    
    jugar_carta(nodoCopy, accion[1])

    return nodoCopy

def es_posible(nodo_param, mov):
    _, _, (pos_ini, pos_fin) = mov
    pieza_turno = "w" if nodo_param.turno == 0 else "b"

    if not (0 <= pos_fin[0] <= 4 and 0 <= pos_fin[1] <= 4) or not (0 <= pos_ini[0] <= 4 and 0 <= pos_ini[1] <= 4):
        return False
    
    pieza_ini = nodo_param.board[pos_ini[0]][pos_ini[1]].lower()
    pieza_fin = nodo_param.board[pos_fin[0]][pos_fin[1]].lower()
    if (pieza_ini in ["-", "", " ", None]) or (pieza_ini != pieza_turno) or (pieza_ini == pieza_fin):
        return False

    return True

def es_final(nodo_param):
    iW, jW = encontrar_master(nodo_param, "W")
    iB, jB = encontrar_master(nodo_param, "B")
    return (iW, jW) == (-1, -1) or (iB, jB) == (-1, -1) or (iW, jW) == (0, 2) or (iB, jB) == (4, 2)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def alpha_beta(nodo_param, profundidad, alfa, beta, jugadorMAX):
    if profundidad == 0 or es_final(nodo_param):
        return eval(nodo_param), None

    acciones = generar_acciones_validas(nodo_param)

    print("NODO:", file=sys.stderr, flush=True)
    nodo_param.imprimir_estado()

    if jugadorMAX:
        value = -math.inf
        mejor_accion = None

        for accion in acciones:
            nuevo_nodo = aplica(accion, nodo_param)
            print("DSP:", file=sys.stderr, flush=True)
            nuevo_nodo.imprimir_estado()

            valor_nuevo_nodo, _ = alpha_beta(nuevo_nodo, profundidad, alfa, beta, False)

            if valor_nuevo_nodo > value:
                value = valor_nuevo_nodo
                mejor_accion = accion
                alfa = value
            if alfa >= beta:
                break
        return value, mejor_accion
    else:
        value = math.inf
        mejor_accion = None

        for accion in acciones:
            nuevo_nodo = aplica(accion, nodo_param)
            
            valor_nuevo_nodo, _ = alpha_beta(nuevo_nodo, profundidad-1, alfa, beta, True)

            if valor_nuevo_nodo < value:
                value = valor_nuevo_nodo
                mejor_accion = accion
                beta = value
            if alfa >= beta:
                break
        return value, mejor_accion
        
player_id = int(input()) # Jugador 0 cuando jugas contra BOSS

while True:
    # Tablero
    board = []
    for i in range(5):
        row = input()
        board.append(list(row))
    
    # 5 cards
    cards = {}
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        card = Tarjeta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        cards.update({card.card_id: card})

    # Acciones posibles
    action_count = int(input())

    for i in range(action_count):
        inputs = input().split()
    
    if action_count > 0:
        nodoActual = Nodo(board, cards, player_id)
        valor, accion = alpha_beta(nodoActual, 10, -math.inf, math.inf, True)

        if accion is not None:
            print(accion[1], traducir_accion_inversa(accion[2]))
        else:
            print("PASS")
    else:
        print("PASS")