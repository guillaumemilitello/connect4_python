'''
Created on Mar 12, 2016

@author: guillaume
'''

from copy import deepcopy
from random import choice
import saved_games
import board
import debug

# debug traces on file and verbose level
DEBUG = True
DEBUG_LEVEL = 0

# number of deeper moves to look for (max : 7)
deep_moves_number = 7

# board evaluation coefficients
invalid_move  = -999999
winning_move  =     100
loosing_move  =    -100
winning_2_moves  =     40
forced_move   =      10
traped_move   =       5
advance_move  =       3

def getComputerBestMove(main_game):

    # only print highest level result
    if DEBUG:
        global __dbg_lvl__
        __dbg_lvl__ = main_game.level - DEBUG_LEVEL

    # compare with pre-registered moves
    for game in saved_games.startup_games:
        if main_game == game:

            if __dbg_lvl__ <= main_game.level:
                debug.writeString('-'*45 + ' pre-registered game - turn:computer')
                debug.writeBoard(game.m_board)
                debug.writeString('final best move          - (%d)\t' %game.move)
            return game.move

    # get the score of the different possible moves and the choose the best one
    scores = turnScore(main_game)
    best_moves = [move for move, x in enumerate(scores) if x == max(scores)]

    # if several move scores 0
    if all([scores[move] == 0 for move in best_moves]) and len(best_moves) > 1:

        if __dbg_lvl__ <= main_game.level:
            debug.scoresBestMoves('final best moves center  - \t', scores, best_moves)

        if board.center in best_moves:
            return board.center
        elif board.center - 1 in best_moves and board.center + 1 in best_moves:
            return choice([board.center - 1, board.center + 1])
        elif board.center - 1 in best_moves:
            return board.center - 1
        elif board.center + 1 in best_moves:
            return board.center + 1
        elif board.center - 2 in best_moves and board.center + 2 in best_moves:
            return choice([board.center - 2, board.center + 2])
        elif board.center - 2 in best_moves:
            return board.center - 2
        elif board.center + 2 in best_moves:
            return board.center + 2

    if __dbg_lvl__ <= main_game.level:
        debug.scoresBestMoves('final best moves         - \t', scores, best_moves)

    return choice(best_moves)

def turnScore(game):

    scores = [0] * board.width

    if __dbg_lvl__ <= game.level:
        debug.writeString('-' * 55 + ' turnScore - turn:%s' %game.turn)
        debug.writeBoard(game.m_board)

    # store the evaluation scores for deeper level moves
    if game.level > 1:
        scores_t = []
        scores_t_others = []

    scores_other = [0] * board.width
    copy_games = []

    for move in range(board.width):
        # save the state of the current game
        copy_game = deepcopy(game)
        copy_games.append(copy_game)
        scores[move], scores_other[move] = moveScore(copy_game, move)

        if game.level > 1:
            scores_t.append((scores[move], move))
            scores_t_others.append((scores_other[move], move))

        # ultimate winning move
        if scores[move] == winning_move:
            scores = [invalid_move] * board.width
            scores[move] = winning_move

            if __dbg_lvl__ <= game.level:
                debug.scores('board scores       - l:%d - \t' %game.level, scores)

            return scores
    
    # check for valid moves
    valid_moves = []
    for move in range(board.width):
        if not scores[move] == invalid_move and scores_other[move] == invalid_move:
            valid_moves.append(move)
    if len(valid_moves) == 1:
        return scores

    # check for winning opponent move
    for move in range(board.width):
        if scores_other[move] == winning_move:
            scores = [loosing_move] * board.width
            scores[move] = forced_move

            if __dbg_lvl__ <= game.level:
                debug.scores('board scores       - l:%d - \t' %game.level, scores)

            return scores

    if __dbg_lvl__ <= game.level:
        debug.scores('board scores       - l:%d - \t' %game.level, scores)
        debug.scores('board scores other - l:%d - \t' %game.level,scores_other)

    if game.level > 1:
        # sort the previous scores
        all_scores = scores_t + scores_t_others
        all_scores.sort(key = lambda x: x[0], reverse=True)

        moves = []
        # study only the best cases
        for score in all_scores:
            if not score[1] in moves and not score[0] == invalid_move:
                moves.append(score[1])
            if len(moves) == deep_moves_number:
                break

        # don't play the others moves
        for move in range(board.width):
            if move not in moves:
                scores[move] = invalid_move

        if __dbg_lvl__ <= game.level:
            # create array for saving all moves
            deep_scores_dbg = []
            debug.scores('turnScore          - l:%d - \t' %game.level, scores)

        # return the best score of the calculation level - 1
        for move in moves:

            copy_games[move].level -= 1

            if __dbg_lvl__ <= copy_games[move].level:
                debug.writeString('-' * 55 + ' l:%d - m:%d' %(game.level - 1, move))

            deep_scores = turnScore(copy_games[move])
            scores[move] -= max(deep_scores)

            if __dbg_lvl__ <= game.level:
                deep_scores_dbg.append((move, deep_scores))

        if __dbg_lvl__ <= game.level:
            debug.deepScores('-' * 55, deep_scores_dbg)

    if __dbg_lvl__ <= game.level:
        debug.scores('final scores             - \t', scores)

    return scores

