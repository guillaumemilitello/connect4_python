'''
Created on Mar 12, 2016

@author: guillaume
'''

import curses
import sys
import terminalsize
import board

class position:
    CENTER   = -1
    
class color:
    BLACK    =  0
    RED      =  1
    YELLOW   =  2
    BLUE     =  3
    GREY     =  4
    RED_H    =  5
    YELLOW_H =  6

# MAC OS X mapping
class keyboard:
    LEFT_KEY = 260
    RIGHT_KEY = 261
    UP_KEY = 259
    DOWN_KEY = 258
    ENTER_KEY = 10
    Q_KEY = 81
    Q_UPPER_KEY = 113
    Y_KEY = 89
    Y_UPPER_KEY = 121
    N_KEY = 78
    N_UPPER_KEY = 110

def init():
    height_term, width_term = terminalsize.get_terminal_size()
    height_min = board.col_height * board.height + 2 + 8
    width_min = board.col_width * board.width + 2 + 5
    if height_term < height_min or width_term < width_min:
        # resize the terminal to fit the minimum size to display the connect4 before exit
        sys.stdout.write("\x1b[8;{h};{w}t".format(h=max(height_min, height_term), w=max(width_min, width_term)))
        sys.exit('Please resize your terminal [%d%s%d] (minimum required 45x28)' %(width_term, 'x', height_term))
    stdscr = curses.initscr()
    height,width = stdscr.getmaxyx()
    if height < height_min or width < width_min:
        # abort the program if the terminal can't be resized
        curses.endwin()
        sys.exit('Please resize your terminal [%d%s%d] (minimum required 45x28)' %(width, 'x', height))
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)
    #define the different colors
    if curses.can_change_color():
        defineColors()
    #return stdscr, width
    stdscr.clear()
    stdscr.border(0)
    return stdscr, width, height

def close():
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

def defineColors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(color.BLACK,    curses.COLOR_BLACK,  -1)
    curses.init_pair(color.GREY,     250,                 -1)
    curses.init_pair(color.RED,      curses.COLOR_RED,    -1)
    curses.init_pair(color.YELLOW,   143,                 -1)
    curses.init_pair(color.BLUE,     curses.COLOR_BLUE,   -1)
    # highlight text
    curses.init_pair(color.RED_H,    curses.COLOR_RED,    curses.COLOR_WHITE)
    curses.init_pair(color.YELLOW_H, curses.COLOR_YELLOW, curses.COLOR_WHITE)

def clearLine(y):
    stdscr.addstr(y, 1, ' ' * (width - 2))

def getKeywordKey():
    return stdscr.getch()

def addString(y, x, string, string_color=color.BLACK, bold=False):
    if x == position.CENTER:
        x = width/2 - len(string)/2
    options = 0
    if curses.can_change_color():
        # tokens special cases color
        if string == 'X':
            options = curses.color_pair(color.RED) if not bold else curses.color_pair(color.RED_H) | curses.A_BOLD
        elif string == 'O':
            options = curses.color_pair(color.YELLOW) if not bold else curses.color_pair(color.YELLOW_H) | curses.A_BOLD
        else:
            options = curses.color_pair(string_color)
    if bold:
        options |= curses.A_BOLD
    stdscr.addstr(y, x, string, options)
    stdscr.refresh()

# main display
stdscr, width, height = init()
