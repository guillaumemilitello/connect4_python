'''
Created on Apr 4, 2016

@author: guillaume
'''

import game
import saved_games
from time import clock
from game import WIDTH, HEIGHT
from copy import deepcopy
from random import choice
from multiprocessing import Process, Queue

# debug traces on file and verbose level (0 = no trace)
DEBUG = 1

# number of deeper moves to look for (max : WIDTH)
DEEP_MOVES_MAX = WIDTH

# multiprocessing support for calculating computer's moves
MULTIPROCESS = True

# game evaluation coefficients
MOVE_INVALID = -999999
MOVE_WIN     =     100
MOVE_LOOSE   =    -100
MOVE_WIN_2   =      40
MOVE_FORCE   =      10
MOVE_TRAP    =       5

if DEBUG:
    import debug

class turnScoreThread (Process):
    def __init__(self, move, game, scores_queue, processing_times_queue):
        Process.__init__(self)
        self.move = move
        self.game = game
        self.scores_queue = scores_queue
        self.processing_times_queue = processing_times_queue

    def run(self):
        start_time = clock()
        self.scores_queue.put((self.move, turnScore(self.game)))
        self.processing_times_queue.put(clock() - start_time)
        return

def getComputerBestMove(main_game):

    global processing_time, start_time
    processing_time = 0
    start_time = clock()

    if MULTIPROCESS:
        global main_level
        main_level = main_game.level

    # adjust write debug level
    global DEBUG_LEVEL
    DEBUG_LEVEL = main_game.level + 1 - DEBUG

    # compare with pre-registered moves
    for game in saved_games.startup_games:
        if main_game == game:

            if DEBUG_LEVEL <= main_game.level:
                debug.writeString('-'*45 + ' pre-registered game - turn:computer')
                debug.writeBoard(game.board)
                debug.writeString('final best move          - (%d)\t' %game.move)
            return game.move, 0

    # get the score of the different possible moves and the choose the best one
    scores = turnScore(main_game)
    best_moves = [move for move, x in enumerate(scores) if x == max(scores)]

    # update processing time counter
    processing_time += clock() - start_time

    # if several move scores 0
    if all([scores[move] == 0 for move in best_moves]) and len(best_moves) > 1:

        if DEBUG_LEVEL <= main_game.level:
            debug.writeBestMoves('final best moves center  - \t', scores, best_moves)

        board_center = WIDTH / 2
        if board_center in best_moves:
            return board_center, processing_time
        elif board_center - 1 in best_moves and board_center + 1 in best_moves:
            return choice([board_center - 1, board_center + 1]), processing_time
        elif board_center - 1 in best_moves:
            return board_center - 1, processing_time
        elif board_center + 1 in best_moves:
            return board_center + 1, processing_time
        elif board_center - 2 in best_moves and board_center + 2 in best_moves:
            return choice([board_center - 2, board_center + 2]), processing_time
        elif board_center - 2 in best_moves:
            return board_center - 2, processing_time
        elif board_center + 2 in best_moves:
            return board_center + 2, processing_time

    if DEBUG_LEVEL <= main_game.level:
        debug.writeBestMoves('final best moves         - \t', scores, best_moves)

    return choice(best_moves), processing_time


