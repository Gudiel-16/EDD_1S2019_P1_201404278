import curses
import time
import csv
import random
import os


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

""" ----------------------------------------------LISTA DOBLE PARA SNAKE ----------------------------------------------"""
class nodoDobleSnake():

    def __init__(self, coordenadas):                  
        self.siguiente = None        
        self.anterior =  None
        self.coordenadas = coordenadas 

class dobleSnake():
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.size=-1

    def estaVacia(self):
        return self.primero is None
    
    def insertarInicio(self, coordenadas):
        nuevo=nodoDobleSnake(coordenadas)
        if self.estaVacia():
            self.primero=nuevo
            self.ultimo=nuevo
        else:
            nuevo.siguiente=self.primero
            self.primero.anterior=nuevo
            self.primero=nuevo

        self.size=self.size+1

    def insertarFinal(self,coordenadas):
        nuevo=nodoDobleSnake(coordenadas)
        if self.estaVacia():
            self.primero=nuevo
            self.ultimo=nuevo
        else:
            self.ultimo.siguiente=nuevo
            nuevo.anterior=self.ultimo
            self.ultimo=nuevo
            
        self.size=self.size+1

    def imprimirLista(self):
    
        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size+1):
                print(temp.coordenadas,end=" ")
                temp=temp.siguiente

listaDobleCircularUsuarios=dobleCircularUsuarios() #objeto como variable global
listaDobleSnake=dobleSnake()  

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
                jugar()
            elif indice_fila_actual==2:
                curses.wrapper(menu_usuarios)
            elif indice_fila_actual==4:
                cargaMasiva()
            elif indice_fila_actual==len(menu)-1:
                break
        
        print_menu(stdscr,indice_fila_actual)
        stdscr.refresh()


""" ----------------------------------------------PARA LA COMIDA Y  ----------------------------------------------"""
def crear_comida(snake):
    comidaa=None

    while comidaa is None:
        comidaa=[random.randint(3, 19),random.randint(3,75)]
        if comidaa in snake:
            comidaa=None
    return comidaa


""" ----------------------------------------------JUGAR ----------------------------------------------"""
def jugar():
    stdscr=curses.initscr()
    sh, sw=stdscr.getmaxyx()
    pos_Y=0
    pos_X=0
    window=curses.newwin(sh,sw,pos_Y,pos_X)
    window.keypad(True)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)
    window.nodelay(True)

    key=KEY_RIGHT
    
    snake=[[7, 8],[7, 7],[7, 6]]#tamanio snake

    for y,x in snake:
        window.addch(y,x,'@')
    
    comida=crear_comida(snake)
    window.addch(comida[0], comida[1], '+')

    comidapop=crear_comida(snake)
    window.addch(comidapop[0], comidapop[1], '*') 
    
    

    while key!=27:
        window.timeout(120)
        keystroke= window.getch()

        cabeza=snake[0]

        if keystroke is not -1:
            key=keystroke                
       
        if key==KEY_RIGHT:
            #pos_X=pos_X es como poner pausa
            nuevaCabeza=[cabeza[0], cabeza[1]+1]
        elif key==KEY_LEFT:
            nuevaCabeza=[cabeza[0], cabeza[1]-1]
        elif key==KEY_UP:
            nuevaCabeza=[cabeza[0]-1, cabeza[1]]
        elif key==KEY_DOWN:
            nuevaCabeza=[cabeza[0]+1, cabeza[1]]

        snake.insert(0,nuevaCabeza)
        window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')

        if snake[0] ==comida:
            comida=crear_comida(snake)
            window.addch(comida[0], comida[1], '+')
            
        elif snake[0] ==comidapop:
            comidapop=crear_comida(snake)
            window.addch(comidapop[0], comidapop[1], '*')
            aa=[snake.pop()] #captura coordenadas del pop()            
            for x,y in aa:
                window.addch(x, y, ' ') #pinta nada en las coordenadas del pop()
            bb=[snake.pop()]
            for x,y in bb:
                window.addch(x, y, ' ')    
            #score+=1
            #print_score(stdscr,score)
        else:
            window.addch(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
          
        
        indiceIzquierdo=[[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1],[21,1],[22,1],[23,1]]
        indiceDerecho=[[1,78],[2,78],[3,78],[4,78],[5,78],[6,78],[7,78],[8,78],[9,78],[10,78],[11,78],[12,78],[13,78],[14,78],[15,78],[16,78],[17,78],[18,78],[19,78],[20,78],[21,78],[22,78],[23,78]]
        indiceSuperior=[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29],[1,30],[1,31],[1,32],[1,33],[1,34],[1,35],[1,36],[1,37],[1,38],[1,39],[1,40],[1,41],[1,42],[1,43],[1,44],[1,45],[1,46],[1,47],[1,48],[1,49],[1,50],[1,51],[1,52],[1,53],[1,54],[1,55],[1,56],[1,57],[1,58],[1,59],[1,60],[1,61],[1,62],[1,63],[1,64],[1,65],[1,66],[1,67],[1,68],[1,69],[1,70],[1,71],[1,72],[1,73],[1,74],[1,75],[1,76],[1,77]]
        indiceInferior=[[23,2],[23,3],[23,4],[23,5],[23,6],[23,7],[23,8],[23,9],[23,10],[23,11],[23,12],[23,13],[23,14],[23,15],[23,16],[23,17],[23,18],[23,19],[23,20],[23,21],[23,22],[23,23],[23,24],[23,25],[23,26],[23,27],[23,28],[23,29],[23,30],[23,31],[23,32],[23,33],[23,34],[23,35],[23,36],[23,37],[23,38],[23,39],[23,40],[23,41],[23,42],[23,43],[23,44],[23,45],[23,46],[23,47],[23,48],[23,49],[23,50],[23,51],[23,52],[23,53],[23,54],[23,55],[23,56],[23,57],[23,58],[23,59],[23,60],[23,61],[23,62],[23,63],[23,64],[23,65],[23,66],[23,67],[23,68],[23,69],[23,70],[23,71],[23,72],[23,73],[23,74],[23,75],[23,76],[23,77]]
        
        if (snake[0] in indiceIzquierdo[0:]):  
            nuevaCabeza=[cabeza[0], cabeza[1]+76]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
        elif (snake[0] in indiceDerecho[0:]): 
            nuevaCabeza=[cabeza[0], cabeza[1]-76]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
        elif (snake[0] in indiceSuperior[0:]):
            nuevaCabeza=[cabeza[0]+21, cabeza[1]]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
        elif (snake[0] in indiceInferior[0:]):
            nuevaCabeza=[cabeza[0]-21, cabeza[1]]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
        elif (snake[0] in snake[1:]): 
            for y,x in snake[1:]:
                coord=str(x) + "," + str(y)
                print(y,x)
                listaDobleSnake.insertarFinal(coord)
            msg="HAS PERDIDO VUELVE A INTENTARLO!"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break


        window.refresh()

    curses.endwin()

