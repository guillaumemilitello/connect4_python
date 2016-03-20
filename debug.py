'''
Created on Mar 20, 2016

@author: guillaume
'''

import board

filename = 'connect4.txt'
filedata = 'data.txt'
f = open(filename, 'w')
f.close

def writeMove(m_board, token, turn, scores, step):
    f = open(filename, 'a')
    f.write('token:%s turn:%s step:%d\n' %(token, turn, step))
    for col in range(board.width):
        f.write('%s\t' %scores[col])
    f.write('\n')
    for line in range(board.height):
        for col in range(board.width):
            if not (m_board[line][col] == 'X' or m_board[line][col] == 'O'):
                f.write('\t')
            else:
                f.write('%s\t' %m_board[line][col])
        f.write('\n')
    f.write('\n')
    f.close()
    
def writeMoveComplete(m_board, token, turn, score, potential_scores, step):
    f = open(filename, 'a')
    f.write('token:%s turn:%s step:%d\n' %(token, turn, step))
    f.write('%s\n' %score)
    for col in range(board.width):
        f.write('%s\t' %potential_scores[col])
    f.write('\n')
    for line in range(board.height):
        for col in range(board.width):
            if not (m_board[line][col] == 'X' or m_board[line][col] == 'O'):
                f.write('\t')
            else:
                f.write('%s\t' %m_board[line][col])
        f.write('\n')
    f.write('\n')
    f.close()
    
def saveResult(m_board, scores):
    f = open(filedata, 'a')
    for line in range(board.height):
        for col in range(board.width):
            if not (m_board[line][col] == 'X' or m_board[line][col] == 'O'):
                f.write(' ')
            else:
                f.write('%s' %m_board[line][col])
    for line in range(board.height):
        f.write('/%s' %scores[line])
    f.write('\n')
    f.close()

