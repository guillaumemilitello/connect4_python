'''
Created on Mar 13, 2016

@author: guillaume
'''

# board dimensions settings
COL_WIDTH  = 6
COL_HEIGHT = 3

import terminal
from game import WIDTH, HEIGHT

def menuToken(choice):
    terminal.addString(2, terminal.position.CENTER, 'Connect4', terminal.color.RED, True)
    terminal.addString(4, terminal.position.CENTER, 'Choose your token', terminal.color.BLACK)
    if choice == 0:
        terminal.addString(5, terminal.position.CENTER, '--> X   ', terminal.color.RED, True)
        terminal.addString(6, terminal.position.CENTER, '    O   ', terminal.color.GREY)
    else:
        terminal.addString(5, terminal.position.CENTER, '    X   ', terminal.color.GREY)
        terminal.addString(6, terminal.position.CENTER, '--> O   ', terminal.color.YELLOW, True)

def menuTurn(choice):
    terminal.addString(8, terminal.position.CENTER, 'Who plays first ?', terminal.color.BLACK)
    if choice == 0:
        terminal.addString(9,  terminal.position.CENTER, '--> player   ', terminal.color.BLACK, True)
        terminal.addString(10, terminal.position.CENTER, '    computer ', terminal.color.GREY)
        terminal.addString(11, terminal.position.CENTER, '    random   ', terminal.color.GREY)
    elif choice == 1:
        terminal.addString(9,  terminal.position.CENTER, '    player   ', terminal.color.GREY)
        terminal.addString(10, terminal.position.CENTER, '--> computer ', terminal.color.BLACK, True)
        terminal.addString(11, terminal.position.CENTER, '    random   ', terminal.color.GREY)
    else:
        terminal.addString(9,  terminal.position.CENTER, '    player   ', terminal.color.GREY)
        terminal.addString(10, terminal.position.CENTER, '    computer ', terminal.color.GREY)
        terminal.addString(11, terminal.position.CENTER, '--> random   ', terminal.color.BLACK, True)

def menuLevel(choice):
    terminal.addString(13, terminal.position.CENTER, 'Choose the level', terminal.color.BLACK)
    if choice == 0:
        terminal.addString(14, terminal.position.CENTER, '--> 1   ', terminal.color.BLACK, True)
        terminal.addString(15, terminal.position.CENTER, '    2   ', terminal.color.GREY)
        terminal.addString(16, terminal.position.CENTER, '    3   ', terminal.color.GREY)
        terminal.addString(17, terminal.position.CENTER, '    4   ', terminal.color.GREY)
        terminal.addString(18, terminal.position.CENTER, '    5   ', terminal.color.GREY)
        terminal.addString(19, terminal.position.CENTER, '    6   ', terminal.color.GREY)
    elif choice == 1:
        terminal.addString(14, terminal.position.CENTER, '    1   ', terminal.color.GREY)
        terminal.addString(15, terminal.position.CENTER, '--> 2   ', terminal.color.BLACK, True)
        terminal.addString(16, terminal.position.CENTER, '    3   ', terminal.color.GREY)
        terminal.addString(17, terminal.position.CENTER, '    4   ', terminal.color.GREY)
        terminal.addString(18, terminal.position.CENTER, '    5   ', terminal.color.GREY)
        terminal.addString(19, terminal.position.CENTER, '    6   ', terminal.color.GREY)
    elif choice == 2:
        terminal.addString(14, terminal.position.CENTER, '    1   ', terminal.color.GREY)
        terminal.addString(15, terminal.position.CENTER, '    2   ', terminal.color.GREY)
        terminal.addString(16, terminal.position.CENTER, '--> 3   ', terminal.color.BLACK, True)
        terminal.addString(17, terminal.position.CENTER, '    4   ', terminal.color.GREY)
        terminal.addString(18, terminal.position.CENTER, '    5   ', terminal.color.GREY)
        terminal.addString(19, terminal.position.CENTER, '    6   ', terminal.color.GREY)
    elif choice == 3:
        terminal.addString(14, terminal.position.CENTER, '    1   ', terminal.color.GREY)
        terminal.addString(15, terminal.position.CENTER, '    2   ', terminal.color.GREY)
        terminal.addString(16, terminal.position.CENTER, '    3   ', terminal.color.GREY)
        terminal.addString(17, terminal.position.CENTER, '--> 4   ', terminal.color.BLACK, True)
        terminal.addString(18, terminal.position.CENTER, '    5   ', terminal.color.GREY)
        terminal.addString(19, terminal.position.CENTER, '    6   ', terminal.color.GREY)
    elif choice == 4:
        terminal.addString(14, terminal.position.CENTER, '    1   ', terminal.color.GREY)
        terminal.addString(15, terminal.position.CENTER, '    2   ', terminal.color.GREY)
        terminal.addString(16, terminal.position.CENTER, '    3   ', terminal.color.GREY)
        terminal.addString(17, terminal.position.CENTER, '    4   ', terminal.color.GREY)
        terminal.addString(18, terminal.position.CENTER, '--> 5   ', terminal.color.BLACK, True)
        terminal.addString(19, terminal.position.CENTER, '    6   ', terminal.color.GREY)
    else:
        terminal.addString(14, terminal.position.CENTER, '    1   ', terminal.color.GREY)
        terminal.addString(15, terminal.position.CENTER, '    2   ', terminal.color.GREY)
        terminal.addString(16, terminal.position.CENTER, '    3   ', terminal.color.GREY)
        terminal.addString(17, terminal.position.CENTER, '    4   ', terminal.color.GREY)
        terminal.addString(18, terminal.position.CENTER, '    5   ', terminal.color.GREY)
        terminal.addString(19, terminal.position.CENTER, '--> 6   ', terminal.color.BLACK, True)