'''    
def crear_comida(snake, box):
    comida=None

    while comida is None:
        comida=[random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]
        if comida in snake:
            comida=None
    return comida
''' 

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
    
    snake=[[sh//2, sw//2+1],[sh//2, sw//2],[sh//2, sw//2-1]]#tmanio snake
    direccion=curses.KEY_RIGHT

    for y,x in snake:
        stdscr.addstr(y,x,'@')

    comida=crear_comida(snake, box)
    stdscr.addstr(comida[0], comida[1], '*')

    score=0
    print_score(stdscr, score)


    while 1:
        key= stdscr.getch()

        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direccion=key

        cabeza=snake[0]#cabeza posicion

        if direccion==curses.KEY_RIGHT:
            nuevaCabeza=[cabeza[0], cabeza[1]+1]
        elif direccion == curses.KEY_LEFT:
            nuevaCabeza=[cabeza[0], cabeza[1]-1]
        elif direccion == curses.KEY_UP:
            nuevaCabeza=[cabeza[0]-1, cabeza[1]]
        elif direccion == curses.KEY_DOWN:
            nuevaCabeza=[cabeza[0]+1, cabeza[1]]
        snake.insert(0,nuevaCabeza)
        stdscr.addstr(nuevaCabeza[0], nuevaCabeza[1],'@')
        
        if snake[0] ==comida:
            comida=crear_comida(snake, box)
            stdscr.addstr(comida[0], comida[1], '*')
            score+=1
            print_score(stdscr,score)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()


        if (snake[0][0] in [box[0][0]+1, box[1][0]-1]):
            nuevaCabeza=[cabeza[0], cabeza[1]-1]
            #snake.insert(0,nuevaCabeza)
            stdscr.addstr(nuevaCabeza[0], nuevaCabeza[1],'@')

        elif(snake[0][1] in [box[0][1], box[1][1]]):
            comida=crear_comida(snake, box)
            stdscr.addstr(comida[0], comida[1], 'k') 

        elif (snake[0] in snake[1:]):    
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

""" ----------------------------------------------GRAFICAR SNAKE -----------------------------------------------------"""    
def graficarSnake():
    # open(nombre_archivo.ext, formato)
    f = open("otro2.dot", "w") 
    # write("texto a escribir") 
    f.write("digraph G {\n")
    f.write("node [shape = square];\n")
    f.write("A") # SU ESTRUCTURA!!!!, PILA, COLA, LISTA_DOBLE, CIRCULAR
    
    snake=[[2, 8],[2, 7],[2, 6]]#tmanio snake    
    for y,x in snake:
        coord=str(x) + "," + str(y)
        print(coord)

    f.write("}")
    # CIERRA EL ARCHIVO
    f.close()
    # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
    os.system("dot -Tjpg"+ " otro2.dot " +"-o imagen2.jpg")
    os.system("imagen2.jpg")

def aa():
    aa=""
    for i in range(77):
        aja="["+str(23)+","+str(i)+"],"
        aa+=aja
    print(aa)

#aa()
#graficarSnake()
jugar()
#curses.wrapper(jugar2)
#curses.wrapper(menu_principal)





#curses.wrapper(main)