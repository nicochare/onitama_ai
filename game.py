import sys
import math
import copy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

player_id = int(input()) # Jugador 0 cuando jugas contra BOSS

class tarjeta:
    def __init__(self, owner, card_id, dx_1,dy_1, dx_2,dy_2, dx_3,dy_3, dx_4,dy_4):
        self.owner = owner
        self.card_id = card_id
        # self.coord1 = coord1
        # self.coord2 = coord2
        # self.coord3 = coord3
        # self.coord4 = coord4
        self.dx_1 = dx_1
        self.dy_1 = dy_1
        self.dx_2 = dx_2
        self.dy_2 = dy_2
        self.dx_3 = dx_3
        self.dy_3 = dy_3
        self.dx_4 = dx_4
        self.dy_4 = dy_4

class coordenada:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class nodo:
    def __init__(self, board, cards, acciones, turno):
        self.turno = turno
        self.board = board
        self.cards = cards
        self.acciones = acciones
    
    def imprimir_estado(self):
        print("Turno: ", self.turno, file=sys.stderr)
        for fila in board:
            print(fila, file=sys.stderr)

def alternarId(id):
    return 1-id

def distancia_manhattan(i, i2, j, j2):
    return abs(i-i2) + abs(j-j2)

def distancia_manhattan_shrine(i, j, player):
    (i2, j2) = (0, 2) if player == 0 else (4, 2)
    return abs(i-i2) + abs(j-j2)

def rival_mas_cercano_master(nodo, xm, ym):
    posiciones = []
    pieza = "B" if nodo.turno == 0 else "W"
    distancia = math.inf
    for i in range(len(nodo.board)): # por cada fila
        fila = "".join(nodo.board[i])
        posMaster = find(fila, pieza.upper())
        if len(posMaster) > 0:
            posiciones.append([i, posMaster[0]]) # Master, solo 1
            if distancia > distancia_manhattan(xm, i, ym, posMaster[0]):
                distancia = distancia_manhattan(xm, i, ym, posMaster[0])
        for j in find(fila, pieza.lower()):
            posiciones.append([i, j])
            if distancia > distancia_manhattan(xm, i, j, ym):
                distancia = distancia_manhattan(xm, i, j, ym)
    return distancia


def eval(nodo):
    heur = 0
    masterMio = "W" if nodo.turno == 0 else "B"
    masterRival = "B" if nodo.turno == 0 else "W"

    xm, ym = encontrarMaster(nodo, masterMio)
    xr, yr = encontrarMaster(nodo, masterRival)
    centro = [(2,2), (2,1), (2,3)]
    shrine_propio = (0,2) if nodo.turno == 1 else (4,2)
    shrine_rival = (4,2) if nodo.turno == 1 else (0,2)
    
    if (xm, ym) == shrine_rival:
        return math.inf
    if (xr, yr) == shrine_propio:
        return -math.inf
    
    # Distancia shrine
    dm_m = distancia_manhattan_shrine(xm, ym, nodo.turno)
    dm_r = distancia_manhattan_shrine(xr, yr, alternarId(nodo.turno))
    valor_distancia = dm_m - dm_r


    # Control centro
    valorCentro = 0
    for i, j in centro:
        if nodo.board[i][j] == masterMio.lower():
            valorCentro += 1.5
        elif nodo.board[i][j] == masterRival.lower():
            valorCentro -= 1.5
    
    heur += valorCentro

    peso_vivas = 0.55
    vivasMias = 0
    vivasRival = 0

    for i in range(5):
        vivasMias += ''.join(nodo.board[i]).count(masterMio.lower())
        vivasRival += ''.join(nodo.board[i]).count(masterRival.lower())
    valor_vivas = vivasMias-vivasRival

    if nodo.turno == 0 and vivasRival > 3 and xm < 3:
        heur -= 0.5
    if nodo.turno == 1 and vivasRival > 3 and xm > 1:
        heur -= 2

    peso_distancia = 0.25 + (4 - (vivasMias + vivasRival)) * 0.1
    
    if rival_mas_cercano_master(nodo, xm, ym) == 3:
        heur -= 2
    elif rival_mas_cercano_master(nodo, xm, ym) < 3:
        heur -= 3

    heur += valor_vivas*peso_vivas
    heur += valor_distancia*peso_distancia
    return heur

