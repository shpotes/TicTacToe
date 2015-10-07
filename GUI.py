__author__ = 'Andrea Posada' and 'Santiago Hincapie'

from Tkinter import *
import ttk
import tkMessageBox

import AI

'''
Atributos para los metodos de la GUI
a representa los dos signos con que se juega.
count es para saber el indice de a en que se esta.
buttonList es una lista con todos los botones del tablero.
first hace referencia a si empieza el computador.
'''

a = ["X","O"]
count = 0
buttonList = []
first = False

def start():
    '''
    Se encarga de incicializar el tablero para una nuevo juego y desactivar las elecciones. 
    Ademas realiza la primera jugada si el usuario desea jugar de segundo en turno.
    '''
    global count
    global first
    for child in board.winfo_children():
        child.configure(state=ACTIVE)
    for child in rbframe.winfo_children():
        child.configure(state=DISABLED)
    info.config(text="Jugando!")
    if str(var.get())=='O':
        first = True
        press(4)

def end():
    '''
    Limpia el tablero e inicia una nueva partida (los atributos vuelven a su estado natural).
    '''
    global count
    global first
    count = 0
    first = False
    AI.posjuego = ['-','-','-','-','-','-','-','-','-']
    AI.poswin = ()
    for child in rbframe.winfo_children():
        child.configure(state="press")
    for child in board.winfo_children():
        child.configure(text="", state=DISABLED, style='TButton')
    info.config(text="Seleccione la X, a su derecha, para comenzar partida")

def press(num):
    '''
    Comando de los botones. Desactiva las posiciones del tablero donde se presento el movimiento.
    :param num: referencia a la posicion del tablero donde se presenta el movimiento.
    :type num: integer
    '''
    global a
    global count
    global first
    button = buttonList[num]
    button.config(text=str(a[count%2]), state=DISABLED)
    AI.posJuego(num, first)
    count+=1
    if first==False and not AI.isOver() and AI.freeSpace():
        first = True
        press(AI.nextMove())
    elif not AI.freeSpace() or AI.isOver():
        colorButton(AI.poswin)
        info.config(text= "Fin Partida! Juego para "+a[(count-1)%2])
        tkMessageBox.showinfo("FIN PARTIDA", message(first, AI.isOver()))
        end()
    else: first = False



def message(boolean1, boolean2):
    '''
    Determina el mensaje para el tkMessageBox
    :param boolean1: referencia al juegador que se encuentra jugando
    :type boolean1: boolean
    :param boolean2: referencia a si el juego a terminado
    :type boolean2: boolean
    '''
    if boolean1 and boolean2: return "Lo sentimos!!! Ha perdido"
    elif not boolean2: return "Empate!!!"
    return "Felicitaciones!!! Ha ganado"

def colorButton(cells):
    '''
    Determina el color de las posiciones donde se ha ganado
    :param cells: posiciones donde se ha ganado
    :type cells: tuple
    '''
    global first
    global buttonList
    if first: COLOR = "red"
    else: COLOR = "yellow"
    if len(cells)!=0:
        for i in cells:
            style = ttk.Style()
            style.configure("Win.TButton", relief="raised", background=COLOR)
            buttonList[i].config(style="Win.TButton")

'''
Aca se crea la ventana, se agrega el LayOutManager (Grid) y a\~naden los widgets.
'''
root = Tk()
root.title("TRIQUI")

mainframe = ttk.Frame(root, padding="10")

board = ttk.Frame(mainframe)
'''
Los botones que se crearan a continuacion representan las p(i) del tablero donde i=0,1,...,8
'''
for i in xrange(9):
    button = ttk.Button(board)
    button.config(command=lambda num=i: press(num))
    button.grid(column=i%3, row=i//3, ipadx=20, ipady=20)
    buttonList.append(button)

rbframe = ttk.Frame(mainframe)
var = StringVar()
rb1 = ttk.Radiobutton(rbframe, text='X', variable=var, value='X', command=start).grid(row=0)
rb2 = ttk.Radiobutton(rbframe, text='O', variable=var, value='O', command=start).grid(row=1)

info = ttk.Label(mainframe, text="Seleccione la X, a su derecha, para comenzar partida")

info.grid(row=1, column=0, sticky="S")
board.grid(row=0, column=0)
rbframe.grid(row=0, column=1)

for child in board.winfo_children():
    child.configure(state=DISABLED)

mainframe.grid()

root.mainloop()
