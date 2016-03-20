'''
Created on Mar 5, 2016

@author: guillaume
'''

from random import randint
from signal import signal, SIGINT
from sys import exit

import draw
import terminal
import computer
import board

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


def mainMenu():
    pos = 0
    player_token = ''
    turn = ''

    while player_token == '':
        
        draw.menuToken(pos)
        
        k = terminal.getKey()

        if k == keyboard.DOWN_KEY and pos < 1:
            pos += 1;
        elif k == keyboard.UP_KEY and pos > 0:
            pos -= 1;
        # press enter
        elif k == keyboard.ENTER_KEY and pos == 0:
            player_token = 'X'
            computer_token = 'O'
        elif k == keyboard.ENTER_KEY and pos == 1:
            player_token = 'O'
            computer_token = 'X'

    # default choice computer
    pos = 1
    while not (turn == 'player' or turn == 'computer'):
        draw.menuTurn(pos)
        k = terminal.getKey()

        if k == keyboard.DOWN_KEY and pos < 2:
            pos += 1;
        elif k == keyboard.UP_KEY and pos > 0:
            pos -= 1;
        # press enter
        elif k == keyboard.ENTER_KEY:
            if pos == 0:
                turn = 'player'
            elif pos == 1:
                turn = 'computer'
            elif pos == 2:
                if randint(0, 1) == 0:
                    turn = 'computer'
                else:
                    turn = 'player'
                    
    draw.menuClear()
    return player_token, computer_token, turn

def main():

    global main_board
    main_board = [['' for _ in range(board.width)] for _ in range(board.height)]
    player_score = 0
    computer_score = 0
    
    player_token, computer_token, turn = mainMenu()

    # until the player wants to play
    while True:
        draw.boardScores(player_token, computer_token, player_score, computer_score)
        draw.boardEmpty()
        # until the current game is on
        while True:
            if turn == 'player':
                draw.noticeMove()
                move = getHumanMoveArrow()
                # quit
                if move == -1:
                    return
                line = board.makeMove(main_board, player_token, move)
                draw.boardToken(main_board, move)
                if board.isWinner(main_board, player_token, True):
                    player_score += 1
                    break
                # next turn
                turn = 'computer'
            else:
                draw.noticeComputer()
                move = computer.getComputerBestMove(main_board, computer_token)
                line = board.makeMove(main_board, computer_token, move)
                draw.boardToken(main_board, move)
                if board.isWinner(main_board, computer_token, True):
                    computer_score += 1
                    break
                # next turn
                turn = 'player'

            if board.isBoardFull(main_board):
                break

        # update boardScores
        draw.boardScores(player_token, computer_token, player_score, computer_score)
        if menuPlayAgain():
            for col in range(board.width):
                for line in range(board.height):
                    main_board[line][col] = ''
        else:
            return

def menuPlayAgain():
    draw.noticePlayAgain()
    while True:
        k = terminal.getKey()
        # 
        if k ==  keyboard.Y_UPPER_KEY or k == keyboard.Y_KEY or k == keyboard.ENTER_KEY:
            return True
        elif k == keyboard.N_UPPER_KEY or k == keyboard.N_KEY or k == keyboard.Q_UPPER_KEY or k == keyboard.Q_KEY:
            return False

def getHumanMoveArrow():
    pos = 3
    while True:
        # draw arrow full string
        draw.boardArrow(pos)
        k = terminal.getKey()
        if k == keyboard.RIGHT_KEY and pos < board.width-1:
            pos += 1
        elif k == keyboard.LEFT_KEY and pos > 0:
            pos -= 1
        elif k == keyboard.ENTER_KEY and board.isValidMove(main_board, pos):
            break
        elif k == keyboard.Q_UPPER_KEY or k == keyboard.Q_KEY:
            return -1

    # remove detailed arrow
    terminal.clearLine(6)
    return pos

# handle SIGINT signal
def signalHandler(signum, frame):
    terminal.term()
    exit()

if __name__ == '__main__':
    signal(SIGINT, signalHandler)
    main()
    terminal.term()