def turnScore(game):
    
    global processing_time, start_time

    scores = [0] * WIDTH

    if DEBUG_LEVEL <= game.level:
        debug.writeString('-' * 55 + ' turnScore - turn:%s' %game.turn)
        debug.writeBoard(game.board)

    # store the evaluation scores for deeper level moves
    if game.level > 1:
        scores_t = []
        scores_t_others = []

    scores_other = [0] * WIDTH
    copy_games = []

    for move in range(WIDTH):
        # save the state of the current game
        copy_game = deepcopy(game)
        copy_games.append(copy_game)
        scores[move], scores_other[move] = moveScore(copy_game, move)

        if game.level > 1:
            scores_t.append((scores[move], move))
            scores_t_others.append((scores_other[move], move))

        # ultimate winning move
        if scores[move] == MOVE_WIN:
            scores = [MOVE_INVALID] * WIDTH
            scores[move] = MOVE_WIN

            if DEBUG_LEVEL <= game.level:
                debug.writeScores('game scores       - l:%d - \t' %game.level, scores)

            return scores
    
    # check for valid moves
    valid_moves = []
    for move in range(WIDTH):
        if not scores[move] == MOVE_INVALID and scores_other[move] == MOVE_INVALID:
            valid_moves.append(move)
    if len(valid_moves) == 1:
        return scores

    # check for winning opponent move
    for move in range(WIDTH):
        if scores_other[move] == MOVE_WIN:
            scores = [MOVE_LOOSE] * WIDTH
            scores[move] = MOVE_FORCE

            if DEBUG_LEVEL <= game.level:
                debug.writeScores('game scores       - l:%d - \t' %game.level, scores)

            return scores

    if DEBUG_LEVEL <= game.level:
        debug.writeScores('game scores       - l:%d - \t' %game.level, scores)
        debug.writeScores('game scores other - l:%d - \t' %game.level,scores_other)

    if game.level > 1:
        # sort the previous scores
        all_scores = scores_t + scores_t_others
        all_scores.sort(key = lambda x: x[0], reverse=True)

        moves = []
        # study only the best cases
        for score in all_scores:
            if not score[1] in moves and not score[0] == MOVE_INVALID:
                moves.append(score[1])
            if len(moves) == DEEP_MOVES_MAX:
                break

        # don't play the others moves
        for move in range(WIDTH):
            if move not in moves:
                scores[move] = MOVE_INVALID

        if DEBUG_LEVEL <= game.level:
            # create array for saving all moves
            move_scores_dbg = []
            debug.writeScores('turnScore          - l:%d - \t' %game.level, scores)

        if MULTIPROCESS and  game.level == main_level:

            # return the best score of the calculation level - 1
            threads = []
            scores_queue = Queue()
            processing_times_queue = Queue()
            scores_threads = deepcopy(scores)
            processing_times_thread = [0] * WIDTH

            for move in moves:
                copy_games[move].level -= 1
                threads.append(turnScoreThread(move, copy_games[move], scores_queue, processing_times_queue))
                

            # reset start time before starting the threads
            processing_time += clock() - start_time

            for t in threads:
                if DEBUG_LEVEL <= t.game.level:
                    debug.writeString('-' * 55 + ' l:%d - m:%d' %(t.game.level, move))
                t.start()

            for t in threads:
                t.join()

            for t in threads:
                scores_thread = scores_queue.get()
                scores_threads[scores_thread[0]] = scores_thread[1]
                processing_times_thread[scores_thread[0]] = processing_times_queue.get()
                scores[scores_thread[0]] -= max(scores_thread[1])

                if DEBUG_LEVEL <= game.level:
                    move_scores_dbg.append((t.move, scores_thread[1]))

            # update the processing time
            processing_time += max(processing_times_thread)
            start_time = clock()

            if DEBUG_LEVEL <= game.level:
                debug.writeMoveScores('-' * 55, move_scores_dbg)

        else:
            # return the best score of the calculation level - 1
            for move in moves:

                copy_games[move].level -= 1
    
                if DEBUG_LEVEL <= copy_games[move].level:
                    debug.writeString('-' * 55 + ' l:%d - m:%d' %(game.level - 1, move))

                move_scores = turnScore(copy_games[move])
                scores[move] -= max(move_scores)

                if DEBUG_LEVEL <= game.level:
                    move_scores_dbg.append((move, move_scores))

            if DEBUG_LEVEL <= game.level:
                debug.writeMoveScores('-' * 55, move_scores_dbg)


    if DEBUG_LEVEL <= game.level:
        debug.writeScores('final scores             - \t', scores)

    return scores

def moveScore(game, move):

    # check for invalid move
    if not game.validMove(move):
        return MOVE_INVALID, MOVE_INVALID

    # evaluate the actual game for reference score
    player_base_score = boardEvaluation(game.board, game.token())
    opponent_base_score = boardEvaluation(game.board, game.tokenOther())

    # copy the actual game for opponent check
    game_opponent = deepcopy(game)

    # generate move for the current player
    winner_move, _ = game.makeMove(move)

    # check for a winning move
    if winner_move:
        return MOVE_WIN, MOVE_LOOSE

    # mock an opponent move for the current game 
    winner_move, _ = game_opponent.makeMoveOther(move)

    if winner_move:
        return MOVE_LOOSE, MOVE_WIN

    # evaluate the current move
    player_score = boardEvaluation(game.board, game.tokenOther())

    # evaluate the mock opponent move
    opponent_score = boardEvaluation(game_opponent.board, game_opponent.token())

    return player_score - player_base_score, opponent_score - opponent_base_score

