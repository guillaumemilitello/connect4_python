'''
Created on Mar 5, 2016

@author: guillaume
'''

import draw
from game import Game, WIDTH
from computer import getComputerBestMove
from terminal import getKeywordKey, close, keyboard

from random import randint
from signal import signal, SIGINT
from sys import exit

QUIT_GAME = -1

def main():

    # return an initialized game
    main_game = mainMenu()
    player_score = 0
    computer_score = 0

    # until the player wants to play, break on QUIT_GAME
    while True:
        draw.boardScores(main_game.player_token, main_game.computer_token, player_score, computer_score)
        draw.boardEmpty()

        # until the current game is on, break on victory
        while True:

            if main_game.turn == 'player':
                draw.noticeMove()
                move = getHumanMoveArrow(main_game)
                # quit game
                if move == QUIT_GAME:
                    return
                winner_move, line = main_game.makeMove(move)
                if winner_move:
                    draw.boardWinnerTokens(move, line, main_game.player_token, main_game.winner_tokens)
                    player_score += 1
                    break
                else:
                    draw.boardToken(move, line, main_game.player_token)

            if main_game.turn == 'computer':
                draw.noticeComputer()
                move, processing_time = getComputerBestMove(main_game)
                draw.noticeComputerTime(processing_time)
                winner_move, line = main_game.makeMove(move)
                if winner_move:
                    draw.boardWinnerTokens(move, line, main_game.computer_token, main_game.winner_tokens)
                    computer_score += 1
                    break
                else:
                    draw.boardToken(move, line, main_game.computer_token)

            # drawn game
            if main_game.full():
                break

        # update boardScores
        draw.boardScores(main_game.player_token, main_game.computer_token, player_score, computer_score)
        if menuPlayAgain():
            main_game.reset()
        else:
            break

def mainMenu():
    position = 0
    player_token = ''
    first_turn = ''
    level = 0

    # player token choice
    while player_token == '':
        draw.menuToken(position)
        k = getKeywordKey()
        if k == keyboard.DOWN_KEY and position < 1:
            position += 1;
        elif k == keyboard.UP_KEY and position > 0:
            position -= 1;
        elif k == keyboard.ENTER_KEY:
            player_token = 'X' if position == 0 else 'O'

    # first turn choice, default is computer
    position = 1
    while first_turn == '':
        draw.menuTurn(position)
        k = getKeywordKey()
        if k == keyboard.DOWN_KEY and position < 2:
            position += 1;
        elif k == keyboard.UP_KEY and position > 0:
            position -= 1;
        elif k == keyboard.ENTER_KEY:
            if position == 0:
                first_turn = 'player'
            elif position == 1:
                first_turn = 'computer'
            # random choice
            elif position == 2:
                if randint(0, 1) == 0:
                    first_turn = 'computer'
                else:
                    first_turn = 'player'

    # level choice, default is 3
    position = 2
    while level == 0:
        draw.menuLevel(position)
        k = getKeywordKey()
        if k == keyboard.DOWN_KEY and position < 5:
            position += 1;
        elif k == keyboard.UP_KEY and position > 0:
            position -= 1;
        elif k == keyboard.ENTER_KEY:
            level = position + 2

    draw.menuClear()
    return Game(player_token, first_turn, level)

def menuPlayAgain():
    draw.noticePlayAgain()
    while True:
        k = getKeywordKey()
        if k ==  keyboard.Y_UPPER_KEY or k == keyboard.Y_KEY or k == keyboard.ENTER_KEY:
            return True
        elif k == keyboard.N_UPPER_KEY or k == keyboard.N_KEY or k == keyboard.Q_UPPER_KEY or k == keyboard.Q_KEY:
            return False

def getHumanMoveArrow(main_game):
    position = 3
    while True:
        # draw arrow position
        draw.arrowMove(position)
        k = getKeywordKey()
        if k == keyboard.RIGHT_KEY and position < WIDTH - 1:
            position += 1
        elif k == keyboard.LEFT_KEY and position > 0:
            position -= 1
        # check the move validity
        elif k == keyboard.ENTER_KEY and main_game.validMove(position):
            break
        # quit game
        elif k == keyboard.Q_UPPER_KEY or k == keyboard.Q_KEY:
            return QUIT_GAME

    # remove detailed arrow
    draw.arrowMoveClear()
    return position

# handle SIGINT signal
def signalHandler(signum, frame):
    close()
    exit()

if __name__ == '__main__':
    signal(SIGINT, signalHandler)
    main()
    close()
