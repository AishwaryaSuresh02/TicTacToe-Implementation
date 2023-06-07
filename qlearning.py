import copy

import numpy as np
import statistics as stats
import random
import operator
import itertools
from collections import deque

from TicTacToe.tic_tac_toe_board import Tic_Tac_Toe_Board, is_result_draw
from TicTacToe.BoardCache import BoardCache
from TicTacToe.play_functions import play_game, play_move_random
import TicTacToe.constants as const

WIN_VALUE = 1.0
DRAW_VALUE = 0.5
LOSE_VALUE = -1.0

INITIAL_Q_VAL_FOR_X = 0.0
INITIAL_Q_VAL_FOR_O = 0.0


def get_ini_q_value(board):
    return (INITIAL_Q_VAL_FOR_X if board.check_whose_turn() == const.CELL_0
            else INITIAL_Q_VAL_FOR_O)


class Qlearn:
    def __init__(self):
        self.q_table = BoardCache()

    def get_q_val_on(self, tic_tac_board):
        mvm_indx = tic_tac_board.get_valid_index_moves()
        q_val = [self.get_q_val(tic_tac_board, mv) for mv in tic_tac_board.get_valid_index_moves()]
        return dict(zip(mvm_indx, q_val))

    def get_q_val(self, tic_tac_board, move_index):
        new_pos = tic_tac_board.assign_move(move_index)
        res, found = self.q_table.get_for_pos(new_pos)
        if found is True:
            qvalue, _ = res
            return qvalue
        return get_ini_q_value(new_pos)

    def update_q_val(self, tic_tac_board, mvm_index, qval):
        new_pos = tic_tac_board.assign_move(mvm_index)
        res, found = self.q_table.get_for_pos(new_pos)
        if found is True:
            _, t = res
            new_pos_trans = Tic_Tac_Toe_Board(t.transform(new_pos.tic_tac_board_2d).flatten())
            self.q_table.set_for_pos(new_pos_trans, qval)
            return
        self.q_table.set_for_pos(new_pos, qval)

    def get_mov_ind_max_q_val(self, tic_tac_board):
        q_val = self.get_q_val_on(tic_tac_board)
        return max(q_val.items(), key=operator.itemgetter(1))

    def print_q_val(self):
        print(f"num q_values = {len(self.q_table.cache)}")
        for k, v in self.q_table.cache.items():
            b = np.frombuffer(k, dtype=int)
            board = Tic_Tac_Toe_Board(b)
            board.print_tic_tac_toe()
            print(f"q_value = {v}")


qtables = [Qlearn()]


# double_qtables = [Qlearn(), Qlearn()]

def gather_q_values_for_move(q_tables, tic_tac_board, mvm_indx):
    return [q_table.get_q_val(tic_tac_board, mvm_indx) for q_table in q_tables]


def get_mv_avg_q_val_pair(q_tables, tic_tac_board):
    mvm_indx = sorted(q_tables[0].get_q_val_on(tic_tac_board).keys())
    avg_q_val = [stats.mean(gather_q_values_for_move(q_tables, tic_tac_board, mi)) for mi in mvm_indx]
    return list(zip(mvm_indx, avg_q_val))


def choose_mvm_index(q_tables, tic_tac_board, epsilon):
    if epsilon > 0:
        random_value = np.random.uniform()
        if random_value < epsilon:
            return tic_tac_board.get_rand_val_mov_indx()

    move_q_value_pairs = get_mv_avg_q_val_pair(q_tables, tic_tac_board)

    return max(move_q_value_pairs, key=lambda pair: pair[1])[0]


def play_q_table_move(board, q_tables=None):
    if q_tables is None:
        q_tables = qtables

    move_index = choose_mvm_index(q_tables, board, 0)
    return board.assign_move(move_index)


def create_q_player(q_tables):
    def play(tic_tac_board):
        return play_q_table_move(tic_tac_board, q_tables)

    return play


def create_training_player(q_tables, move_history, epsilon):
    def play(tic_tac_board):
        move_index = choose_mvm_index(q_tables, tic_tac_board, epsilon)
        move_history.appendleft((tic_tac_board, move_index))
        return tic_tac_board.assign_move(move_index)

    return play


def is_win(player, board):
    result = board.get_result()
    return ((player == const.CELL_0 and result == const.RESULT_O_WINS)
            or (player == const.CELL_X and result == const.RESULT_X_WINS))


def is_loss(player, board):
    result = board.get_result()
    return ((player == const.CELL_0 and result == const.RESULT_X_WINS)
            or (player == const.CELL_X and result == const.RESULT_O_WINS))


