import curses
import time
import csv
import random
import os
import sys

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, textpad

menu=['Jugar','Puntuaciones','Usuarios','Reportes','Carga Masica',"Salir"]
menuPausa=['Continuar','Puntuaciones','Usuarios','Reportes','Carga Masica',"Menu Principal"]
nombreUsuarioActual=["vacio"]
Puntuaciones=[]
banderaGuardarPunteoPausa=["vacio","vacio"]

""" -----------------------------------------------LISTA DOBLE CIRCULAR PARA USUARIOS ------------------------------------------------------------"""
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
    
    def reporte(self):
        contador=1  
        contador2=1      
        cadena="" 
        cadena2=""     
        temp=self.primero
        if self.size==1:
            cadena+='node0[label = "{ <a> |'+ self.primero.nombre +'| <s> }"];'
            cadena+='node0:s -> node0:a[color=red];'
            cadena+='node0:a -> node0:s[color=blue];'
        else:
            for i in range(self.size):#ssssssssssssssss size
                cadenaNodo='node'+str(contador)+'[label = "{ |'+str(temp.nombre)+' | }  "];\n'
                cadena+=cadenaNodo
                contador=contador+1
                temp=temp.siguiente

            for j in range(self.size):#ddddddddddddddddd size
                if contador2==1:
                    #cadena2+='node'+str(contador2)+':a -> nullInicio; \n'
                    sig=contador2+1
                    cadena2+='node'+str(contador2)+' -> node'+str(sig)+';\n'
                elif contador2==self.size:
                    ant=contador2-1
                    cadena2+='node'+str(contador2)+' -> node1[color=red]' + ';\n'
                    cadena2+='node'+str(contador2)+' -> node'+str(ant) +';\n'
                    cadena2+='node1 -> node'+str(contador2)+'[color=red]' + ';\n'
                else:
                    ant=contador2-1
                    sig=contador2+1
                    cadena2+='node'+str(contador2)+' -> node'+str(sig)+';\n'
                    cadena2+='node'+str(contador2)+' -> node'+str(ant)+';\n'
                contador2=contador2+1
            cadena+=cadena2
        return cadena    

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

""" ---------------------------------------------------LISTA DOBLE PARA SNAKE --------------------------------------------------------------------"""
class nodoDobleSnake():

    def __init__(self, coordenadas):                  
        self.siguiente = None        
        self.anterior =  None
        self.coordenadas = coordenadas 

class dobleSnake():
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.size=0

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

    def vaciar(self):
        self.primero=None
        self.ultimo=None
        self.size=0
    
    def reporte(self):
        contador=1  
        contador2=1      
        cadena='nullInicio[label = "null"];\n' 
        cadena2=""     
        temp=self.primero
        for i in range(self.size):
            cadenaNodo='node'+str(contador)+'[label = "{ <a> |'+str(temp.coordenadas)+' | }  "];\n'
            cadena+=cadenaNodo
            contador=contador+1
            temp=temp.siguiente
        cadena+='nullFinal[label = " null"];\n'

        for j in range(self.size):
            if contador2==1:
                cadena2+='node'+str(contador2)+':a -> nullInicio; \n'
                sig=contador2+1
                cadena2+='node'+str(contador2)+' -> node'+str(sig)+';\n'
            elif contador2==self.size:
                ant=contador2-1
                cadena2+='node'+str(contador2)+' -> nullFinal' + ';\n'
                cadena2+='node'+str(contador2)+' -> node'+str(ant) +';\n'
            else:
                ant=contador2-1
                sig=contador2+1
                cadena2+='node'+str(contador2)+' -> node'+str(sig)+';\n'
                cadena2+='node'+str(contador2)+' -> node'+str(ant)+';\n'
            contador2=contador2+1
        cadena+=cadena2
        return cadena       
    
    def imprimirLista(self):
    
        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size):
                print(temp.coordenadas,end=" ")
                temp=temp.siguiente

""" ------------------------------------------------------ PILA PUNTEO --------------------------------------------------------------------------"""
class nodoPilaPunteo():
    def __init__(self, coordenadas):                  
        self.siguiente = None        
        self.coordenadas = coordenadas 

class pilaPunteo():
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.size=0

    def estaVacia(self):
        return self.primero is None

    def insertarInicio(self, coordenadas):
        nuevo=nodoPilaPunteo(coordenadas)
        if self.estaVacia():
            self.primero=nuevo
        else:
            nuevo.siguiente=self.primero
            self.primero=nuevo
        self.size=self.size+1

    def eliminarInicio(self):
        if self.size==1:
            self.primero=None
            self.size=self.size-1
        elif self.size>1:
            aux=self.primero.siguiente
            self.primero.siguiente=None
            self.primero=aux
            self.size=self.size-1

    def vaciar(self):
        self.primero=None
        self.primero=None
        self.size=0
    
    def reporte(self):
        temp=self.primero
        cadena='node0[label = "{' 
        for i in range(self.size):
            cadenaNodo='|'+str(temp.coordenadas)
            cadena+=cadenaNodo
            temp=temp.siguiente
        cadena+='}"];'
        return cadena

    def imprimirLista(self):

        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size):
                print(temp.coordenadas,end=" ")
                temp=temp.siguiente
 