def menuClear():
    terminal.clearLine(5)
    terminal.clearLine(6)

def boardScores(player_token, computer_token, player_score, computer_score):
    terminal.addString(4, terminal.position.CENTER, '  player %d - %d computer' %(player_score, computer_score))
    # fixed string score length
    x = terminal.width/2 - (25)/2 + 1
    if player_token == 'X':
        terminal.addString(4, x, 'X', terminal.color.RED)
    else:
        terminal.addString(4, x, 'O', terminal.color.YELLOW)
    x = terminal.width/2 + (25)/2 + 1
    if computer_token == 'X':
        terminal.addString(4, x, 'X', terminal.color.RED)
    else:
        terminal.addString(4, x, 'O', terminal.color.YELLOW)

def arrowMove(move):
    terminal.clearLine(6)
    x = terminal.width/2 - (WIDTH*COL_WIDTH+1)/2 +COL_WIDTH*move+3 
    terminal.addString(6, x, 'V', terminal.color.BLACK, True)

def arrowMoveClear():
    terminal.clearLine(6)

def boardEmpty():
    y = 7
    for line in range(HEIGHT):
        #empty line
        terminal.addString(y  , terminal.position.CENTER, ('|'+(' '*(COL_WIDTH-1)))*WIDTH + '|', terminal.color.BLUE)
        terminal.addString(y+1, terminal.position.CENTER, ('|'+(' '*(COL_WIDTH-1)))*WIDTH + '|', terminal.color.BLUE)
        # draw the last line
        if line == HEIGHT - 1:
            terminal.addString(y+2, terminal.position.CENTER, ('|'+('_'*(COL_WIDTH-1)))*WIDTH + '|', terminal.color.BLUE)
        else:
            terminal.addString(y+2, terminal.position.CENTER, ('|'+(' '*(COL_WIDTH-1)))*WIDTH + '|', terminal.color.BLUE)
            y += 3

def boardToken(move, line, token):
        x = terminal.width/2 - (WIDTH*COL_WIDTH+1)/2 +COL_WIDTH*move+3
        y = 7+(COL_HEIGHT*line)+1
        terminal.addString(y, x, token)

def boardWinnerTokens(move, line, token, winner_tokens):
    for i in range(len(winner_tokens)):
        line = winner_tokens[i][0]
        col  = winner_tokens[i][1]
        x = terminal.width/2 - (WIDTH*COL_WIDTH+1)/2 +COL_WIDTH*col+3
        y = 7+(COL_HEIGHT*line)+1
        terminal.addString(y, x, token, 0, True)

def noticeMove():
    terminal.clearLine(26)
    terminal.addString(26, terminal.position.CENTER, 'Make your move or quit ? [q]')

def noticeComputer():
    terminal.clearLine(26)
    terminal.addString(26, terminal.position.CENTER, 'The computer is thinking...')
    terminal.clearLine(27)

def noticeComputerTime(time):
    terminal.clearLine(27)
    terminal.addString(27, terminal.position.CENTER, 'computer\'s move calculated in %.3fs' %time, terminal.color.GREY)

def noticePlayAgain():
    terminal.clearLine(26)
    terminal.addString(26, terminal.position.CENTER, 'Do you want to play again ? [y,n]', terminal.color.BLACK, True)