def boardEvaluation(board, token):

    evaluation_board = deepcopy(board)

    def boardScoreEvaluation():
        score = 0
        for col in range(WIDTH):
            for line in range(HEIGHT):
                # trap
                if evaluation_board[line][col] == 'T':
                    # winning within 2 move
                    if line < HEIGHT - 1 and evaluation_board[line + 1][col] == 'F':
                        score += MOVE_WIN_2
                    else:
                        score += MOVE_TRAP
                # forced move
                elif evaluation_board[line][col] == 'F':
                    score += MOVE_FORCE
                # winning move
                elif evaluation_board[line][col] == 'W':
                    return MOVE_WIN
        return score

    def horizontalEvaluation(board, token):
        for col in range(WIDTH - 3):
            for line in range(HEIGHT):
                if board[line][col] == token:
                    # XXX- XX-X
                    if board[line][col + 1] == token:
                        # XXX-
                        if board[line][col + 2] == token and \
                           board[line][col + 3] == '':
                            if line < HEIGHT - 1:
                                # XXX-
                                # ???-
                                if board[line + 1][col + 3] == '':
                                    evaluation_board[line][col + 3] = 'T'
                                    #score += MOVE_TRAP
                                # XXX-
                                # ????
                                else:
                                    evaluation_board[line][col + 3] = 'F'
                                    #score += MOVE_FORCE
                            # XXX-
                            else:
                                evaluation_board[line][col + 3] = 'F'
                                #score += MOVE_FORCE
                        # XX-X
                        elif board[line][col + 2] == '' and \
                             board[line][col + 3] == token:
                            if line < HEIGHT - 1:
                                # XX-X
                                # ??-?
                                if board[line + 1][col + 2] == '':
                                    evaluation_board[line][col + 2] = 'T'
                                    #score += MOVE_TRAP
                                # XX-X
                                # ????
                                else:
                                    evaluation_board[line][col + 2] = 'F'
                                    #score += MOVE_FORCE
                            # XX-X
                            else:
                                evaluation_board[line][col + 2] = 'F'
                                #score += MOVE_FORCE
                    # X-XX
                    elif board[line][col + 1] == ''    and \
                         board[line][col + 2] == token and \
                         board[line][col + 3] == token:
                        if line < HEIGHT - 1:
                            # X-XX
                            # ?-??
                            if board[line + 1][col + 1] == '':
                                evaluation_board[line][col + 1] = 'T'
                                #score += MOVE_TRAP
                            # X-XX
                            # ????
                            else:
                                evaluation_board[line][col + 1] = 'F'
                                #score += MOVE_FORCE
                        # X-XX
                        else:
                            evaluation_board[line][col + 1] = 'F'
                            #score += MOVE_FORCE
                # -XXX -XXX-
                elif board[line][col] == '' and \
                     board[line][col + 1] == token and \
                     board[line][col + 2] == token and \
                     board[line][col + 3] == token:
                    if line < HEIGHT - 1:
                        # -XXX
                        # -???
                        if board[line + 1][col] == '':
                            evaluation_board[line][col] = 'T'
                            #score += MOVE_TRAP
                        # -XXX-
                        # ?????
                        elif col < WIDTH - 4 and board[line][col + 4] == '' and \
                             not board[line + 1][col + 4] == '':
                            evaluation_board[line][col    ] = 'W'
                            evaluation_board[line][col + 4] = 'W'
                            #score += MOVE_WIN
                        # -XXX
                        # ????
                        else:
                            evaluation_board[line][col] = 'F'
                            #score += MOVE_FORCE
                    # -XXX-
                    elif col < WIDTH - 4 and board[line][col + 4] == '':
                        evaluation_board[line][col    ] = 'W'
                        evaluation_board[line][col + 4] = 'W'
                        #score += MOVE_WIN
                    # -XXX
                    else:
                        evaluation_board[line][col] = 'T'
                        #score += MOVE_FORCE

    def verticalEvaluation(board, token):
        for col in range(WIDTH):
            for line in range(HEIGHT - 3):
                # -
                # X
                # X
                # X
                if board[line    ][col] == ''    and \
                   board[line + 1][col] == token and \
                   board[line + 2][col] == token and \
                   board[line + 3][col] == token:
                    evaluation_board[line][col] = 'F'
                    # score += MOVE_FORCE
    
    def diagonalEvaluation(board, token):
        for col in range(WIDTH - 3):
            for line in range(HEIGHT - 3):
                # X    X    X
                # ?X   ?X   ?-
                # ??X  ??-  ??X
                # ???- ???X ???X
                if board[line][col] == token :
                    # X    X
                    # ?X   ?X
                    # ??X  ??-
                    # ???- ???X
                    if board[line + 1][col + 1] == token:
                        # X
                        # ?X
                        # ??X
                        # ???-
                        if board[line + 2][col + 2] == token and \
                           board[line + 3][col + 3] == '':
                            if line + 4 < HEIGHT - 1:
                                # X
                                # ?X
                                # ??X
                                # ???-
                                # ???-
                                if board[line + 4][col + 3] == '':
                                    evaluation_board[line + 3][col + 3] = 'T'
                                    #score += MOVE_TRAP
                                # X
                                # ?X
                                # ??X
                                # ???-
                                # ????
                                else:
                                    evaluation_board[line + 3][col + 3] = 'F'
                                    #score += MOVE_FORCE 
                            # X
                            # ?X
                            # ??X
                            # ???-
                            else:
                                evaluation_board[line + 3][col + 3] = 'F'
                                #score += MOVE_FORCE
                        # X
                        # ?X
                        # ??-
                        # ???X
                        elif board[line + 2][col + 2] == '' and \
                             board[line + 3][col + 3] == token:
                            # X
                            # ?X
                            # ??-
                            # ??-X
                            if board[line + 3][col + 2] == '':
                                evaluation_board[line + 2][col + 2] = 'T'
                                #score += MOVE_TRAP
                            # X
                            # ?X
                            # ??-
                            # ???X
                            else:
                                evaluation_board[line + 2][col + 2] = 'F'
                                #score += MOVE_FORCE
                    # X
                    # ?-
                    # ??X
                    # ???X
                    elif board[line + 1][col + 1] == ''    and \
                         board[line + 2][col + 2] == token and \
                         board[line + 3][col + 3] == token:
                            # X
                            # ?-
                            # ?-X
                            # ??-X
                            if board[line + 2][col + 1] == '':
                                evaluation_board[line + 1][col + 1] = 'T'
                                #score += MOVE_TRAP
                            # X
                            # ?-
                            # ??X
                            # ???X
                            else:
                                evaluation_board[line + 1][col + 1] = 'F'
                                #score += MOVE_FORCE
                # -    -
                # ?X   ?X
                # ??X  ??X
                # ???X ???X
                # ???? ????-
                elif board[line    ][col    ] == ''    and \
                     board[line + 1][col + 1] == token and \
                     board[line + 2][col + 2] == token and \
                     board[line + 3][col + 3] == token:
                        # -
                        # -X
                        # ??X
                        # ???X
                        if board[line + 1][col] == '':
                            evaluation_board[line][col] = 'T'
                            #score += MOVE_TRAP
                        # -
                        # ?X
                        # ??X
                        # ???X
                        # ????-
                        elif col < WIDTH - 4 and line < HEIGHT -  4 and \
                             board[line + 4][col + 4] == '':
                            evaluation_board[line    ][col    ] = 'W'
                            evaluation_board[line + 4][col + 4] = 'W'
                            #score += MOVE_WIN
                        # -
                        # ?X
                        # ??X
                        # ???X
                        else:
                            evaluation_board[line][col] = 'F'
                            #score += MOVE_FORCE

    # horizontal check
    # XXX- XXX- X-XX X-XX XX-X XX-X -XXX -XXX -XXX-
    # ???- ???? ?-?? ???? ??-? ???? -??? ???? ?????
    horizontalEvaluation(board, token)

    # vertical check
    # -
    # X
    # X
    # X
    verticalEvaluation(board, token)

    # diagonal check
    # X    X    X    X    X    X    -    -    -
    # ?X   ?X   ?X   ?X   ?-   ?-   ?X   -X   ?X
    # ??X  ??X  ??-  ??-  ??X  ?-X  ??X  ??X  ??X
    # ???- ???- ???X ??-X ???X ???X ???X ???X ???X
    # ???? ???- ???? ???? ???? ???? ???? ???? ????-
    diagonalEvaluation(board, token)

    # diagonal check mirrored
    #    X    X    X    X    X    X    -    -    -
    #   X?   X?   X?   X?   -?   -?   X?   X-   X-
    #  X??  X??  -??  -??  X??  X-?  X??  X??  X??
    # -??? -??? X??? X-?? X??? X??? X??? X??? X???
    # ???? -??? ???? ???? ???? ???? ???? ???? -???
    diagonalEvaluation(game.mirrorBoard(board), token)

    # calculate score and find winning move
    return boardScoreEvaluation()