""" ----------------------------------------------------- COLA PUNTUACIONES -------------------------------------------------------------------"""
class nodoColaPuntuaciones():
    def __init__(self, coordenadas):                  
        self.siguiente = None        
        self.coordenadas = coordenadas 

class colaPuntuaciones():
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.size=0

    def estaVacia(self):
        return self.primero is None

    def insertarFinal(self, coordenadas):
        nuevo=nodoColaPuntuaciones(coordenadas)
        if self.estaVacia():
            self.primero=nuevo
            self.ultimo=nuevo
        else:
            self.ultimo.siguiente=nuevo
            self.ultimo=nuevo
        self.size=self.size+1

    def eliminar(self):
        aux=self.primero.siguiente
        self.primero.siguiente=None
        self.primero=aux
        self.size=self.size-1
    
    def vaciar(self):
        self.primero=None
        self.ultimo=None
        self.size=0
    
    def reporte(self):
        contador=1  
        contador2=1      
        cadena=""
        cadena2=""     
        temp=self.primero
        for i in range(self.size):
            cadenaNodo='node'+str(contador)+'[label = "{'+str(temp.coordenadas)+' | } "];\n'
            cadena+=cadenaNodo
            contador=contador+1
            temp=temp.siguiente

        for j in range(self.size):
            if contador2==1:
                cadena2+='node'+str(contador2)+' -> null; \n'
            elif contador2==self.size:
                ant=contador2-1
                cadena2+='node'+str(contador2)+' -> node'+str(ant) +';\n'
            else:
                ant=contador2-1
                cadena2+='node'+str(contador2)+' -> node'+str(ant)+';\n'
            contador2=contador2+1
        cadena+=cadena2
        return cadena 

    def imprimirLista(self):

        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size):
                print(temp.coordenadas,end=" ")
                temp=temp.siguiente
            
""" ----------------------------------------------------- MATRIZ PUNTUACIONES ------------------------------------------------------------------"""
def matrizPuntuaciones(nombre, punteo):
    if len(Puntuaciones)<10:
        punt=[nombre,punteo]
        Puntuaciones.append(punt)
    elif len(Puntuaciones)==10:
        del Puntuaciones[0]
        punt=[nombre,punteo]
        Puntuaciones.append(punt)


listaDobleCircularUsuarios=dobleCircularUsuarios() #objeto como variable global
listaDobleSnake=dobleSnake()  
listaPilaPunteo=pilaPunteo()
listaColaPuntuaciones=colaPuntuaciones()

""" -----------------------------------------------------PARA EL MENU PRINCIPAL ----------------------------------------------------------------"""
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
            '''stdscr.addstr(0,0,"presionaste {}".format(menu[indice_fila_actual]))
            stdscr.refresh()
            stdscr.getch()'''
            if indice_fila_actual==0:
                if str(nombreUsuarioActual[0])=='vacio':
                    a=""
                    stdscr.addstr(2,2,"NO HA SELECCIONADO USUARIO, PARA CREAR NUEVO USUARIO INGRESE UN NOMBRE ")
                    stdscr.addstr(3,2,"Y LUEGO PRESIONE ENTER: \n\n ")
                    while True:
                        tecla = stdscr.getch()                    
                        if tecla>48 and tecla <58:#numeros
                            a+=chr(tecla)
                            stdscr.addstr(6,2,format(a))
                        elif tecla>64 and tecla<91:#letras mayusculas
                            a+=chr(tecla)
                            stdscr.addstr(6,2,format(a))
                        elif tecla>96 and tecla <123:#letras minusculas
                            a+=chr(tecla)
                            stdscr.addstr(6,2,format(a))
                        elif tecla==46:#punto
                            a+=chr(tecla)
                            stdscr.addstr(6,2,format(a))
                        elif tecla==8:#borrar
                            temp=len(a)
                            a=a[:temp-1]
                            stdscr.addstr(6,2,format(a))
                        elif tecla==10 and len(a)>0:#enter 
                            nombreUsuarioActual[0]=a
                            listaDobleCircularUsuarios.insertarFinal(a)
                            stdscr.addstr(20,25,"USUARIO CREADO CORRECTAMENTE, YA PUEDES JUGAR!")
                            stdscr.getch()
                            stdscr.clear()
                            stdscr.refresh()                            
                            break

                else:    
                    jugar()
            elif indice_fila_actual==1:                               
                if listaColaPuntuaciones.estaVacia():                    
                    stdscr.addstr(11,26,"AUN NO HAN JUGADO USUARIOS!")
                else:
                    ejey=2
                    stdscr.addstr(2,20,"USUARIO")
                    stdscr.addstr(2,50,"PUNTEO")
                    for nom,punt in Puntuaciones[0:]:
                        ejey=ejey+2
                        stdscr.addstr(ejey,20,str(nom))
                        stdscr.addstr(ejey,52,str(punt))
                stdscr.getch()  
                stdscr.clear()
                stdscr.refresh()              
            elif indice_fila_actual==2:
                if listaDobleCircularUsuarios.estaVacia():
                    stdscr.addstr(11,32,"NO HAY USUARIOS!")
                    stdscr.getch()  
                    stdscr.clear()
                    stdscr.refresh() 
                else:    
                    curses.wrapper(menu_usuarios)
            elif indice_fila_actual==3:
                graficarSnake()
                graficarUsuarios()
                graficarPilaPunteo()
                graficarColaPuntuaciones()
            elif indice_fila_actual==4:
                a=""
                stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: \n\n ")
                while True:
                    tecla = stdscr.getch()                    
                    if tecla>48 and tecla <58:#numeros
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla>64 and tecla<91:#letras mayusculas
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla>96 and tecla <123:#letras minusculas
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==46:#punto
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==8:#borrar
                        temp=len(a)
                        a=a[:temp-1]
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==10:#enter   
                        try:                   
                            cargaMasiva(str(a))
                            stdscr.addstr(20,40,"USUARIOS CARGADOS CORRECTAMENTE!")
                            stdscr.getch()
                            stdscr.clear()
                            stdscr.refresh()                            
                            break
                        except:
                            stdscr.addstr(20,35,"EL NOMBRE DEL ARCHIVO NO SE ENCONTRO!")
                            stdscr.refresh()
                            stdscr.getch()
                            stdscr.clear()
                            stdscr.refresh() 
                            break                        
            elif indice_fila_actual==len(menu)-1:
                sys.exit()
        
        print_menu(stdscr,indice_fila_actual)
        stdscr.refresh()


