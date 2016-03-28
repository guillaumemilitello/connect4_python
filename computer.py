'''
Created on Mar 12, 2016

@author: guillaume
'''

from copy import deepcopy
from random import choice
import board
import debug

# debug traces on file
__dbg__ = False

# number of deeper moves to look for (max : 7)
deep_moves_number = 5

# board evaluation coefficients
invalid_move  = -999999
winning_move  =     100
loosing_move  =    -100
forced_move   =      10
traped_move   =       5
advance_move  =       3

def getComputerBestMove(main_game):

    # focus on the middle column for the first moves
    if main_game.sum_tokens < board.height:
        status = True
        for col in range(board.width):
            if not col == board.center:
                for line in range(board.height):
                    if not main_game.m_board[line][col] == '':
                        status = False
                        break
                if not status:
                    break
        if status:
            return board.center

    if __dbg__:
        global highest_level
        highest_level = main_game.level

    # get the score of the different possible moves and the choose the best one
    scores = turnScore(main_game)
    best_moves = [move for move, x in enumerate(scores) if x == max(scores)]

    # if several move scores 0
    if all([scores[move] == 0 for move in best_moves]) and len(best_moves) > 1:

        if __dbg__:
            debug.scoresBestMoves('final best moves         - \t', scores, best_moves)

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

    if __dbg__:
        debug.scoresBestMoves('final best moves         - \t', scores, best_moves)

    return choice(best_moves)

def turnScore(game):

    scores = [0] * board.width

    if game.level == 0:
        return scores

    if __dbg__ and highest_level == game.level:
        debug.writeString('-' * 55 + ' turn score - t:%s' %game.turn)
        debug.writeBoard(game.m_board)

    # store the evaluation scores for deeper level moves
    if game.level > 1:
        scores_t = []
        scores_t_others = []

    scores_other = [0] * board.width

    for move in range(board.width):
        # save the state of the current game
        copy_game = deepcopy(game)
        scores[move], scores_other[move] = moveScore(copy_game, move)

        if game.level > 1:
            scores_t.append((scores[move], move))
            scores_t_others.append((scores_other[move], move))

        # ultimate winning move
        if scores[move] == winning_move:
            scores = [invalid_move] * board.width
            scores[move] = winning_move

            if __dbg__:
                debug.scores('board scores       - l:%d - \t' %game.level, scores)

            return scores

    # check for winning opponent move
    for move in range(board.width):
        if scores_other[move] == winning_move:
            scores = [loosing_move] * board.width
            scores[move] = forced_move

            if __dbg__:
                debug.scores('board scores       - l:%d - \t' %game.level, scores)

            return scores

    if __dbg__:
        debug.scores('board scores       - l:%d - \t' %game.level, scores)
        debug.scores('board scores other - l:%d - \t' %game.level,scores_other)

    if game.level > 1:
        # sort the previous scores
        all_scores = scores_t + scores_t_others
        all_scores.sort(key=lambda x: x[0], reverse=True)

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

        if __dbg__:
            debug.scores('turn score         - l:%d - \t' %game.level, scores)

        # create array for saving all moves
        if __dbg__:
            deep_scores_dbg = []

        # check level below for the best results
        for move in moves:

            if __dbg__:
                debug.writeString('-' * 55 + ' l:%d - m:%d' %(game.level - 1, move))

            # save the state of the current game
            # TODO : optimize copy
            copy_game = deepcopy(game)
            copy_game.makeMove(move)

            # return the best score of the calculation level - 1
            copy_game.level -= 1
            deep_scores = turnScore(copy_game)
            scores[move] -= max(deep_scores)

            if __dbg__:
                deep_scores_dbg.append((move, deep_scores))

        if __dbg__ and highest_level == game.level:
            debug.deepScores('-' * 55, deep_scores_dbg)

    if __dbg__ and highest_level == game.level:
        debug.scores('final scores             - \t', scores)

    return scores

def moveScore(game, move):

    # check for invalid move
    if not game.validMove(move):
        return invalid_move, invalid_move

    # evaluate the actual board for reference score
    base_score = moveEvaluation(game.m_board, game.token())

    # copy the actual board for opponent check
    game_other = deepcopy(game)

    # generate move for the current game
    winner_move, _ = game.makeMove(move)

    # check for a winning move
    if winner_move:
        return winning_move, loosing_move

    # evaluate the current move
    player_score = moveEvaluation(game.m_board, game.tokenOther())
    
    # mock an opponent move for the current game 
    winner_move, _ = game_other.makeMoveOther(move)

    if winner_move:
        return loosing_move, winning_move

    # evaluate the mock opponent move
    opponent_score = moveEvaluation(game_other.m_board, game_other.token())

    return player_score - base_score, opponent_score - base_score

