import curses
import time

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

menu=['Jugar','Puntuaciones','Usuarios','Reportes','Carga Masica',"Salir"]

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

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx=0

    print_menu(stdscr,current_row_idx)
    
    while 1:
        key=stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx>0:
            current_row_idx-=1
        elif key == curses.KEY_DOWN and current_row_idx<len(menu)-1:
            current_row_idx+=1
        elif key==curses.KEY_ENTER or key in [10,13]:
            stdscr.addstr(0,0,"presionaste {}".format(menu[current_row_idx]))
            stdscr.refresh()
            stdscr.getch()
            if current_row_idx==len(menu)-1:
                jugar()
        
        print_menu(stdscr,current_row_idx)
        stdscr.refresh()

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


curses.wrapper(main)