""" -------------------------------------------------------PARA EL MENU PAUSA ------------------------------------------------------------------"""
def print_menu_Pausa(stdscr, selected_row_idx):
    h, w= stdscr.getmaxyx()
        
    for idx, row in enumerate(menuPausa):
        x=w//2 - len(row)//2
        y=h//2 -len(menuPausa) + idx
        if idx==selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)


    stdscr.refresh()
    

def menu_principal_Pausa(stdscr,snake,puntos,puntText,tamanioSnake,comida,comidapop,comidanivel):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    indice_fila_actual=0

    print_menu_Pausa(stdscr,indice_fila_actual)
    
    while 1:
        key=stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and indice_fila_actual>0:
            indice_fila_actual-=1
        elif key == curses.KEY_DOWN and indice_fila_actual<len(menuPausa)-1:
            indice_fila_actual+=1
        elif key==curses.KEY_ENTER or key in [10,13]:
            if indice_fila_actual==0:
                jugarPausa(snake,puntos,puntText,tamanioSnake,comida,comidapop,comidanivel)
            elif indice_fila_actual==1:                               
                if listaColaPuntuaciones.estaVacia():                    
                    stdscr.addstr(11,26,"AUN NO HAN JUGADO USUARIOS!")
                else:
                    ejey=2
                    stdscr.addstr(2,20,"USUARIO")
                    stdscr.addstr(2,50,"PUNTEO")
                    for nom,punt in Puntuaciones[0:]:
                        ejey=ejey+2
                        stdscr.addstr(ejey,20,str(nom))
                        stdscr.addstr(ejey,52,str(punt))
                stdscr.getch()  
                stdscr.clear()
                stdscr.refresh()              
            elif indice_fila_actual==2:
                if listaDobleCircularUsuarios.estaVacia():
                    stdscr.addstr(11,32,"NO HAY USUARIOS!")
                    stdscr.getch()  
                    stdscr.clear()
                    stdscr.refresh() 
                else:    
                    curses.wrapper(menu_usuarios_pausa(stdscr,snake))
            elif indice_fila_actual==3:
                listaDobleSnake.vaciar()
                for y,x in snake[0:]:
                    coord="("+str(x) + "," + str(y)+")"
                    listaDobleSnake.insertarFinal(coord)
                graficarSnake()
                graficarUsuarios()
                graficarPilaPunteo()
                graficarColaPuntuaciones()
            elif indice_fila_actual==4:
                a=""
                stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: \n\n ")
                while True:
                    tecla = stdscr.getch()                    
                    if tecla>48 and tecla <58:#numeros
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla>64 and tecla<91:#letras mayusculas
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla>96 and tecla <123:#letras minusculas
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==46:#punto
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==8:#borrar
                        temp=len(a)
                        a=a[:temp-1]
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==10:#enter   
                        try:                   
                            cargaMasiva(str(a))
                            stdscr.addstr(20,40,"USUARIOS CARGADOS CORRECTAMENTE!")
                            stdscr.getch()
                            stdscr.clear()
                            stdscr.refresh()                            
                            break
                        except:
                            stdscr.addstr(20,35,"EL NOMBRE DEL ARCHIVO NO SE ENCONTRO!")
                            stdscr.refresh()
                            stdscr.getch()
                            stdscr.clear()
                            stdscr.refresh() 
                            break                        
            elif indice_fila_actual==len(menuPausa)-1:
                listaDobleSnake.vaciar()
                for y,x in snake[0:]:
                    coord="("+str(x) + "," + str(y)+")"
                    listaDobleSnake.insertarFinal(coord)
                nomb=str(banderaGuardarPunteoPausa[0])
                puntt=str(banderaGuardarPunteoPausa[1])
                punt=[nomb,puntt]
                Puntuaciones.append(punt)
                pil="("+str(nomb)+","+str(puntt)+")"
                listaColaPuntuaciones.insertarFinal(pil)
                stdscr.clear()
                stdscr.refresh()
                curses.wrapper(menu_principal)
        
        print_menu_Pausa(stdscr,indice_fila_actual)
        stdscr.refresh()        
        

