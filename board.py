'''
Created on Mar 19, 2016

@author: guillaume
'''

import draw

width = 7
height = 6
col_width = 6
col_height = 3

def makeMove(m_board, token, move):
    for line in range(height - 1, -1, -1):
        if m_board[line][move] == '':
            m_board[line][move] = token
            return line

def isValidMove(m_board, move):
    if move < 0 or move > width - 1:
        return False

    for line in range(height - 1, -1, -1):
        if not (m_board[line][move] == 'X' or m_board[line][move] == 'O'):
            return True

    return False

def isBoardFull(m_board):
    for col in range(width):
        for line in range(height):
            if not(m_board[line][col] == 'X' or m_board[line][col] == 'O'):
                return False
    return True

def isWinner(m_board, token, draw_token=False):
    # check horizontal
    for col in range(width - 3):
        for line in range(height):
            if m_board[line][col  ] == token and m_board[line][col + 1] == token and \
               m_board[line][col + 2] == token and m_board[line][col + 3] == token:
                if draw_token:
                    draw.boardTokenBold(line, col, token)
                    draw.boardTokenBold(line, col + 1, token)
                    draw.boardTokenBold(line, col + 2, token)
                    draw.boardTokenBold(line, col + 3, token)
                return True

    # check vertical
    for col in range(width):
        for line in range(height - 3):
            if m_board[line  ][col] == token and m_board[line + 1][col] == token and \
               m_board[line + 2][col] == token and m_board[line + 3][col] == token:
                if draw_token:
                    draw.boardTokenBold(line, col, token)
                    draw.boardTokenBold(line + 1, col, token)
                    draw.boardTokenBold(line + 2, col, token)
                    draw.boardTokenBold(line + 3, col, token)
                return True

    # check diagonals
    for col in range(3, width):
        for line in range(height - 3):
            if m_board[line  ][col  ] == token and m_board[line + 1][col - 1] == token and \
               m_board[line + 2][col - 2] == token and m_board[line + 3][col - 3] == token:
                if draw_token:
                    draw.boardTokenBold(line, col, token)
                    draw.boardTokenBold(line + 1, col - 1, token)
                    draw.boardTokenBold(line + 2, col - 2, token)
                    draw.boardTokenBold(line + 3, col - 3, token)
                return True
    
    for col in range(width - 3):
        for line in range(height - 3):
            if m_board[line  ][col  ] == token and m_board[line + 1][col + 1] == token and \
               m_board[line + 2][col + 2] == token and m_board[line + 3][col + 3] == token:
                if draw_token:
                    draw.boardTokenBold(line, col, token)
                    draw.boardTokenBold(line + 1, col + 1, token)
                    draw.boardTokenBold(line + 2, col + 2, token)
                    draw.boardTokenBold(line + 3, col + 3, token)
                return True

    return False

