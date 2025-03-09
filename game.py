import sys
import math
import copy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class tarjeta:
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

class nodo:
    def __init__(self, board, cards, turno):
        self.board = board
        self.cards = cards
        self.turno = turno
        self.acciones = self.generar_acciones_validas()

    def generar_acciones_validas(self):
        acciones = []
        pieza = "W" if self.turno == 0 else "B"
        posiciones = []
        
        for i in range(len(self.board)): # por cada fila
            fila = "".join(self.board[i])
            pos_master = find(fila, pieza.upper())
            if pos_master:
                posiciones.append([i, pos_master[0]]) # Master, solo 1
            for j in find(fila, pieza.lower()):
                posiciones.append([i, j])
        
        for card in self.cards:
            if card.owner == self.turno:
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
                        if es_posible(self, [card.owner, card.card_id, [pos, pos_fin]]):
                            acciones.append([self.turno, card.card_id, [pos, pos_fin]])
        return acciones
    
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

def swap(board, pos_inic, pos_fin):
    board_copy = board.copy()
    if board_copy[pos_fin[0]][pos_fin[1]] != '-':
        board_copy[pos_fin[0]][pos_fin[1]] = '-'
    
    aux = board_copy[pos_inic[0]][pos_inic[1]]
    board_copy[pos_inic[0]][pos_inic[1]] = board_copy[pos_fin[0]][pos_fin[1]] 
    board_copy[pos_fin[0]][pos_fin[1]] = aux
    return board_copy
    
def jugar_carta(cards, num_tarjeta, owner):
    new_cards = []
    for c in cards:
        if c.card_id == num_tarjeta:
            new_cards.append(tarjeta(
                -1,
                c.card_id,
                -c.dx_1, -c.dy_1,
                -c.dx_2, -c.dy_2,
                -c.dx_3, -c.dy_3,
                -c.dx_4, -c.dy_4
            ))
        elif c.owner == -1:
            new_cards.append(tarjeta(
                owner,
                c.card_id,
                c.dx_1, c.dy_1,
                c.dx_2, c.dy_2,
                c.dx_3, c.dy_3,
                c.dx_4, c.dy_4
            ))
        else:
            new_cards.append(tarjeta(
                c.owner,
                c.card_id,
                c.dx_1, c.dy_1,
                c.dx_2, c.dy_2,
                c.dx_3, c.dy_3,
                c.dx_4, c.dy_4
            ))
    return new_cards

def aplica(accion, nodo_param):
    (pos_ini, pos_fin) = accion[2]
    
    nn = nodo(
        swap(nodo_param.board, pos_ini, pos_fin), 
        jugar_carta(nodo_param.cards, accion[1], nodo_param.turno), 
        nodo_param.turno)

    return nn

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
    
    acciones = nodo_param.acciones

    if jugadorMAX:
        value = -math.inf
        mejor_accion = None

        for accion in acciones:
            nuevo_nodo = aplica(accion, nodo_param)

            valor_nuevo_nodo, _ = alpha_beta(nuevo_nodo, profundidad-1, alfa, beta, False)

            print("MAX: ", accion, " - ", valor_nuevo_nodo, file=sys.stderr, flush=True)

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
            print("MIN: ", accion, " - ", valor_nuevo_nodo, file=sys.stderr, flush=True)

            if valor_nuevo_nodo < value:
                value = valor_nuevo_nodo
                mejor_accion = accion
                beta = value
            if alfa >= beta:
                break
        return value, mejor_accion
        
def encontrar_owner(tarjetas, card_id):
    for card in tarjetas:
        if card.card_id == card_id:
            return card.owner


player_id = int(input()) # Jugador 0 cuando jugas contra BOSS


while True:
    # Tablero
    board = []
    for i in range(5):
        row = input()
        board.append(list(row))
    
    # 5 cards
    cards = []
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        card = tarjeta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        cards.append(card)

    # Acciones posibles
    acciones = []
    action_count = int(input())

    for i in range(action_count):
        inputs = input().split()
        card_id = int(inputs[0])
        move = inputs[1]
        pos_ini, pos_fin = traducir_posicion(move)
        acciones.append([player_id, card_id, [pos_ini, pos_fin]])

    if len(acciones) > 0:
        nodoActual = nodo(board, cards, player_id)
        if len(acciones) >= 8:
            valor, accion = alpha_beta(nodoActual, 2, -math.inf, math.inf, True)
        else:
            valor, accion = alpha_beta(nodoActual, 3, -math.inf, math.inf, True)

        if accion is not None:
            print(accion[1], traducir_accion_inversa(accion[2]))
        else:
            print("PASS")
    else:
        print("PASS")