""" ------------------------------------------------------PARA MOSTRAR USUARIOS ----------------------------------------------------------------"""
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
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal)
        elif (tecla==curses.KEY_ENTER) or tecla in [10,13]:
            nombreUsuarioActual[0]=listaDobleCircularUsuarios.obtenerNombre(index)
        if( index < 0): # EN CASO DE QUE EL INDICE SE VUELVA NEGAVITO LO DEJAMOS EN 0
            index = listaDobleCircularUsuarios.tamanio()-1
        if( index >= listaDobleCircularUsuarios.tamanio()): # EN CASO QUE EL INDICE SE VUELVA MAYOR AL SIZE DEL ARREGLO...
            index = 0 # ... LO LIMITAMOS AL ULTIMO INDICE VALIDO
        pintar_menu(stdscr, index) # MANDAMOS A REPINTAR LA PANTALLA

def pinter_ventana(stdscr):
    # -----------------------------------------------------------
    # PINTAMOS EL MARCO DEL MENU
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # COLOR DEL MARCO
    stdscr.attron(curses.color_pair(1)) # PERMITE HABILITAR UN ATRIBUTO ESPECIFICO
    stdscr.box("|", "-") ## PINTA EL MARCO
    stdscr.attroff(curses.color_pair(1)) # DESHABILITA EL ATRIBUTO ESPECIICO
    stdscr.refresh()
    # -----------------------------------------------------------

def pintar_menu(stdsrc, index):
    # -----------------------------------------------------------
    stdsrc.clear() # LIMPIA LA CONSOLA
    pinter_ventana(stdsrc) # MANDA A PINTAR EL MARCO
    altura, ancho = stdsrc.getmaxyx() # OBTIENE LA ALTURA Y ANCHO DE LA PANTALLA
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE) # COLOR DE LAS OPCIONES, INIICIALIZA UNA PAREJA DE COLORES EL COLOR DE LETRA Y COLOR DE FONDO RESPECTIVAMENTE
    y = int(altura/2) 
    x = int((ancho/2)-(len(listaDobleCircularUsuarios.obtenerNombre(index))/2))
    stdsrc.addstr(y,x, listaDobleCircularUsuarios.obtenerNombre(index), curses.color_pair(2)) # HAGREGA UNA CADENA  LA PANTALLA EN COORDENADAS Y, X Y UN ATRIBUTO EN ESTE CASO ES LA PAREJA DE COLORES
    stdsrc.refresh()
    
 
""" -----------------------------------------------------PARA MOSTRAR USUARIOS PAUSA ------------------------------------------------------------"""
def menu_usuarios_pausa(stdscr,snake): #INICIA LAS PROPIEDADES BASICAS
    curses.curs_set(0) # SETEA EL CURSOR EN LA POSICION 0
    index = 0
    pintar_menu_pausa(stdscr, 0) # VA A INICAR EN EL INDICE 0
    while True:
        tecla = stdscr.getch() # OBTENEMOS EL CARACTER DEL TECLADO
        if(tecla == curses.KEY_RIGHT): # VERIFICAMOS SI EL FLECHA A LA DERECHA
            index = index + 1
        elif (tecla == curses.KEY_LEFT ): # VERIFICAMOS SI ES FLECHA A LA IZQUIERDA
            index = index - 1
        elif (tecla == 27): # SI ES LA TECLA DE SCAPE.... 
            nom=str(banderaGuardarPunteoPausa[0])
            punte=str(banderaGuardarPunteoPausa[1])
            punt=[nom,punte]
            Puntuaciones.append(punt)
            pil="("+str(nom)+","+str(punte)+")"
            listaColaPuntuaciones.insertarFinal(pil)
            nombreUsuarioActual[0]=listaDobleCircularUsuarios.obtenerNombre(index)
            listaDobleSnake.vaciar()
            for y,x in snake[0:]:
                coord="("+str(x) + "," + str(y)+")"
                listaDobleSnake.insertarFinal(coord)
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal)
        elif (tecla==curses.KEY_ENTER) or tecla in [10,13]:
            nom=str(banderaGuardarPunteoPausa[0])
            punte=str(banderaGuardarPunteoPausa[1])
            punt=[nom,punte]
            Puntuaciones.append(punt)
            pil="("+str(nom)+","+str(punte)+")"
            listaColaPuntuaciones.insertarFinal(pil)
            nombreUsuarioActual[0]=listaDobleCircularUsuarios.obtenerNombre(index)
            listaDobleSnake.vaciar()
            for y,x in snake[0:]:
                coord="("+str(x) + "," + str(y)+")"
                listaDobleSnake.insertarFinal(coord)
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal)
        if( index < 0): # EN CASO DE QUE EL INDICE SE VUELVA NEGAVITO LO DEJAMOS EN 0
            index = listaDobleCircularUsuarios.tamanio()-1
        if( index >= listaDobleCircularUsuarios.tamanio()): # EN CASO QUE EL INDICE SE VUELVA MAYOR AL SIZE DEL ARREGLO...
            index = 0 # ... LO LIMITAMOS AL ULTIMO INDICE VALIDO
        pintar_menu_pausa(stdscr, index) # MANDAMOS A REPINTAR LA PANTALLA

