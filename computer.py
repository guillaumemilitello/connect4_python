'''
Created on Mar 12, 2016

@author: guillaume
'''

from copy import deepcopy
from random import choice
import board
import debug

def getComputerBestMove(m_board, computer_token):
    score_moves = turnScore(m_board, computer_token, 'computer', 4)
    debug.saveResult(m_board, score_moves)
    score_max = max(score_moves)
    best_moves = []
    for i in range(board.width):
        if score_moves[i] == score_max:
            best_moves.append(i)
    return choice(best_moves)

def turnScore(m_board, token, turn, step):
    scores = [0] * board.width
    # utile board full ?
    if step == 0:
        return scores

    for move in range(board.width):
        # save the state of the board
        copy_board = deepcopy(m_board)
        scores[move] = moveScore(copy_board, token, turn, move, step)

    debug.writeMove(m_board, token, turn, scores, step)

    return scores

def moveScore(m_board, token, turn, move, step):

    # check if the move is valid
    if not board.isValidMove(m_board, move):
        return -1000

    next_token = 'X' if token == 'O' else 'O'
    next_turn = 'player' if turn == 'computer' else 'computer'

    # trace the move on the saved state board
    board.makeMove(m_board, token, move)
    
    # winning move
    if board.isWinner(m_board, token):
        return 1000

    # score of this unique move
    score = board.scoreStatus(m_board, token)
    
    # check the next step
    potential_moves = turnScore(m_board, next_token, next_turn, step - 1)
    best_next_move = max(potential_moves[i] for i in range(board.width))
    
    #debug.writeMoveComplete(m_board, token, turn, score, potential_moves, step)
    
    return (score - 2*best_next_move)/3