def moveEvaluation(m_board, token):
    score = 0

    for col in range(board.width - 3):
        for line in range(board.height):
            if m_board[line][col    ] == token and \
               m_board[line][col + 1] == token and \
               m_board[line][col + 2] == token and \
               m_board[line][col + 3] == '':
                # XXX-
                # ???-
                if line < board.height - 1 and m_board[line + 1][col + 3] == '':
                    # trap
                    score += traped_move
                # XXX-
                # ????
                    # force play
                    score += forced_move

    for col in range(board.width - 3):
        for line in range(board.height):
            if m_board[line][col    ] == ''    and \
               m_board[line][col + 1] == token and \
               m_board[line][col + 2] == token and \
               m_board[line][col + 3] == token:
                # -XXX
                # -???
                if line < board.height - 1 and m_board[line + 1][col] == '':
                    # trap
                    score += traped_move
                # -XXX
                # ????
                else:
                    # force play
                    score += forced_move

    for col in range(board.width - 3):
        for line in range(board.height):
            if m_board[line][col    ] == token and \
               m_board[line][col + 1] == ''    and \
               m_board[line][col + 2] == token and \
               m_board[line][col + 3] == token:
                # X-XX
                # ?-??
                if line < board.height - 1 and m_board[line + 1][col + 1] == '':
                    # trap
                    score += traped_move
                # X-XX
                # ????
                else:
                    # force play
                    score += forced_move
    
    for col in range(board.width - 3):
        for line in range(board.height):
            if m_board[line][col    ] == token and \
               m_board[line][col + 1] == token and \
               m_board[line][col + 2] == ''    and \
               m_board[line][col + 3] == token:
                # XX-X
                # ??-?
                if line < board.height - 1 and m_board[line + 1][col + 2] == '':
                    # trap
                    score += traped_move
                # XX-X
                # ????
                else:
                    # force play
                    score += forced_move

    for col in range(board.width - 4):
        for line in range(board.height):
            if m_board[line][col    ] == ''    and \
               m_board[line][col + 1] == token and \
               m_board[line][col + 2] == token and \
               m_board[line][col + 3] == token and \
               m_board[line][col + 4] == '':
                # -XXX-
                # -???-
                if line < board.height - 1 and m_board[line + 1][col] == '' and m_board[line + 1][col + 4] == '':
                    # double force trap (already)
                    score += traped_move
                elif line < board.height - 1 and (m_board[line + 1][col] == '' or m_board[line + 1][col + 4] == ''):
                    # -XXX- -XXX-
                    # ????- -????
                    # force play already + trap
                    score += traped_move
                else:
                    # -XXX-
                    # ?????
                    # winning move
                    score += winning_move

    # -
    # X
    # X
    # X
    for col in range(board.width):
        for line in range(board.height - 3):
            if m_board[line    ][col] == ''    and \
               m_board[line + 1][col] == token and \
               m_board[line + 2][col] == token and \
               m_board[line + 3][col] == token:
                # force play
                score += forced_move

    # -
    # X
    # X
    for col in range(board.width):
        for line in range(board.height - 2):
            if m_board[line    ][col] == ''    and \
               m_board[line + 1][col] == token and \
               m_board[line + 2][col] == token:
                # minor play
                score += advance_move

    #   -
    #  X?
    # X??
    for col in range(2, board.width):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == ''    and \
               m_board[line + 1][col - 1] == token and \
               m_board[line + 2][col - 2] == token:
                # minor play
                score += advance_move

    # -
    # ?X
    # ??X
    for col in range(board.width - 3):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == ''    and \
               m_board[line + 1][col + 1] == token and \
               m_board[line + 2][col + 2] == token:
                # minor play
                score += advance_move

    for col in range(board.width - 3):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == ''    and \
               m_board[line + 1][col + 1] == token and \
               m_board[line + 2][col + 2] == token and \
               m_board[line + 3][col + 3] == token:
                # -
                # -X
                # ??X
                # ???X
                if m_board[line + 1][col] == '':
                    # trap
                    score += traped_move
                # -
                # ?X
                # ??X
                # ???X
                else:
                    # force play
                    score += forced_move

    for col in range(board.width - 3):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == token and \
               m_board[line + 1][col + 1] == ''    and \
               m_board[line + 2][col + 2] == token and \
               m_board[line + 3][col + 3] == token:
                # X
                # ?-
                # ?-X
                # ???X
                if m_board[line + 2][col + 1] == '':
                    # trap
                    score += traped_move
                # X
                # ?-
                # ??X
                # ???X
                else:
                    # force play
                    score += forced_move

    for col in range(board.width - 3):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == token and \
               m_board[line + 1][col + 1] == token and \
               m_board[line + 2][col + 2] == ''    and \
               m_board[line + 3][col + 3] == token:
                # X
                # ?X
                # ??-
                # ??-X
                if m_board[line + 3][col + 2] == '':
                    # trap
                    score += traped_move
                # X
                # ?X
                # ??-
                # ???X
                else:
                    # force play
                    score += forced_move

    for col in range(board.width - 3):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == token and \
               m_board[line + 1][col + 1] == token and \
               m_board[line + 2][col + 2] == token and \
               m_board[line + 3][col + 3] == '':
                # X
                # ?X
                # ??X
                # ???-
                # ???-
                if line + 4 < board.height - 1 and m_board[line + 4][col + 3] == '':
                    # trap
                    score += traped_move
                # X
                # ?X
                # ??X
                # ???-
                # ????
                else:
                    # force play
                    score += forced_move

    for col in range(board.width - 4):
        for line in range(board.height - 4):
            if m_board[line    ][col    ] == ''    and \
               m_board[line + 1][col + 1] == token and \
               m_board[line + 2][col + 2] == token and \
               m_board[line + 3][col + 3] == token and \
               m_board[line + 4][col + 4] == '':
                if m_board[line + 1][col] == '':
                    # -
                    # -X
                    # ??X
                    # ???X
                    # ????-
                    # ????-
                    if line + 5 < board.height - 1 and m_board[line + 5][col + 4] == '':
                        # double trap
                        score += traped_move
                    # -
                    # -X
                    # ??X
                    # ???X
                    # ????-
                    # ?????
                    else:
                        # force play + trap
                        score += traped_move
                else:
                    # -
                    # ?X
                    # ??X
                    # ???X
                    # ????-
                    # ????-
                    if line + 5 < board.height - 1 and m_board[line + 5][col + 4] == '':
                        # force play + trap
                        score += traped_move
                    # -
                    # ?X
                    # ??X
                    # ???X
                    # ????-
                    # ?????
                    else:
                        # winning board
                        score += winning_move

    for col in range(3, board.width):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == token and \
               m_board[line + 1][col - 1] == token and \
               m_board[line + 2][col - 2] == token and \
               m_board[line + 3][col - 3] == '':
                #    X
                #   X?
                #  X??
                # -???
                # -???
                if line + 4 < board.height - 1 and m_board[line + 4][col - 3] == '':
                    # trap
                    score += traped_move
                #    X
                #   X?
                #  X??
                # -???
                else:
                    # force play
                    score += forced_move

    for col in range(3, board.width):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == token and \
               m_board[line + 1][col - 1] == token and \
               m_board[line + 2][col - 2] == ''    and \
               m_board[line + 3][col - 3] == token:
                #    X
                #   X?
                #  -??
                # X-??
                if m_board[line + 3][col - 2] == '':
                    # trap
                    score += traped_move
                #    X
                #   X?
                #  -??
                # X???
                else:
                    # force play
                    score += forced_move

    for col in range(3, board.width):
        for line in range(board.height - 3):
            if m_board[line    ][col    ] == token and \
               m_board[line + 1][col - 1] == ''    and \
               m_board[line + 2][col - 2] == token and \
               m_board[line + 3][col - 3] == token:
                #    X
                #   -?
                #  X-?
                # X???
                if m_board[line + 2][col - 1] == '':
                    # trap
                    score += traped_move
                #    X
                #   -?
                #  X??
                # X???
                else:
                    # force play
                    score += forced_move

    for col in range(4, board.width):
        for line in range(board.height - 4):
            if m_board[line    ][col    ] == ''    and \
               m_board[line + 1][col - 1] == token and \
               m_board[line + 2][col - 2] == token and \
               m_board[line + 3][col - 3] == token and \
               m_board[line + 4][col - 4] == '':
                if m_board[line + 1][col] == '':
                    #     -
                    #    X-
                    #   X??
                    #  X???
                    # -????
                    # -????
                    if line + 5 < board.height - 1 and m_board[line + 5][col - 4] == '':
                        # double trap
                        score += traped_move
                    #     -
                    #    X-
                    #   X??
                    #  X???
                    # -????
                    # ?????
                    else:
                        # force play + trap
                        score += forced_move
                else:
                    #     -
                    #    X?
                    #   X??
                    #  X???
                    # -????
                    # -????
                    if line + 5 < board.height - 1 and m_board[line + 5][col - 4] == '':
                        # force play + trap
                        score += forced_move
                    #     -
                    #    X?
                    #   X??
                    #  X???
                    # -????
                    # ?????
                    else:
                        # winning board
                        score += winning_move

    return score