def scoreStatus(m_board, token):
    score = 0
    # check horizontal
    for col in range(width - 3):
        for line in range(height):
            if m_board[line][col] == token and m_board[line][col + 1] == token and m_board[line][col + 2] == token and m_board[line][col + 3] == '':
                # XXX-
                # ???-
                if line < height - 1 and m_board[line + 1][col + 3] == '':
                    score += 100
                # XXX-
                # ????
                    score += 200

    for col in range(width - 3):
        for line in range(height):
            if m_board[line][col] == '' and m_board[line][col + 1] == token and m_board[line][col + 2] == token and m_board[line][col + 3] == token:
                # -XXX
                # -???
                if line < height - 1 and m_board[line + 1][col] == '':
                    score += 100
                # -XXX
                # ????
                    score += 200

    for col in range(width - 3):
        for line in range(height):
            if m_board[line][col] == token and m_board[line][col + 1] == token and m_board[line][col + 2] == token and m_board[line][col + 3] == '':
                # XXX-
                # ???-
                if line < height - 1 and m_board[line + 1][col + 3] == '':
                    score += 100
                # XXX-
                # ????
                    score += 200

    for col in range(width - 3):
        for line in range(height):
            if m_board[line][col] == token and m_board[line][col + 1] == '' and m_board[line][col + 2] == token and m_board[line][col + 3] == token:
                # X-XX
                # ?-??
                if line < height - 1 and m_board[line + 1][col + 1] == '':
                    score += 100
                # X-XX
                # ????
                    score += 200
    
    for col in range(width - 3):
        for line in range(height):
            if m_board[line][col] == token and m_board[line][col + 1] == token and m_board[line][col + 2] == '' and m_board[line][col + 3] == token:
                # XX-X
                # ??-?
                if line < height - 1 and m_board[line + 1][col + 2] == '':
                    score += 100
                # XX-X
                # ????
                    score += 200

    # --XX-
    for col in range(width - 4):
        for line in range(height):
            if m_board[line][col    ] == ''    and m_board[line][col + 1] == ''    and \
               m_board[line][col + 2] == token and m_board[line][col + 3] == token and \
               m_board[line][col + 4] == '':
                score += 50
    # -XX--
    for col in range(width - 4):
        for line in range(height):
            if m_board[line][col    ] == ''    and m_board[line][col + 1] == token and \
               m_board[line][col + 2] == token and m_board[line][col + 3] == ''    and \
               m_board[line][col + 4] == '':
                score += 50
    # check vertical
    # -
    # X
    # X
    # X
    for col in range(width):
        for line in range(height - 3):
            if m_board[line][col] == '' and m_board[line + 1][col] == token and m_board[line + 2][col] == token and m_board[line + 3][col] == token:
                score += 200

    # check diagonals
    for col in range(width - 3):
        for line in range(height - 3):
            if m_board[line][col] == '' and m_board[line + 1][col + 1] == token and m_board[line + 2][col + 2] == token and m_board[line + 3][col + 3] == token:
                # -
                # -X
                # ??X
                # ???X
                if m_board[line + 1][col] == '':
                    score += 100
                # -
                # ?X
                # ??X
                # ???X
                else:
                    score += 200

    for col in range(width - 3):
        for line in range(height - 3):
            if m_board[line][col] == token and m_board[line + 1][col + 1] == token and m_board[line + 2][col + 2] == token and m_board[line + 3][col + 3] == '':
                # X
                # ?X
                # ??X
                # ???-
                # ???-
                if line + 3 < height - 1 and m_board[line + 1][col + 3] == '':
                    score += 100
                # X
                # ?X
                # ??X
                # ???-
                # ????
                else:
                    score += 200

    for col in range(3, width):
        for line in range(height - 3):
            if m_board[line][col] == token and m_board[line + 1][col - 1] == token and m_board[line + 2][col - 2] == token and m_board[line + 3][col - 3] == '':
                #    X
                #   X?
                #  X??
                # -???
                # -???
                if line + 3 < height - 1 and m_board[line + 3][col] == '':
                    score += 100
                #    -
                #   X-
                #  X??
                # X???
                else:
                    score += 200

    for col in range(3, width):
        for line in range(height - 3):
            if m_board[line][col] == token and m_board[line + 1][col - 1] == token and m_board[line + 2][col - 2] == '' and m_board[line + 3][col - 3] == token:
                #    X
                #   X?
                #  -??
                # X-??
                if m_board[line + 3][col - 2] == '':
                    score += 100
                #    X
                #   X?
                #  -??
                # X???
                else:
                    score += 200

    for col in range(3, width):
        for line in range(height - 3):
            if m_board[line][col] == token and m_board[line + 1][col - 1] == '' and m_board[line + 2][col - 2] == token and m_board[line + 3][col - 3] == token:
                #    X
                #   -?
                #  X-?
                # X???
                if m_board[line + 2][col - 1] == '':
                    score += 100
                #    X
                #   -?
                #  X??
                # X???
                else:
                    score += 200

    return score