def pinter_ventana_pausa(stdscr):
    # -----------------------------------------------------------
    # PINTAMOS EL MARCO DEL MENU
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED) # COLOR DEL MARCO
    stdscr.attron(curses.color_pair(1)) # PERMITE HABILITAR UN ATRIBUTO ESPECIFICO
    stdscr.box("|", "-") ## PINTA EL MARCO
    stdscr.attroff(curses.color_pair(1)) # DESHABILITA EL ATRIBUTO ESPECIICO
    stdscr.refresh()
    # -----------------------------------------------------------

def pintar_menu_pausa(stdsrc, index):
    # -----------------------------------------------------------
    stdsrc.clear() # LIMPIA LA CONSOLA
    pinter_ventana_pausa(stdsrc) # MANDA A PINTAR EL MARCO
    altura, ancho = stdsrc.getmaxyx() # OBTIENE LA ALTURA Y ANCHO DE LA PANTALLA
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # COLOR DE LAS OPCIONES, INIICIALIZA UNA PAREJA DE COLORES EL COLOR DE LETRA Y COLOR DE FONDO RESPECTIVAMENTE
    y = int(altura/2) 
    x = int((ancho/2)-(len(listaDobleCircularUsuarios.obtenerNombre(index))/2))
    stdsrc.addstr(y,x, listaDobleCircularUsuarios.obtenerNombre(index), curses.color_pair(2)) # HAGREGA UNA CADENA  LA PANTALLA EN COORDENADAS Y, X Y UN ATRIBUTO EN ESTE CASO ES LA PAREJA DE COLORES
    stdsrc.refresh()
 

""" --------------------------------------------------------PARA LA COMIDA SNAKE --------------------------------------------------------------"""
def crear_comida(snake):
    comidaa=None

    while comidaa is None:
        comidaa=[random.randint(3, 19),random.randint(3,75)]
        if comidaa in snake:
            comidaa=None
    return comidaa

