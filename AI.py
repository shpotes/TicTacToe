__author__ = 'Andrea Posada' and 'Santiago Hincapie'

import random

posjuego = ['-','-','-','-','-','-','-','-','-']
poswin = ()

def posJuego(num, boolean):
    global posjuego
    if boolean: str="O"
    else: str="X"
    posjuego[num] = str

def isOver():
    win=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(2,4,6),(0,4,8)]
    if(len(posjuego)>4):
        posx = []
        poso = []
        for i in xrange (len(posjuego)):
            if posjuego[i]=='X': posx.append(i)
            elif posjuego[i]=='O': poso.append(i)
        for j in xrange (len(win)):
            if isInVal(win[j], posx) or isInVal(win[j], poso): return True
    return False

def isInVal(j, pos):
    global poswin
    count = 0
    for i in pos:
        if i==j[0] or i==j[1] or i==j[2]: count+=1
        if count==3:
            poswin = j
            return True
    return False

def freeSpace():
    global posjuego
    for i in posjuego:
        if i=='-': return True
    else: return False

########################################################################################################################
########################################################################################################################

INFINITY = 1000000
HUMAN = "X"
COMPUTER = "O"

def nextMove():
    return computer_move(posjuego)

def computer_move(b):
    '''
    Este metodo controla los movimientos del PC
    :param b: el tablero actual
    :return move, el movimiento que debe realizar el PC:
    '''
    maxDepth = 9
    cp = 2
    score, move = negamax(b, cp, maxDepth, 0)
    return move

def negamax(board, currentPlayer, maxDepth, currentDepth):
    '''
    Este es metodo contiene el algoritmo negamax
    :param board: Es el estado actual del tablero
    :param currentPlayer: El jugador de turno
    :param maxDepth: La profundidad maxima del arbol de recursion
    :param currentDepth: el nivel actual de recursion
    :return bestMove: El mejor movimiento posible
    :return bestScore: El puntaje del mejor movimiento
    '''
    if gameover(board) or currentDepth == maxDepth:
        return ev(board, currentPlayer), None
    bestMove = None
    bestScore = -INFINITY
    if currentPlayer == 2:
        otherPlayer = 1
    else:
        otherPlayer = 2
    for move in opMov(board):
        newBoard = mover(board, move, currentPlayer)
        recursedScore, currentMove = negamax(newBoard, otherPlayer, maxDepth, currentDepth + 1)
        currentScore = -recursedScore
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = move
    return bestScore, bestMove

def ev(board, cp):
    '''
    Este metodo realiza evaluaciones para el Negamax
    :param board: El tablero actual
    :param cp: El jugador actual
    :return: el puntaje del "nodo"
    '''
    winner = check_for_winner(board)
    if cp == 1:
        cpl = HUMAN
        opl = COMPUTER
    if cp == 2:
        cpl = COMPUTER
        opl = HUMAN
    if winner == cpl:
        return INFINITY
    elif winner == opl:
        return -INFINITY
    elif check_if_filled(board):
        return 0

def check_for_winner(b):
    '''
    Revisa si hay un ganador
    :param b: El tablero actual
    :return check: verdadero o falso dependiendo si hay un ganador o no
    '''
    if check_rows(b) != -1:
        return check_rows(b)
    if check_columns(b) != -1:
        return check_columns(b)
    if check_diagonals(b) != -1:
        return check_diagonals(b)

def check_if_filled(b):
    '''
    Este metodo revisa si hay empate
    :param b: El tablero actual
    :return: verdadero o falso dependiendo de si hay empate
    '''
    c = True
    for t in b:
        if t == "-":
            c = False
    return c

def check_diagonals(b):
    '''
    Revisa las diagonales para buscar si hay un ganador
    :param b: El tablero actual
    :return: verdadero o falso dependiendo de si alguien acertado las diagonales
    '''
    i = 0
    if b[i] != '-' and b[i] == b[i + 4] and b[i] == b[i + 8]:
        return b[i]
    i = i + 6
    if b[i] != '-' and b[i] == b[i - 2] and b[i] == b[i - 4]:
        return b[i]
    return -1

def check_rows(b):
    '''
    Revisa las filas para buscar si hay un ganador
    :param b: El tablero actual
    :return: verdadero o falso dependiendo de si alguien acertado las filas
    '''
    i = 0
    while i < 9:
        if b[i] != '-' and b[i] == b[i + 1] and b[i] == b[i + 2]:
            return b[i]
        i = i + 3
    return -1

def check_columns(b):
    '''
    Revisa las columnas para buscar si hay un ganador
    :param b El tablero actual:
    :return: verdadero o falso dependiendo de si alguien acertado las columnas
    '''
    if b[0] != '-' and b[0] == b[3] and b[0] == b[6]:
        return b[0]
    if b[1] != '-' and b[1] == b[4] and b[1] == b[7]:
        return b[1]
    if b[2] != '-' and b[2] == b[5] and b[2] == b[8]:
        return b[2]
    return -1

def opMov(brd):
    '''
    este metodo optiene los lugares "vacios"
    :param brd: el tablero actual
    :return move:
    '''
    moves = []
    for k in range(9):
        if brd[k] == '-':
            moves.append(k)
    random.shuffle(moves)
    return moves

def gameover(b):
    '''
    me dice si el juego a terminado
    :param b: el tablero actual
    :return: verdadero o falso dependiendo de si el juego a terminado o no
    '''
    if check_rows(b) != -1 or check_columns(b) != -1 or check_diagonals(b) != -1:
        return True
    if check_if_filled(b):
        return True
    return False

def mover(brd, move, cp):
    '''
    Este metodo realiza el moviemto
    :param brd: el tablero a modificar
    :param move: el movimiento a efectuar
    :param cp: el jugador actual
    :return b: el nuevo tablero
    '''
    b = []
    for l in range(9):
        b.append(brd[l])
    if cp == 1:
        b[move] = HUMAN
    else:
        b[move] = COMPUTER
    return b
