'''
Created on Mar 31, 2016

@author: guillaume
'''
from game import PredefinedGame
from random import choice

startup_games = []

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '', 'O', 'X',  '',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '', 'X', 'O',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '',  '',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', '']], 3)
startup_games.append(game)

game = PredefinedGame([['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', ''],
                       ['',  '',  '', 'O',  '',  '', ''],
                       ['',  '',  '', 'X',  '',  '', '']], choice([2, 4]))
startup_games.append(game)