""" ---------------------------------------------------------------JUGAR -----------------------------------------------------------------------"""
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
    
    #cada vez que se juegue, se vacian las listas
    listaPilaPunteo.vaciar()
    listaDobleSnake.vaciar()

    snake=[[7, 8],[7, 7],[7, 6]]#tamanio snake

    for y,x in snake:
        window.addch(y,x,'@')
    
    comida=crear_comida(snake)
    window.addch(comida[0], comida[1], '+')

    comidapop=crear_comida(snake)
    window.addch(comidapop[0], comidapop[1], '*') 

    comidanivel=crear_comida(snake)
    
    indiceIzquierdo=[[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1],[21,1],[22,1],[23,1]]
    indiceDerecho=[[1,78],[2,78],[3,78],[4,78],[5,78],[6,78],[7,78],[8,78],[9,78],[10,78],[11,78],[12,78],[13,78],[14,78],[15,78],[16,78],[17,78],[18,78],[19,78],[20,78],[21,78],[22,78],[23,78]]
    indiceSuperior=[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29],[1,30],[1,31],[1,32],[1,33],[1,34],[1,35],[1,36],[1,37],[1,38],[1,39],[1,40],[1,41],[1,42],[1,43],[1,44],[1,45],[1,46],[1,47],[1,48],[1,49],[1,50],[1,51],[1,52],[1,53],[1,54],[1,55],[1,56],[1,57],[1,58],[1,59],[1,60],[1,61],[1,62],[1,63],[1,64],[1,65],[1,66],[1,67],[1,68],[1,69],[1,70],[1,71],[1,72],[1,73],[1,74],[1,75],[1,76],[1,77]]
    indiceInferior=[[23,2],[23,3],[23,4],[23,5],[23,6],[23,7],[23,8],[23,9],[23,10],[23,11],[23,12],[23,13],[23,14],[23,15],[23,16],[23,17],[23,18],[23,19],[23,20],[23,21],[23,22],[23,23],[23,24],[23,25],[23,26],[23,27],[23,28],[23,29],[23,30],[23,31],[23,32],[23,33],[23,34],[23,35],[23,36],[23,37],[23,38],[23,39],[23,40],[23,41],[23,42],[23,43],[23,44],[23,45],[23,46],[23,47],[23,48],[23,49],[23,50],[23,51],[23,52],[23,53],[23,54],[23,55],[23,56],[23,57],[23,58],[23,59],[23,60],[23,61],[23,62],[23,63],[23,64],[23,65],[23,66],[23,67],[23,68],[23,69],[23,70],[23,71],[23,72],[23,73],[23,74],[23,75],[23,76],[23,77]]
    
    tamanioSnake=3
    puntos=0
    puntText="PUNTOS: " + str(puntos)
    window.addstr(0,5,puntText)

    usuariojug= "JUGADOR: " + nombreUsuarioActual[0]
    window.addstr(0,32,usuariojug)

    textoNivel="NIVEL: 1" 
    
    window.addstr(0,60,textoNivel)

    while key!=27:
        '''SEGUNDO NIVEL MAS RAPIDO'''
        if puntos>=15:
            textoNivel="NIVEL: 2" 
            window.timeout(2)            
            window.addstr(0,60,textoNivel)
            window.addch(comidanivel[0], comidanivel[1], 'G')
        else:
            window.timeout(100)

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
        elif key==109 or key==32: #letra m o espacio -> pausa
            banderaGuardarPunteoPausa[0]=str(nombreUsuarioActual[0])
            banderaGuardarPunteoPausa[1]=str(puntos)
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal_Pausa(stdscr,snake,puntos,textoNivel,tamanioSnake,comida,comidapop,comidanivel))            
            
        snake.insert(0,nuevaCabeza)
        window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')

        if snake[0] ==comida:
            pil=[comida]
            for y,x in pil:
                coord="("+str(x) + "," + str(y)+")"
                listaPilaPunteo.insertarInicio(coord)
            comida=crear_comida(snake)
            window.addch(comida[0], comida[1], '+')
            puntos=puntos+1
            puntText="PUNTOS: " + str(puntos)
            window.addstr(0,5,puntText)
            tamanioSnake=tamanioSnake+1
        elif snake[0] ==comidapop and tamanioSnake<4: #si el tamanio de snake es menor a 3, lo deja igual
            listaPilaPunteo.eliminarInicio()
            comidapop=crear_comida(snake)
            window.addch(comidapop[0], comidapop[1], '*')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
        elif snake[0] ==comidapop and tamanioSnake>3: #si el tamanio de snake es mayor a 3, disminuye
            listaPilaPunteo.eliminarInicio()
            comidapop=crear_comida(snake)
            window.addch(comidapop[0], comidapop[1], '*')
            aa=[snake.pop()] #captura coordenadas del pop()            
            for y,x in aa:
                window.addch(y, x, ' ') #pinta nada en las coordenadas del pop()
            bb=[snake.pop()]
            for y,x in bb:
                window.addch(y, x, ' ')
            tamanioSnake=tamanioSnake-1
           
            if puntos>0:#solo si el punteo es mayor a 0 resta puntos                  
                puntos=puntos-1
                puntText="PUNTOS: " + str(puntos)
                window.addstr(0,5,puntText)  
        elif snake[0]==comidanivel and puntos>=15:
            comidanivel=crear_comida(snake)
            window.addch(comidanivel[0], comidanivel[1], 'G')
            if puntos>=2:
                puntos=puntos-2
                puntText="PUNTOS: " + str(puntos)
                window.addstr(0,5,puntText)                  
        else:
            window.addch(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
         
        #para que se pase de un lado para el otro    
        if (snake[0] in indiceIzquierdo[0:]):  
            nuevaCabeza=[cabeza[0], cabeza[1]+76]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in indiceDerecho[0:]): 
            nuevaCabeza=[cabeza[0], cabeza[1]-76]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in indiceSuperior[0:]):
            nuevaCabeza=[cabeza[0]+21, cabeza[1]]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in indiceInferior[0:]):
            nuevaCabeza=[cabeza[0]-21, cabeza[1]]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in snake[1:]): 
            for y,x in snake[0:]:
                coord="("+str(x) + "," + str(y)+")"
                listaDobleSnake.insertarFinal(coord)            
            matrizPuntuaciones(str(nombreUsuarioActual[0]),puntos)
            listaColaPuntuaciones.vaciar() #vaciar para luego volver a llenar (sino se lo mismo)
            for nom,punt in Puntuaciones[0:]:
                pil="("+str(nom)+","+str(punt)+")"
                listaColaPuntuaciones.insertarFinal(pil)
            msg="HAS PERDIDO VUELVE A INTENTARLO!"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.getch()
            stdscr.clear()
            window.refresh()
            break        

        window.refresh()

    curses.endwin()


