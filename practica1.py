import curses
import time
import csv
import random


from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, textpad

menu=['Jugar','Puntuaciones','Usuarios','Reportes','Carga Masica',"Salir"]
nombreDeJugadorQueJugara=""

""" ----------------------------------------------LISTA DOBLE CIRCULAR PARA USUARIOS ----------------------------------------------"""
class nodoDobleUsuarios():

    def __init__(self,nombre):
        self.siguiente=None
        self.anterior=None
        self.nombre=nombre

class dobleCircularUsuarios():
    
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.size=0
    
    def estaVacia(self):
        return self.size==0
    
    def insertarFinal(self, nombre):
        nuevo=nodoDobleUsuarios(nombre)
        if (self.estaVacia()):
            self.primero=nuevo
            self.ultimo=nuevo
            self.primero.anterior=self.ultimo
            self.ultimo.siguiente=self.primero
        else:
            self.ultimo.siguiente=nuevo
            nuevo.anterior=self.ultimo
            self.ultimo=nuevo
            self.ultimo.siguiente=self.primero
            self.primero.anterior=self.ultimo
        self.size=self.size+1
    
    def impresion(self):
        temp=self.primero
        for i in range(self.size):
            print(temp.nombre,end=" ")
            temp=temp.siguiente
    
    def tamanio(self):
        return self.size

    def obtenerNombre(self, index):
        actual=self.primero
        for i in range(index):
            actual=actual.siguiente
        return actual.nombre
            

listaDobleCircularUsuarios=dobleCircularUsuarios() #objeto como variable global  

""" ----------------------------------------------PARA EL MENU PRINCIPAL ----------------------------------------------"""
def print_menu(stdscr, selected_row_idx):
    h, w= stdscr.getmaxyx()
        
    for idx, row in enumerate(menu):
        x=w//2 - len(row)//2
        y=h//2 -len(menu) + idx
        if idx==selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)


    stdscr.refresh()

