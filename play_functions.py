import itertools
import random
import numpy as np
from tic_tac_toe_board import Tic_Tac_Toe_Board
import constants as const


def play_game(xStrategy, oStrategy):
    tic_tac_toe_board = Tic_Tac_Toe_Board()
    player_modes = itertools.cycle([xStrategy, oStrategy])
    while not tic_tac_toe_board.check_is_game_over():
        play = next(player_modes)
        tic_tac_toe_board = play(tic_tac_toe_board)
    return tic_tac_toe_board

def play_games(no_of_games, xStrategy, oStrategy, single_play_game=play_game):
    result_stats = {
        const.RESULT_X_WINS: 0,
        const.RESULT_O_WINS: 0,
        const.RESULT_DRAW: 0
    }

    for game in range (no_of_games):
        result_game = (single_play_game(xStrategy,oStrategy))
        result = result_game.get_result()
        result_stats[result]+=1

    x_percentage_win = (result_stats[const.RESULT_X_WINS]/no_of_games) * 100
    o_percentage_win = (result_stats[const.RESULT_O_WINS]/no_of_games) *100
    percentage_draw = (result_stats[const.RESULT_DRAW]/no_of_games) * 100

    print(f"X Win Percentage :{x_percentage_win :.2f}%")
    print(f"O Win Percentage :{o_percentage_win:.2f}%")
    print(f"Draw Percentage :{percentage_draw:.2f}%")

def play_move_random(tic_tac_board):
    rand_move = tic_tac_board.get_rand_val_mov_indx()
    return tic_tac_board.assign_move(rand_move)