def traducirCaracter(caracter):
    if caracter.isdigit():
        return ord('5')-ord(caracter)
    else:
        return ord(caracter)-ord('A')

def traducirCaracterInversa(posiciones):
    stringFinal = ""
    for pos in posiciones:
        codNumero, codLetra = pos
        
        letra = chr(codLetra + ord('A')) # Convierte 0->'A', 1->'B', ...
        numero = chr(ord('5') - codNumero) # Convierte 0->'5', 1->'4', ...

        stringFinal += letra + numero

    return stringFinal

def traducirPosicion(accion):
    posIni = [traducirCaracter(accion[1]), traducirCaracter(accion[0])]
    posFin = [traducirCaracter(accion[3]), traducirCaracter(accion[2])]

    return posIni, posFin

def swap(board, posInic, posFin):
    aux = board[posInic[0]][posInic[1]]
    board[posInic[0]][posInic[1]] = board[posFin[0]][posFin[1]] 
    board[posFin[0]][posFin[1]] = aux
    return board
    
def traducirAccionATarjeta(accionIni, accionFin):
    return accionFin[0]-accionIni[0], accionFin[1]-accionIni[1]

def jugarCarta(cards, num_tarjeta):
    cardsCopy = [copy.deepcopy(c) for c in cards]
    i = next(i for i, c in enumerate(cardsCopy) if c.card_id == num_tarjeta)
    j = next(j for j, c in enumerate(cardsCopy) if c.owner == -1)

    aux = cardsCopy[i].owner
    cardsCopy[i].owner = -1
    cardsCopy[j].owner = aux

    cardsCopy[i].dx_1, cardsCopy[i].dy_1 = -cardsCopy[i].dx_1, -cardsCopy[i].dy_1
    cardsCopy[i].dx_2, cardsCopy[i].dy_2 = -cardsCopy[i].dx_2, -cardsCopy[i].dy_2
    cardsCopy[i].dx_3, cardsCopy[i].dy_3 = -cardsCopy[i].dx_3, -cardsCopy[i].dy_3
    cardsCopy[i].dx_4, cardsCopy[i].dy_4 = -cardsCopy[i].dx_4, -cardsCopy[i].dy_4
    return cardsCopy

def realizarAccion(nodo, accion):
    nodoCopy = copy.deepcopy(nodo)
    posIni, posFin = accion[2]
    
    if nodoCopy.board[posFin[0]][posFin[1]] != '-':
        nodoCopy.board[posFin[0]][posFin[1]] = '-'
    
    nodoCopy.board = swap(nodoCopy.board, posIni, posFin)
    
    nodoCopy.cards = jugarCarta(nodoCopy.cards, accion[1])

    nodoCopy.turno = alternarId(nodoCopy.turno)

    return nodoCopy

def evaluarPuntuacionAccion(nodo, accion):
    nodoCopy = realizarAccion(nodo, accion)
    return eval(nodoCopy)

def transformarTablero(board):
    for i in range(len(board)):
        board[i] = list(board[i])

def encontrarMaster(nodo, masterCaracter):
    for i in range(len(nodo.board)):
        for j in range(len(nodo.board)):
            if nodo.board[i][j] == masterCaracter:
                return i, j
    return -1, -1

def posValida(pos):
    return 0 <= pos[0] <= 4 and 0 <= pos[1] <= 4

def esPosible(nodo, mov):
    posIni, posFin = mov[2]
    piezaTurno = "w" if nodo.turno == 0 else "b"

    if not posValida(posIni) or not posValida(posFin):
        return False
    
    piezaIni = nodo.board[posIni[0]][posIni[1]].lower()
    piezaFin = nodo.board[posFin[0]][posFin[1]].lower()
    if piezaIni in ["-", "", " "] or piezaIni != piezaTurno:
        return False
    if piezaIni == piezaFin:
        return False
    return True

