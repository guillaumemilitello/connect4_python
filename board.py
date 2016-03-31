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

    def __eq__(self, other):
        if self.sum_tokens == other.sum_tokens:
            if self.sum_tokens == 0:
                return True
            else:
                m_board_reverse = self.reverse()
                status = True
                status_mirror = True
                for col in range(width):
                    for line in range(height):
                        if not self.m_board[line][col] == other.m_board[line][col]:
                            status = False
                        if not m_board_reverse[line][col] == other.m_board[line][col]:
                            status_mirror = False
                        if not status and not status_mirror:
                            break
                    if not status and not status_mirror:
                        break
                return status ^ status_mirror
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

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

    def reverse(self):
        m_board_reverse = [['' for _ in range(width)] for _ in range(height)]
        for col in range(width):
            for line in range(height):
                if self.m_board[line][col] == 'X':
                    m_board_reverse[line][col] = 'O'
                elif self.m_board[line][col] == 'O':
                    m_board_reverse[line][col] = 'X'
        return m_board_reverse

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

class PredefinedGame(Game):

    def __init__(self, m_predefined_board = [['' for _ in range(width)] for _ in range(height)], move = 0):
        Game.__init__(self)
        sum_predefined_tokens = 0
        for col in range(width):
            for line in range(height):
                if m_predefined_board[line][col] == 'X' or m_predefined_board[line][col] == 'O':
                    sum_predefined_tokens += 1
        self.sum_tokens = sum_predefined_tokens
        self.m_board = m_predefined_board
        self.move = move


def mirrorBoard(m_board):
    m_board_mirror = [['' for _ in range(width)] for _ in range(height)]
    for col in range(width):
        for line in range(height):
            m_board_mirror[line][col] = m_board[line][width - 1 - col]
    return m_board_mirror