def menu_principal(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    indice_fila_actual=0

    print_menu(stdscr,indice_fila_actual)
    
    while 1:
        key=stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and indice_fila_actual>0:
            indice_fila_actual-=1
        elif key == curses.KEY_DOWN and indice_fila_actual<len(menu)-1:
            indice_fila_actual+=1
        elif key==curses.KEY_ENTER or key in [10,13]:
            stdscr.addstr(0,0,"presionaste {}".format(menu[indice_fila_actual]))
            stdscr.refresh()
            stdscr.getch()
            if indice_fila_actual==0:
                curses.wrapper(jugar2)
            elif indice_fila_actual==2:
                curses.wrapper(menu_usuarios)
            elif indice_fila_actual==4:
                cargaMasiva()
            elif indice_fila_actual==len(menu)-1:
                break
        
        print_menu(stdscr,indice_fila_actual)
        stdscr.refresh()

""" ----------------------------------------------JUGAR ----------------------------------------------"""

def jugar():
    stdscr=curses.initscr()
    height=20
    width=40
    pos_Y=0
    pos_X=0
    window=curses.newwin(height,width,pos_Y,pos_X)
    window.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
    window.nodelay(True)

    key=KEY_RIGHT
    pos_X=5
    pos_Y=5
    window.addch(pos_Y,pos_X,'*')
    
    while key!=27:
        window.timeout(100)
        keystroke= window.getch()
        
        if keystroke is not -1:
            key=keystroke
                
        window.addch(pos_Y,pos_X,' ')

        if pos_X is 1:
            pos_X=39
            window.border(0)
        elif pos_X is 39:
            pos_X=1
            window.border(0)
        
        if pos_Y is 0:
            pos_Y=19
        elif pos_Y is 19:
            pos_Y=0

        if key==KEY_RIGHT:
            #pos_X=pos_X es como poner pausa
            pos_X=pos_X+1
        elif key==KEY_LEFT:
            pos_X=pos_X-1
        elif key==KEY_UP:
            pos_Y=pos_Y-1
        elif key==KEY_DOWN:
            pos_Y=pos_Y+1
        window.addch(pos_Y,pos_X,'*')

    curses.endwin()

def create_food(snake, box):
    food=None

    while food is None:
        food=[random.randint(box[0][0]+1, box[1][0]-1),
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food=None
    return food

def print_score(stdscr, score):
    sh,sw=stdscr.getmaxyx()
    scoreText="Score: {}".format(score)
    stdscr.addstr(0,sw//2-len(scoreText)//2,scoreText)
    stdscr.refresh()


def jugar2(stdscr):
    curses.curs_set(0)
    stdscr.border(0)
    stdscr.nodelay(1)
    stdscr.timeout(75)

    sh, sw=stdscr.getmaxyx()
    box =[[3,3],[sh-3,sw-3]]
    textpad.rectangle=(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    
    snake=[[sh//2, sw//2+1],[sh//2, sw//2],[sh//2, sw//2-1]]
    direccion=curses.KEY_RIGHT

    for y,x in snake:
        stdscr.addstr(y,x,'@')

    food=create_food(snake, box)
    stdscr.addstr(food[0], food[1], '*')

    score=0
    print_score(stdscr, score)


    while 1:
        key= stdscr.getch()

        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direccion=key

        head=snake[0]

        if direccion==curses.KEY_RIGHT:
            newHead=[head[0], head[1]+1]
        elif direccion == curses.KEY_LEFT:
            newHead=[head[0], head[1]-1]
        elif direccion == curses.KEY_UP:
            newHead=[head[0]-1, head[1]]
        elif direccion == curses.KEY_DOWN:
            newHead=[head[0]+1, head[1]]
        snake.insert(0,newHead)
        stdscr.addstr(newHead[0], newHead[1],'@')
        
        if snake[0] ==food:
            food=create_food(snake, box)
            stdscr.addstr(food[0], food[1], '*')
            score+=1
            print_score(stdscr,score)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()


        if (snake[0][0] in [box[0][0], box[1][0]] or 
            snake[0][1] in [box[0][1], box[1][1]] or 
            snake[0] in snake[1:]):
            msg="GAME OVER"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break

        stdscr.refresh()

        

""" ----------------------------------------------CARGA MASIVA ----------------------------------------------"""

def cargaMasiva(): 
        
    with open('C:\\Users\\GUDIEL\\Desktop\\cargaMasiva1.csv') as f:
        ingresarCabecera=0 #para no ingresar cabecera
        reader=csv.reader(f)
        for row in reader:
            if ingresarCabecera!=0:#no ingresa el primer elemento (cabecera)
                us="{0}".format(row[0])
                listaDobleCircularUsuarios.insertarFinal(us)
            ingresarCabecera=ingresarCabecera+1

""" ----------------------------------------------PARA MOSTRAR USUARIOS ----------------------------------------------"""
def menu_usuarios(stdscr): #INICIA LAS PROPIEDADES BASICAS
    curses.curs_set(0) # SETEA EL CURSOR EN LA POSICION 0
    index = 0
    pintar_menu(stdscr, 0) # VA A INICAR EN EL INDICE 0
    while True:
        tecla = stdscr.getch() # OBTENEMOS EL CARACTER DEL TECLADO
        if(tecla == curses.KEY_RIGHT): # VERIFICAMOS SI EL FLECHA A LA DERECHA
            index = index + 1
        elif (tecla == curses.KEY_LEFT ): # VERIFICAMOS SI ES FLECHA A LA IZQUIERDA
            index = index - 1
        elif (tecla == 27): # SI ES LA TECLA DE SCAPE....            
            curses.wrapper(menu_principal)
        elif (tecla==curses.KEY_ENTER):
            nombreDeJugadorQueJugara=listaDobleCircularUsuarios.obtenerNombre(index)
            curses.wrapper(menu_principal)
        if( index < 0): # EN CASO DE QUE EL INDICE SE VUELVA NEGAVITO LO DEJAMOS EN 0
            index = listaDobleCircularUsuarios.tamanio()-1
        if( index >= listaDobleCircularUsuarios.tamanio()): # EN CASO QUE EL INDICE SE VUELVA MAYOR AL SIZE DEL ARREGLO...
            index = 0 # ... LO LIMITAMOS AL ULTIMO INDICE VALIDO
        pintar_menu(stdscr, index) # MANDAMOS A REPINTAR LA PANTALLA

def pinter_ventana(stdscr):
    # -----------------------------------------------------------
    # PINTAMOS EL MARCO DEL MENU
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED) # COLOR DEL MARCO
    stdscr.attron(curses.color_pair(1)) # PERMITE HABILITAR UN ATRIBUTO ESPECIFICO
    stdscr.box("#", "$") ## PINTA EL MARCO
    stdscr.attroff(curses.color_pair(1)) # DESHABILITA EL ATRIBUTO ESPECIICO
    stdscr.refresh()
    # -----------------------------------------------------------

def pintar_menu(stdsrc, index):
    # -----------------------------------------------------------
    stdsrc.clear() # LIMPIA LA CONSOLA
    pinter_ventana(stdsrc) # MANDA A PINTAR EL MARCO
    altura, ancho = stdsrc.getmaxyx() # OBTIENE LA ALTURA Y ANCHO DE LA PANTALLA
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # COLOR DE LAS OPCIONES, INIICIALIZA UNA PAREJA DE COLORES EL COLOR DE LETRA Y COLOR DE FONDO RESPECTIVAMENTE
    y = int(altura/2) 
    x = int((ancho/2)-(len(listaDobleCircularUsuarios.obtenerNombre(index))/2))
    stdsrc.addstr(y,x, listaDobleCircularUsuarios.obtenerNombre(index), curses.color_pair(2)) # HAGREGA UNA CADENA  LA PANTALLA EN COORDENADAS Y, X Y UN ATRIBUTO EN ESTE CASO ES LA PAREJA DE COLORES
    stdsrc.refresh()
    # -----------------------------------------------------------


curses.wrapper(menu_principal)





#curses.wrapper(main)