def esFinal(nodo):
    iW, jW = encontrarMaster(nodo, "W")
    iB, jB = encontrarMaster(nodo, "B")
    return (iW, jW) == (-1, -1) or (iB, jB) == (-1, -1) or (iW, jW) == (0, 2) or (iB, jB) == (4, 2)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def devAccionesJugActual(nodo):
    posiciones = []
    pieza = "W" if nodo.turno == 0 else "B"

    for i in range(len(nodo.board)): # por cada fila
        fila = "".join(nodo.board[i])
        posMaster = find(fila, pieza.upper())
        if len(posMaster) > 0:
            posiciones.append([i, posMaster[0]]) # Master, solo 1
        for j in find(fila, pieza.lower()):
            posiciones.append([i, j])
    
    # Owner card 0 = "W w"
    # Owner card 1 = "B b"
    # Owner card -1 = middle
    
    accionesTotales = []
    for card in nodo.cards:
        if card.owner == nodo.turno:
            movimientos = [
                (card.dx_1, card.dy_1),
                (card.dx_2, card.dy_2),
                (card.dx_3, card.dy_3),
                (card.dx_4, card.dy_4)
            ]
            mov_validos = {m for m in movimientos if m != (0, 0)}
            for dx, dy in mov_validos:
                #print(f"Carta {card.card_id} - dx: {dx}, dy: {dy}", file=sys.stderr)
                for pos in posiciones:
                    accionesTotales.append([
                        card.owner,
                        card.card_id,
                        [   
                            pos,   # posIni
                            [pos[0] - dy, pos[1] + dx] # posFin
                        ]
                    ])
    return accionesTotales # Formato [cardOwner, card_id, [posIni, posFin]]

def encontrarAccionesPosibles(nodo):
    acciones = []
    for ac in devAccionesJugActual(nodo):
        if esPosible(nodo, ac):
            acciones.append(ac)
    return acciones

def alpha_beta(nodo, profundidad, alfa, beta, jugadorMAX):
    if profundidad == 0 or esFinal(nodo):
        return eval(nodo), None
    
    if jugadorMAX:
        value = -math.inf
        mejor_accion = None

        for accion in encontrarAccionesPosibles(nodo):
            nuevoNodo = realizarAccion(nodo, accion)
            valNuevoNodo, _ = alpha_beta(nuevoNodo, profundidad-1, alfa, beta, False)
            if valNuevoNodo > value:
                value = valNuevoNodo
                mejor_accion = accion
            alfa = max(alfa, value)
            if alfa >= beta:
                break
        return value, mejor_accion
    else:
        value = math.inf
        mejor_accion = None

        for accion in encontrarAccionesPosibles(nodo):
            nuevoNodo = realizarAccion(nodo, accion)
            valNuevoNodo, _ = alpha_beta(nuevoNodo, profundidad-1, alfa, beta, True)
            if valNuevoNodo < value:
                value = valNuevoNodo
                mejor_accion = accion
            beta = min(beta, value)
            if alfa >= beta:
                break
        return value, mejor_accion
        
def encontrarOwner(tarjetas, card_id):
    for card in tarjetas:
        if card.card_id == card_id:
            return card.owner

print("Soy jugador: ", player_id,  file=sys.stderr, flush=True)

while True:
    # Tablero
    board = []
    for i in range(5):
        row = input()
        board.append(row)
    
    transformarTablero(board)

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
        posIni, posFin = traducirPosicion(move)
        acciones.append([player_id, card_id, [posIni, posFin]])

    if len(acciones) > 0:
        nodoActual = nodo(board, cards, acciones, player_id)
        valor, maxAccion = alpha_beta(nodoActual, 2, -math.inf, math.inf, True)

        if maxAccion is not None:
            print(valor, file=sys.stderr, flush=True)
            print(maxAccion,  file=sys.stderr, flush=True)
            print(maxAccion[1], traducirCaracterInversa(maxAccion[2]))
        else:
            print("PASS")
    else:
        print("PASS")