def moveScore(game, move):

    # check for invalid move
    if not game.validMove(move):
        return invalid_move, invalid_move

    # evaluate the actual board for reference score
    base_score = boardEvaluation(game.m_board, game.token())

    # copy the actual board for opponent check
    game_other = deepcopy(game)

    # generate move for the current game
    winner_move, _ = game.makeMove(move)

    # check for a winning move
    if winner_move:
        return winning_move, loosing_move

    # evaluate the current move
    player_score = boardEvaluation(game.m_board, game.tokenOther())
    
    # mock an opponent move for the current game 
    winner_move, _ = game_other.makeMoveOther(move)

    if winner_move:
        return loosing_move, winning_move

    # evaluate the mock opponent move
    opponent_score = boardEvaluation(game_other.m_board, game_other.token())

    return player_score - base_score, opponent_score - base_score

def boardEvaluation(m_board, token):

    m_board_evaluation = deepcopy(m_board)

    def boardScoreEvaluation():
        score = 0
        for col in range(board.width):
            for line in range(board.height):
                # trap
                if m_board_evaluation[line][col] == 'T':
                    # winning within 2 move
                    if line < board.height - 1 and m_board_evaluation[line + 1][col] == 'F':
                        score += winning_2_moves
                    else:
                        score += traped_move
                # forced move
                elif m_board_evaluation[line][col] == 'F':
                    score += forced_move
                # winning move
                elif m_board_evaluation[line][col] == 'W':
                    return winning_move
        return score

    def horizontalEvaluation(m_board, token):
        for col in range(board.width - 3):
            for line in range(board.height):
                if m_board[line][col] == token:
                    # XXX- XX-X
                    if m_board[line][col + 1] == token:
                        # XXX-
                        if m_board[line][col + 2] == token and \
                           m_board[line][col + 3] == '':
                            if line < board.height - 1:
                                # XXX-
                                # ???-
                                if m_board[line + 1][col + 3] == '':
                                    m_board_evaluation[line][col + 3] = 'T'
                                    #score += traped_move
                                # XXX-
                                # ????
                                else:
                                    m_board_evaluation[line][col + 3] = 'F'
                                    #score += forced_move
                            # XXX-
                            else:
                                m_board_evaluation[line][col + 3] = 'F'
                                #score += forced_move
                        # XX-X
                        elif m_board[line][col + 2] == '' and \
                             m_board[line][col + 3] == token:
                            if line < board.height - 1:
                                # XX-X
                                # ??-?
                                if m_board[line + 1][col + 2] == '':
                                    m_board_evaluation[line][col + 2] = 'T'
                                    #score += traped_move
                                # XX-X
                                # ????
                                else:
                                    m_board_evaluation[line][col + 2] = 'F'
                                    #score += forced_move
                            # XX-X
                            else:
                                m_board_evaluation[line][col + 2] = 'F'
                                #score += forced_move
                    # X-XX
                    elif m_board[line][col + 1] == ''    and \
                         m_board[line][col + 2] == token and \
                         m_board[line][col + 3] == token:
                        if line < board.height - 1:
                            # X-XX
                            # ?-??
                            if m_board[line + 1][col + 1] == '':
                                m_board_evaluation[line][col + 1] = 'T'
                                #score += traped_move
                            # X-XX
                            # ????
                            else:
                                m_board_evaluation[line][col + 1] = 'F'
                                #score += forced_move
                        # X-XX
                        else:
                            m_board_evaluation[line][col + 1] = 'F'
                            #score += forced_move
                # -XXX -XXX-
                elif m_board[line][col] == '' and \
                     m_board[line][col + 1] == token and \
                     m_board[line][col + 2] == token and \
                     m_board[line][col + 3] == token:
                    if line < board.height - 1:
                        # -XXX
                        # -???
                        if m_board[line + 1][col] == '':
                            m_board_evaluation[line][col] = 'T'
                            #score += traped_move
                        # -XXX-
                        # ?????
                        elif col < board.width - 4 and m_board[line][col + 4] == '' and \
                             not m_board[line + 1][col + 4] == '':
                            m_board_evaluation[line][col    ] = 'W'
                            m_board_evaluation[line][col + 4] = 'W'
                            #score += winning_move
                        # -XXX
                        # ????
                        else:
                            m_board_evaluation[line][col] = 'F'
                            #score += forced_move
                    # -XXX-
                    elif col < board.width - 4 and m_board[line][col + 4] == '':
                        m_board_evaluation[line][col    ] = 'W'
                        m_board_evaluation[line][col + 4] = 'W'
                        #score += winning_move
                    # -XXX
                    else:
                        m_board_evaluation[line][col] = 'T'
                        #score += forced_move

    def verticalEvaluation(m_board, token):
        for col in range(board.width):
            for line in range(board.height - 3):
                # -
                # X
                # X
                # X
                if m_board[line    ][col] == ''    and \
                   m_board[line + 1][col] == token and \
                   m_board[line + 2][col] == token and \
                   m_board[line + 3][col] == token:
                    m_board_evaluation[line][col] = 'F'
                    # score += forced_move
    
    def diagonalEvaluation(m_board, token):
        for col in range(board.width - 3):
            for line in range(board.height - 3):
                # X    X    X
                # ?X   ?X   ?-
                # ??X  ??-  ??X
                # ???- ???X ???X
                if m_board[line][col] == token :
                    # X    X
                    # ?X   ?X
                    # ??X  ??-
                    # ???- ???X
                    if m_board[line + 1][col + 1] == token:
                        # X
                        # ?X
                        # ??X
                        # ???-
                        if m_board[line + 2][col + 2] == token and \
                           m_board[line + 3][col + 3] == '':
                            if line + 4 < board.height - 1:
                                # X
                                # ?X
                                # ??X
                                # ???-
                                # ???-
                                if m_board[line + 4][col + 3] == '':
                                    m_board_evaluation[line + 3][col + 3] = 'T'
                                    #score += traped_move
                                # X
                                # ?X
                                # ??X
                                # ???-
                                # ????
                                else:
                                    m_board_evaluation[line + 3][col + 3] = 'F'
                                    #score += forced_move 
                            # X
                            # ?X
                            # ??X
                            # ???-
                            else:
                                m_board_evaluation[line + 3][col + 3] = 'F'
                                #score += forced_move
                        # X
                        # ?X
                        # ??-
                        # ???X
                        elif m_board[line + 2][col + 2] == '' and \
                             m_board[line + 3][col + 3] == token:
                            # X
                            # ?X
                            # ??-
                            # ??-X
                            if m_board[line + 3][col + 2] == '':
                                m_board_evaluation[line + 2][col + 2] = 'T'
                                #score += traped_move
                            # X
                            # ?X
                            # ??-
                            # ???X
                            else:
                                m_board_evaluation[line + 2][col + 2] = 'F'
                                #score += forced_move
                    # X
                    # ?-
                    # ??X
                    # ???X
                    elif m_board[line + 1][col + 1] == ''    and \
                         m_board[line + 2][col + 2] == token and \
                         m_board[line + 3][col + 3] == token:
                            # X
                            # ?-
                            # ?-X
                            # ??-X
                            if m_board[line + 2][col + 1] == '':
                                m_board_evaluation[line + 1][col + 1] = 'T'
                                #score += traped_move
                            # X
                            # ?-
                            # ??X
                            # ???X
                            else:
                                m_board_evaluation[line + 1][col + 1] = 'F'
                                #score += forced_move
                # -    -
                # ?X   ?X
                # ??X  ??X
                # ???X ???X
                # ???? ????-
                elif m_board[line    ][col    ] == ''    and \
                     m_board[line + 1][col + 1] == token and \
                     m_board[line + 2][col + 2] == token and \
                     m_board[line + 3][col + 3] == token:
                        # -
                        # -X
                        # ??X
                        # ???X
                        if m_board[line + 1][col] == '':
                            m_board_evaluation[line][col] = 'T'
                            #score += traped_move
                        # -
                        # ?X
                        # ??X
                        # ???X
                        # ????-
                        elif col < board.width - 4 and line < board.height -  4 and \
                             m_board[line + 4][col + 4] == '':
                            m_board_evaluation[line    ][col    ] = 'W'
                            m_board_evaluation[line + 4][col + 4] = 'W'
                            #score += winning_move
                        # -
                        # ?X
                        # ??X
                        # ???X
                        else:
                            m_board_evaluation[line][col] = 'F'
                            #score += forced_move

    # horizontal check
    # XXX- XXX- X-XX X-XX XX-X XX-X -XXX -XXX -XXX-
    # ???- ???? ?-?? ???? ??-? ???? -??? ???? ?????
    horizontalEvaluation(m_board, token)

    # vertical check
    # -
    # X
    # X
    # X
    verticalEvaluation(m_board, token)

    # diagonal check
    # X    X    X    X    X    X    -    -    -
    # ?X   ?X   ?X   ?X   ?-   ?-   ?X   -X   ?X
    # ??X  ??X  ??-  ??-  ??X  ?-X  ??X  ??X  ??X
    # ???- ???- ???X ??-X ???X ???X ???X ???X ???X
    # ???? ???- ???? ???? ???? ???? ???? ???? ????-
    diagonalEvaluation(m_board, token)

    # diagonal check mirrored
    #    X    X    X    X    X    X    -    -    -
    #   X?   X?   X?   X?   -?   -?   X?   X-   X-
    #  X??  X??  -??  -??  X??  X-?  X??  X??  X??
    # -??? -??? X??? X-?? X??? X??? X??? X??? X???
    # ???? -??? ???? ???? ???? ???? ???? ???? -???
    diagonalEvaluation(board.mirrorBoard(m_board), token)

    # calculate score and find winning move
    return boardScoreEvaluation()
