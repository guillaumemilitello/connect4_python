'''
Created on Mar 13, 2016

@author: guillaume
'''
import terminal
import board

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

def boardArrow(move):
    terminal.clearLine(6)
    x = terminal.width/2 - (board.width*board.col_width+1)/2 +board.col_width*move+3 
    terminal.addString(6, x, 'V', terminal.color.BLACK, True)

def boardEmpty():
    y = 7
    for line in range(board.height):
        #empty line
        terminal.addString(y  , terminal.position.CENTER, ('|'+(' '*(board.col_width-1)))*board.width + '|', terminal.color.BLUE)
        terminal.addString(y+1, terminal.position.CENTER, ('|'+(' '*(board.col_width-1)))*board.width + '|', terminal.color.BLUE)
        # draw the last line
        if line == board.height-1:
            terminal.addString(y+2, terminal.position.CENTER, ('|'+('_'*(board.col_width-1)))*board.width + '|', terminal.color.BLUE)
        else:
            terminal.addString(y+2, terminal.position.CENTER, ('|'+(' '*(board.col_width-1)))*board.width + '|', terminal.color.BLUE)
            y += 3

def boardToken(m_board, move):
    for line in range(board.height):
        if not m_board[line][move] == '':
            x = terminal.width/2 - (board.width*board.col_width+1)/2 +board.col_width*move+3
            y = 7+(board.col_height*line)+1
            if m_board[line][move] == 'X':
                terminal.addString(y, x, 'X', terminal.color.RED)
            elif m_board[line][move] == 'O':
                terminal.addString(y, x, 'O', terminal.color.YELLOW)
            return

def boardTokenBold(line, col, token):
    x = terminal.width/2 - (board.width*board.col_width+1)/2 +board.col_width*col+3
    y = 7+(board.col_height*line)+1
    if token == 'X':
        terminal.addString(y, x, token, terminal.color.RED_H, True)
    elif token == 'O':
        terminal.addString(y, x, token, terminal.color.YELLOW_H, True)

def noticeMove():
    terminal.clearLine(26)
    terminal.addString(26, terminal.position.CENTER, 'Make your move or quit ? [q]', terminal.color.BLACK)

def noticeComputer():
    terminal.clearLine(26)
    terminal.addString(26, terminal.position.CENTER, 'The computer is thinking...', terminal.color.BLACK)

def noticePlayAgain():
    terminal.clearLine(26)
    terminal.addString(26, terminal.position.CENTER, 'Do you want to play again ? [y,n]', terminal.color.BLACK, True)
