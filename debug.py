'''
Created on Mar 20, 2016

@author: guillaume
'''

import board
import computer

filename = 'connect4.txt'
f = open(filename, 'w')
f.close

def scoresBestMoves(string, scores, best_moves):
    dbg_str = string
    for move in best_moves:
        if scores[move] == computer.invalid_move:
            dbg_str += 'I (%d)\t' %move
        elif scores[move] == computer.winning_move:
            dbg_str += 'W (%d)\t' %move
        elif scores[move] == computer.loosing_move:
            dbg_str += 'L (%d)\t' %move
        else:
            dbg_str += '%d (%d)\t' %(scores[move], move)
    writeString(dbg_str)
    writeString('-' * 55)

def deepScores(string, deep_scores):
    writeString(string)
    for scores in deep_scores:
        dbg_str = 'turn score - move:%d      - \t' %scores[0]
        for move in range(board.width):
            if scores[1][move] == computer.invalid_move:
                dbg_str += 'I\t'
            elif scores[1][move] == computer.winning_move:
                dbg_str += 'W\t'
            elif scores[1][move] == computer.loosing_move:
                dbg_str += 'L\t'
            else:
                dbg_str += '%d\t' %scores[1][move]
        writeString(dbg_str)

def scores(string, scores):
    dbg_str = string
    for move in range(board.width):
        if scores[move] == computer.invalid_move:
            dbg_str += 'I\t'
        elif scores[move] == computer.winning_move:
            dbg_str += 'W\t'
        elif scores[move] == computer.loosing_move:
            dbg_str += 'L\t'
        else:
            dbg_str += '%d\t' %scores[move]
    writeString(dbg_str)


def writeBoard(m_board):
    f = open(filename, 'a')
    for line in range(board.height):
        for col in range(board.width):
            if not (m_board[line][col] == 'X' or m_board[line][col] == 'O'):
                f.write('\t')
            else:
                f.write('%s\t' %m_board[line][col])
        f.write('\n')
    f.write('\n')
    f.close()

def writeString(string):
    f = open(filename, 'a')
    f.write(string)
    f.write('\n')
    f.close()