def jugarPausa(snake,punt,textlevel,tamansnak,comid,comidpop,comidlevel):
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
    
    for y,x in snake:
        window.addch(y,x,'@')
    
    comida=comid
    window.addch(comida[0], comida[1], '+')

    comidapop=comidpop
    window.addch(comidapop[0], comidapop[1], '*') 

    comidanivel=comidlevel
    
    indiceIzquierdo=[[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1],[17,1],[18,1],[19,1],[20,1],[21,1],[22,1],[23,1]]
    indiceDerecho=[[1,78],[2,78],[3,78],[4,78],[5,78],[6,78],[7,78],[8,78],[9,78],[10,78],[11,78],[12,78],[13,78],[14,78],[15,78],[16,78],[17,78],[18,78],[19,78],[20,78],[21,78],[22,78],[23,78]]
    indiceSuperior=[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[1,13],[1,14],[1,15],[1,16],[1,17],[1,18],[1,19],[1,20],[1,21],[1,22],[1,23],[1,24],[1,25],[1,26],[1,27],[1,28],[1,29],[1,30],[1,31],[1,32],[1,33],[1,34],[1,35],[1,36],[1,37],[1,38],[1,39],[1,40],[1,41],[1,42],[1,43],[1,44],[1,45],[1,46],[1,47],[1,48],[1,49],[1,50],[1,51],[1,52],[1,53],[1,54],[1,55],[1,56],[1,57],[1,58],[1,59],[1,60],[1,61],[1,62],[1,63],[1,64],[1,65],[1,66],[1,67],[1,68],[1,69],[1,70],[1,71],[1,72],[1,73],[1,74],[1,75],[1,76],[1,77]]
    indiceInferior=[[23,2],[23,3],[23,4],[23,5],[23,6],[23,7],[23,8],[23,9],[23,10],[23,11],[23,12],[23,13],[23,14],[23,15],[23,16],[23,17],[23,18],[23,19],[23,20],[23,21],[23,22],[23,23],[23,24],[23,25],[23,26],[23,27],[23,28],[23,29],[23,30],[23,31],[23,32],[23,33],[23,34],[23,35],[23,36],[23,37],[23,38],[23,39],[23,40],[23,41],[23,42],[23,43],[23,44],[23,45],[23,46],[23,47],[23,48],[23,49],[23,50],[23,51],[23,52],[23,53],[23,54],[23,55],[23,56],[23,57],[23,58],[23,59],[23,60],[23,61],[23,62],[23,63],[23,64],[23,65],[23,66],[23,67],[23,68],[23,69],[23,70],[23,71],[23,72],[23,73],[23,74],[23,75],[23,76],[23,77]]
    
    tamanioSnake=tamansnak
    puntos=punt
    puntText="PUNTOS: " + str(puntos)
    window.addstr(0,5,puntText)

    usuariojug= "JUGADOR: " + nombreUsuarioActual[0]
    window.addstr(0,32,usuariojug)

    textoNivel=textlevel 
    
    window.addstr(0,60,textoNivel)

    while key!=27:
        '''SEGUNDO NIVEL MAS RAPIDO'''
        if puntos>=15:
            textoNivel="NIVEL: 2" 
            window.timeout(2)            
            window.addstr(0,60,textoNivel)
            window.addch(comidanivel[0], comidanivel[1], 'G')
        else:
            window.timeout(100)

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
        elif key==109 or key==32: #letra m o espacio -> pausa
            banderaGuardarPunteoPausa[0]=str(nombreUsuarioActual[0])
            banderaGuardarPunteoPausa[1]=str(puntos)
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal_Pausa(stdscr,snake,puntos,textoNivel,tamanioSnake,comida,comidapop,comidanivel)) 

        snake.insert(0,nuevaCabeza)
        window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')

        if snake[0] ==comida:
            pil=[comida]
            for y,x in pil:
                coord="("+str(x) + "," + str(y)+")"
                listaPilaPunteo.insertarInicio(coord)
            comida=crear_comida(snake)
            window.addch(comida[0], comida[1], '+')
            puntos=puntos+1
            puntText="PUNTOS: " + str(puntos)
            window.addstr(0,5,puntText)
            tamanioSnake=tamanioSnake+1
        elif snake[0] ==comidapop and tamanioSnake<4: #si el tamanio de snake es menor a 3, lo deja igual
            listaPilaPunteo.eliminarInicio()
            comidapop=crear_comida(snake)
            window.addch(comidapop[0], comidapop[1], '*')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
        elif snake[0] ==comidapop and tamanioSnake>3: #si el tamanio de snake es mayor a 3, disminuye
            listaPilaPunteo.eliminarInicio()
            comidapop=crear_comida(snake)
            window.addch(comidapop[0], comidapop[1], '*')
            aa=[snake.pop()] #captura coordenadas del pop()            
            for y,x in aa:
                window.addch(y, x, ' ') #pinta nada en las coordenadas del pop()
            bb=[snake.pop()]
            for y,x in bb:
                window.addch(y, x, ' ')
            tamanioSnake=tamanioSnake-1
            
            if puntos>0:#solo si el punteo es mayor a 0 resta puntos                  
                puntos=puntos-1
                puntText="PUNTOS: " + str(puntos)
                window.addstr(0,5,puntText)  
        elif snake[0]==comidanivel and puntos>=15:
            comidanivel=crear_comida(snake)
            window.addch(comidanivel[0], comidanivel[1], 'G')
            if puntos>=2:
                puntos=puntos-2
                puntText="PUNTOS: " + str(puntos)
                window.addstr(0,5,puntText)                  
        else:
            window.addch(snake[-1][0], snake[-1][1], ' ')
            snake.pop()
            
        #para que se pase de un lado para el otro    
        if (snake[0] in indiceIzquierdo[0:]):  
            nuevaCabeza=[cabeza[0], cabeza[1]+76]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in indiceDerecho[0:]): 
            nuevaCabeza=[cabeza[0], cabeza[1]-76]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in indiceSuperior[0:]):
            nuevaCabeza=[cabeza[0]+21, cabeza[1]]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in indiceInferior[0:]):
            nuevaCabeza=[cabeza[0]-21, cabeza[1]]
            snake.insert(0,nuevaCabeza)
            window.addch(nuevaCabeza[0], nuevaCabeza[1],'@')
            window.addch(snake[-1][0], snake[-1][1], ' ')
            tamanioSnake=tamanioSnake+1
        elif (snake[0] in snake[1:]): 
            for y,x in snake[0:]:
                coord="("+str(x) + "," + str(y)+")"
                listaDobleSnake.insertarFinal(coord)            
            matrizPuntuaciones(str(nombreUsuarioActual[0]),puntos)
            listaColaPuntuaciones.vaciar() #vaciar para luego volver a llenar (sino se lo mismo)
            for nom,punt in Puntuaciones[0:]:
                pil="("+str(nom)+","+str(punt)+")"
                listaColaPuntuaciones.insertarFinal(pil)
            msg="HAS PERDIDO VUELVE A INTENTARLO!"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.getch()
            stdscr.clear()
            window.refresh()
            curses.wrapper(menu_principal)        

        window.refresh()

    curses.endwin()

