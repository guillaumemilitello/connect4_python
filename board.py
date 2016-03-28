'''
Created on Mar 19, 2016

@author: guillaume
'''

width = 7
height = 6
center = width / 2

# draw settings
col_width = 6
col_height = 3

class Game:

    def __init__(self, player_token = 'X', first_turn = '', level = 3):
        self.player_token = player_token
        self.computer_token = 'X' if self.player_token == 'O' else 'O'
        self.turn = first_turn
        self.level = level
        self.sum_tokens = 0
        self.m_board = [['' for _ in range(width)] for _ in range(height)]
        self.winner_tokens = []

    def token(self):
        if self.turn == 'player':
            return self.player_token
        else:
            return self.computer_token

    def tokenOther(self):
        if self.turn == 'player':
            return self.computer_token
        else:
            return self.player_token
    
    def turnOther(self):
        self.turn = 'player' if self.turn == 'computer' else 'computer'

    def makeMove(self, move):
        token = self.player_token if self.turn == 'player' else self.computer_token
        for line in range(height - 1, -1, -1):
            if self.m_board[line][move] == '':
                self.m_board[line][move] = token
                self.turnOther()
                self.sum_tokens += 1
                return self.won(token), line

    def makeMoveOther(self, move):
        token = self.player_token if self.turn == 'computer' else self.computer_token
        for line in range(height - 1, -1, -1):
            if self.m_board[line][move] == '':
                self.m_board[line][move] = token
                self.turnOther()
                self.sum_tokens += 1
                return self.won(token), line

    def validMove(self, move):
        if move < 0 or move > width - 1:
            return False
        for line in range(height - 1, -1, -1):
            if not (self.m_board[line][move] == 'X' or self.m_board[line][move] == 'O'):
                return True
        return False

    def reset(self):
        # reset board
        for col in range(width):
            for line in range(height):
                self.m_board[line][col] = ''
        # reset winner tokens
        self.winner_tokens = []
        self.sum_tokens = 0
        # winner to play next game first
        self.turnOther()

    def full(self):
        if self.sum_tokens == width * height:
            return True
        else:
            return False

    def won(self, token):
        status = False
        # check horizontal
        for col in range(width - 3):
            for line in range(height):
                if self.m_board[line][col    ] == token and \
                   self.m_board[line][col + 1] == token and \
                   self.m_board[line][col + 2] == token and \
                   self.m_board[line][col + 3] == token:
                    self.winner_tokens.append([line, col    ])
                    self.winner_tokens.append([line, col + 1])
                    self.winner_tokens.append([line, col + 2])
                    self.winner_tokens.append([line, col + 3])
                    status = True
        # check vertical
        for col in range(width):
            for line in range(height - 3):
                if self.m_board[line    ][col] == token and \
                   self.m_board[line + 1][col] == token and \
                   self.m_board[line + 2][col] == token and \
                   self.m_board[line + 3][col] == token:
                    self.winner_tokens.append([line    , col])
                    self.winner_tokens.append([line + 1, col])
                    self.winner_tokens.append([line + 2, col])
                    self.winner_tokens.append([line + 3, col])
                    status = True
        # check diagonals
        for col in range(3, width):
            for line in range(height - 3):
                if self.m_board[line    ][col    ] == token and \
                   self.m_board[line + 1][col - 1] == token and \
                   self.m_board[line + 2][col - 2] == token and \
                   self.m_board[line + 3][col - 3] == token:
                    self.winner_tokens.append([line    , col    ])
                    self.winner_tokens.append([line + 1, col - 1])
                    self.winner_tokens.append([line + 2, col - 2])
                    self.winner_tokens.append([line + 3, col - 3])
                    status = True
        for col in range(width - 3):
            for line in range(height - 3):
                if self.m_board[line    ][col    ] == token and \
                   self.m_board[line + 1][col + 1] == token and \
                   self.m_board[line + 2][col + 2] == token and \
                   self.m_board[line + 3][col + 3] == token:
                    self.winner_tokens.append([line    , col    ])
                    self.winner_tokens.append([line + 1, col + 1])
                    self.winner_tokens.append([line + 2, col + 2])
                    self.winner_tokens.append([line + 3, col + 3])
                    status = True
        return status

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

def isWinner(m_board, token):
    # check horizontal
    for col in range(width - 3):
        for line in range(height):
            if m_board[line][col  ] == token and m_board[line][col + 1] == token and \
               m_board[line][col + 2] == token and m_board[line][col + 3] == token:
                return True

    # check vertical
    for col in range(width):
        for line in range(height - 3):
            if m_board[line  ][col] == token and m_board[line + 1][col] == token and \
               m_board[line + 2][col] == token and m_board[line + 3][col] == token:
                return True

    # check diagonals
    for col in range(3, width):
        for line in range(height - 3):
            if m_board[line  ][col  ] == token and m_board[line + 1][col - 1] == token and \
               m_board[line + 2][col - 2] == token and m_board[line + 3][col - 3] == token:
                return True
    
    for col in range(width - 3):
        for line in range(height - 3):
            if m_board[line  ][col  ] == token and m_board[line + 1][col + 1] == token and \
               m_board[line + 2][col + 2] == token and m_board[line + 3][col + 3] == token:
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