def get_game_result_value(player, tic_tac_board):
    if is_win(player, tic_tac_board):
        return WIN_VALUE
    if is_loss(player, tic_tac_board):
        return LOSE_VALUE
    if is_result_draw(tic_tac_board):
        return DRAW_VALUE


def update_training_gameover(q_tables, move_history, q_table_player, board,
                             learning_rate, discount_factor):
    game_result_reward = get_game_result_value(q_table_player, board)

    # move history is in reverse-chronological order - last to first
    if move_history:
        next_position, move_index = move_history[0]
    else:
        move_index=random.choice(board.get_valid_index_moves())
        next_position = copy.deepcopy(board)

    for q_table in q_tables:
        current_q_value = q_table.get_q_val(next_position, move_index)
        new_q_value = calculate_new_q_value(current_q_value, game_result_reward,
                                            0.0, learning_rate, discount_factor)

        q_table.update_q_val(next_position, move_index, new_q_value)

    for (position, move_index) in list(move_history)[1:]:
        current_q_table, next_q_table = get_shuffled_q_tables(q_tables)

        max_next_move_index, _ = current_q_table.get_mov_ind_max_q_val(
            next_position)

        max_next_q_value = next_q_table.get_q_val(next_position,
                                                    max_next_move_index)

        current_q_value = current_q_table.get_q_val(position, move_index)
        new_q_value = calculate_new_q_value(current_q_value, 0.0,
                                            max_next_q_value, learning_rate,
                                            discount_factor)
        current_q_table.update_q_val(position, move_index, new_q_value)

        next_position = position

    return new_q_value


def play_training_game(q_tables, move_history, q_table_player, x_strategy,
                       o_strategy, learning_rate, discount_factor):
    board = play_game(x_strategy, o_strategy)

    update_training_gameover(q_tables, move_history, q_table_player, board,
                             learning_rate, discount_factor)


def play_training_games(total_games, q_tables, q_table_player, learning_rate,
                        discount_factor, epsilon, x_strategies, o_strategies):
    if x_strategies:
        x_strategies_to_use = itertools.cycle(x_strategies)

    if o_strategies:
        o_strategies_to_use = itertools.cycle(o_strategies)

    for game in range(total_games):
        move_history = deque()

        if not x_strategies:
            x = [create_training_player(q_tables, move_history, epsilon)]
            x_strategies_to_use = itertools.cycle(x)

        if not o_strategies:
            o = [create_training_player(q_tables, move_history, epsilon)]
            o_strategies_to_use = itertools.cycle(o)

        x_strategy_to_use = next(x_strategies_to_use)
        o_strategy_to_use = next(o_strategies_to_use)

        play_training_game(q_tables, move_history, q_table_player,
                           x_strategy_to_use, o_strategy_to_use, learning_rate,
                           discount_factor)

        if (game + 1) % (total_games / 10) == 0:
            epsilon = max(0, epsilon - 0.1)
            print(f"{game + 1}/{total_games} games, using epsilon={epsilon}...")


def play_training_games_x(total_games=10000, q_tables=None,
                          learning_rate=0.4, discount_factor=1.0, epsilon=0.7,
                          o_strategies=None):
    if q_tables is None:
        q_tables = qtables
    if o_strategies is None:
        o_strategies = [play_move_random]

    play_training_games(total_games, q_tables, const.CELL_X, learning_rate,
                        discount_factor, epsilon, None, o_strategies)


def play_training_games_o(total_games=10000, q_tables=None,
                          learning_rate=0.4, discount_factor=1.0, epsilon=0.7,
                          x_strategies=None):
    if q_tables is None:
        q_tables = qtables
    if x_strategies is None:
        x_strategies = [play_move_random]

    play_training_games(total_games, q_tables, const.CELL_0, learning_rate,
                        discount_factor, epsilon, x_strategies, None)


def calculate_new_q_value(current_q_value, reward, max_next_q_value,
                          learning_rate, discount_factor):
    weighted_prior_values = (1 - learning_rate) * current_q_value
    weighted_new_value = (learning_rate
                          * (reward + discount_factor * max_next_q_value))
    return weighted_prior_values + weighted_new_value


def get_shuffled_q_tables(q_tables):
    q_tables_copy = q_tables.copy()
    random.shuffle(q_tables_copy)
    q_tables_cycle = itertools.cycle(q_tables_copy)

    current_q_table = next(q_tables_cycle)
    next_q_table = next(q_tables_cycle)

    return current_q_table, next_q_table
