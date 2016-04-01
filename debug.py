'''
Created on Mar 20, 2016

@author: guillaume
'''

from game import WIDTH, HEIGHT
from computer import MOVE_INVALID, MOVE_WIN, MOVE_LOOSE, MOVE_WIN_2, MOVE_FORCE, MOVE_TRAP

filename = 'connect4.txt'
f = open(filename, 'w')
f.close

def writeBestMoves(string, scores, best_moves):
    dbg_str = string
    for move in best_moves:
        if scores[move] == MOVE_INVALID:
            dbg_str += 'I (%d)\t' %move
        elif scores[move] == MOVE_WIN:
            dbg_str += 'W (%d)\t' %move
        elif scores[move] == MOVE_LOOSE:
            dbg_str += 'L (%d)\t' %move
        elif scores[move] == MOVE_FORCE:
            dbg_str += 'F (%d)\t' %move
        elif scores[move] == MOVE_TRAP:
            dbg_str += 'T (%d)\t' %move
        elif scores[move] == MOVE_WIN_2:
            dbg_str += 'W2 (%d)\t' %move
        else:
            dbg_str += '%d (%d)\t' %(scores[move], move)
    writeString(dbg_str)

def writeMoveScores(string, move_scores):
    writeString(string)
    for scores in move_scores:
        dbg_str = 'turn score - move:%d      - \t' %scores[0]
        for move in range(WIDTH):
            if scores[1][move] == MOVE_INVALID:
                dbg_str += 'I\t'
            elif scores[1][move] == MOVE_WIN:
                dbg_str += 'W\t'
            elif scores[1][move] == MOVE_LOOSE:
                dbg_str += 'L\t'
            elif scores[1][move] == MOVE_FORCE:
                dbg_str += 'F\t' %move
            elif scores[1][move] == MOVE_TRAP:
                dbg_str += 'T\t' %move
            elif scores[1][move] == MOVE_WIN_2:
                dbg_str += 'W2\t' %move
            else:
                dbg_str += '%d\t' %scores[1][move]
        writeString(dbg_str)

def writeScores(string, scores):
    dbg_str = string
    for move in range(WIDTH):
        if scores[move] == MOVE_INVALID:
            dbg_str += 'I\t'
        elif scores[move] == MOVE_WIN:
            dbg_str += 'W\t'
        elif scores[move] == MOVE_LOOSE:
            dbg_str += 'L\t'
        elif scores[move] == MOVE_FORCE:
            dbg_str += 'F\t' %move
        elif scores[move] == MOVE_TRAP:
            dbg_str += 'T\t' %move
        elif scores[move] == MOVE_WIN_2:
            dbg_str += 'W2\t' %move
        else:
            dbg_str += '%d\t' %scores[move]
    writeString(dbg_str)


def writeBoard(board):
    f = open(filename, 'a')
    for line in range(HEIGHT):
        for col in range(WIDTH):
            f.write('%s\t' %board[line][col])
        f.write('\n')
    f.write('\n')
    f.close()

def writeString(string):
    f = open(filename, 'a')
    f.write(string)
    f.write('\n')
    f.close()