""" -------------------------------------------------------------CARGA MASIVA -------------------------------------------------------------------"""

def cargaMasiva(ruta): 
    
    #with open('C:\\Users\\GUDIEL\\Desktop\\cargaMasiva1.csv') as f:
    with open(ruta) as f:
        ingresarCabecera=0 #para no ingresar cabecera
        reader=csv.reader(f)
        for row in reader:
            if ingresarCabecera!=0:#no ingresa el primer elemento (cabecera)
                us="{0}".format(row[0])
                listaDobleCircularUsuarios.insertarFinal(us)
            ingresarCabecera=ingresarCabecera+1


""" ---------------------------------------------------------------GRAFICAS ---------------------------------------------------------------------"""    
def graficarSnake():
    # open(nombre_archivo.ext, formato)
    f = open("snake.dot", "w") 
    # write("texto a escribir") 
    
    f.write("digraph G {\n")
    f.write('rankdir="LR"')
    f.write("node [shape=record,width=.1,height=.1];")
    
    a=listaDobleSnake.reporte()
    f.write(a)

    f.write("}")
    # CIERRA EL ARCHIVO
    f.close()
    # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
    os.system("dot -Tjpg"+ " snake.dot " +"-o snake.jpg")
    os.system("snake.jpg")

def graficarPilaPunteo():
    # open(nombre_archivo.ext, formato)
    f = open("pilapunt.dot", "w") 
    # write("texto a escribir") 
    
    f.write("digraph G {\n")
    f.write("node [shape=record,width=.1,height=.1];")
    
    a=listaPilaPunteo.reporte()
    f.write(a)

    f.write("}")
    # CIERRA EL ARCHIVO
    f.close()
    # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
    os.system("dot -Tjpg"+ " pilapunt.dot " +"-o pilapunt.jpg")
    os.system("pilapunt.jpg")

def graficarUsuarios():
    # open(nombre_archivo.ext, formato)
    f = open("usuarios.dot", "w") 
    # write("texto a escribir") 
    
    f.write("digraph G {\n")
    f.write('rankdir="LR"')
    f.write("node [shape=record,width=.1,height=.1];")
    
    a=listaDobleCircularUsuarios.reporte()
    f.write(a)

    f.write("}")
    # CIERRA EL ARCHIVO
    f.close()
    # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
    os.system("dot -Tjpg"+ " usuarios.dot " +"-o usuarios.jpg")
    os.system("usuarios.jpg")

def graficarColaPuntuaciones():
    # open(nombre_archivo.ext, formato)
    f = open("colapunt.dot", "w") 
    # write("texto a escribir") 
    
    f.write("digraph G {\n")
    f.write('rankdir="LR"')
    f.write("node [shape=record,width=.1,height=.1];")
    
    a=listaColaPuntuaciones.reporte()
    f.write(a)

    f.write("}")
    # CIERRA EL ARCHIVO
    f.close()
    # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
    os.system("dot -Tjpg"+ " colapunt.dot " +"-o colapunt.jpg")
    os.system("colapunt.jpg")


curses.wrapper(menu_principal)
