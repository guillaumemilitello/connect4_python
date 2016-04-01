'''
Created on Mar 19, 2016

@author: guillaume
'''

# define board dimensions (minimum 7x6)
WIDTH  = 7
HEIGHT = 6

class Game:

    def __init__(self, player_token = 'X', first_turn = '', level = 3):
        self.player_token = player_token
        self.computer_token = 'X' if self.player_token == 'O' else 'O'
        self.turn = first_turn
        self.level = level
        self.sum_tokens = 0
        self.board = [['' for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.winner_tokens = []

    def __eq__(self, other):
        if self.sum_tokens == other.sum_tokens:
            if self.sum_tokens == 0:
                return True
            else:
                m_board_reverse = self.reverse()
                status = True
                status_mirror = True
                for col in range(WIDTH):
                    for line in range(HEIGHT):
                        if not self.board[line][col] == other.board[line][col]:
                            status = False
                        if not m_board_reverse[line][col] == other.board[line][col]:
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
        for line in range(HEIGHT - 1, -1, -1):
            if self.board[line][move] == '':
                self.board[line][move] = token
                self.turnOther()
                self.sum_tokens += 1
                return self.won(token), line

    def makeMoveOther(self, move):
        token = self.player_token if self.turn == 'computer' else self.computer_token
        for line in range(HEIGHT - 1, -1, -1):
            if self.board[line][move] == '':
                self.board[line][move] = token
                self.turnOther()
                self.sum_tokens += 1
                return self.won(token), line

    def validMove(self, move):
        if move < 0 or move > WIDTH - 1:
            return False
        for line in range(HEIGHT - 1, -1, -1):
            if not (self.board[line][move] == 'X' or self.board[line][move] == 'O'):
                return True
        return False

    def reset(self):
        # reset board
        for col in range(WIDTH):
            for line in range(HEIGHT):
                self.board[line][col] = ''
        # reset winner tokens
        self.winner_tokens = []
        self.sum_tokens = 0
        # winner to play next game first
        self.turnOther()

    def full(self):
        if self.sum_tokens == WIDTH * HEIGHT:
            return True
        else:
            return False

    def reverse(self):
        m_board_reverse = [['' for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for col in range(WIDTH):
            for line in range(HEIGHT):
                if self.board[line][col] == 'X':
                    m_board_reverse[line][col] = 'O'
                elif self.board[line][col] == 'O':
                    m_board_reverse[line][col] = 'X'
        return m_board_reverse

    def won(self, token):
        status = False
        # check horizontal
        for col in range(WIDTH - 3):
            for line in range(HEIGHT):
                if self.board[line][col    ] == token and \
                   self.board[line][col + 1] == token and \
                   self.board[line][col + 2] == token and \
                   self.board[line][col + 3] == token:
                    self.winner_tokens.append([line, col    ])
                    self.winner_tokens.append([line, col + 1])
                    self.winner_tokens.append([line, col + 2])
                    self.winner_tokens.append([line, col + 3])
                    status = True
        # check vertical
        for col in range(WIDTH):
            for line in range(HEIGHT - 3):
                if self.board[line    ][col] == token and \
                   self.board[line + 1][col] == token and \
                   self.board[line + 2][col] == token and \
                   self.board[line + 3][col] == token:
                    self.winner_tokens.append([line    , col])
                    self.winner_tokens.append([line + 1, col])
                    self.winner_tokens.append([line + 2, col])
                    self.winner_tokens.append([line + 3, col])
                    status = True
        # check diagonals
        for col in range(3, WIDTH):
            for line in range(HEIGHT - 3):
                if self.board[line    ][col    ] == token and \
                   self.board[line + 1][col - 1] == token and \
                   self.board[line + 2][col - 2] == token and \
                   self.board[line + 3][col - 3] == token:
                    self.winner_tokens.append([line    , col    ])
                    self.winner_tokens.append([line + 1, col - 1])
                    self.winner_tokens.append([line + 2, col - 2])
                    self.winner_tokens.append([line + 3, col - 3])
                    status = True
        for col in range(WIDTH - 3):
            for line in range(HEIGHT - 3):
                if self.board[line    ][col    ] == token and \
                   self.board[line + 1][col + 1] == token and \
                   self.board[line + 2][col + 2] == token and \
                   self.board[line + 3][col + 3] == token:
                    self.winner_tokens.append([line    , col    ])
                    self.winner_tokens.append([line + 1, col + 1])
                    self.winner_tokens.append([line + 2, col + 2])
                    self.winner_tokens.append([line + 3, col + 3])
                    status = True
        return status

class PredefinedGame(Game):

    def __init__(self, predefined_board = [['' for _ in range(WIDTH)] for _ in range(HEIGHT)], move = 0):
        Game.__init__(self)
        sum_predefined_tokens = 0
        for col in range(WIDTH):
            for line in range(HEIGHT):
                if predefined_board[line][col] == 'X' or predefined_board[line][col] == 'O':
                    sum_predefined_tokens += 1
        self.sum_tokens = sum_predefined_tokens
        self.board = predefined_board
        self.move = move


def mirrorBoard(board):
    m_board_mirror = [['' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for col in range(WIDTH):
        for line in range(HEIGHT):
            m_board_mirror[line][col] = board[line][WIDTH - 1 - col]
    return m_board_mirror
