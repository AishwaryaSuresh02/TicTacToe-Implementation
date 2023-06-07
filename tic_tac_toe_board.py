import random

import numpy as np
import constants as const


class Tic_Tac_Toe_Board:
    def __init__(self, tic_tac_toc_board=None, illegal_move=None):
        if tic_tac_toc_board is None:
            self.tic_tac_board = np.array([const.CELL_EMPTY] * const.BOARD_SIZE ** 2)
        else:
            self.tic_tac_board = tic_tac_toc_board
        self.illegal_move = illegal_move
        self.tic_tac_board_2d = self.tic_tac_board.reshape(const.BOARD_STATS)

    def get_result(self):
        if self.illegal_move is not None:
            val = const.RESULT_O_WINS if self.check_whose_turn() == const.CELL_X else const.RESULT_X_WINS
            return val
        ro_col_dia = get_all_row_col_and_dia(self.tic_tac_board_2d)
        sum_val = list(map(sum, ro_col_dia))
        max_val = max(sum_val)
        min_val = min(sum_val)
        if max_val == const.BOARD_SIZE:
            return const.RESULT_X_WINS
        if min_val == -const.BOARD_SIZE:
            return const.RESULT_O_WINS
        if const.CELL_EMPTY not in self.tic_tac_board_2d:
            return const.RESULT_DRAW
        return const.RESULT_NOT_OVER

    def check_is_game_over(self):
        res = (self.get_result() != const.RESULT_NOT_OVER)
        return res

    def is_the_board_in_illegal_state(self):
        return self.illegal_move is not None

    def get_valid_index_moves(self):
        temp = ([index for index in range(self.tic_tac_board.size) if self.tic_tac_board[index] == const.CELL_EMPTY])
        return temp

    def check_whose_turn(self):
        non_empty_places = np.count_nonzero(self.tic_tac_board)
        return const.CELL_X if is_even(non_empty_places) else const.CELL_0

    def assign_move(self, index_val):
        tic_tac_toe_board_copy = np.copy(self.tic_tac_board)
        if index_val not in self.get_valid_index_moves():
            return Tic_Tac_Toe_Board(tic_tac_toe_board_copy, illegal_move=index_val)
        tic_tac_toe_board_copy[index_val] = self.check_whose_turn()
        return Tic_Tac_Toe_Board(tic_tac_toe_board_copy)

    def get_illegal_move_index(self):
        return [indx for indx in range(self.tic_tac_board.size) if self.tic_tac_board[indx] != const.CELL_EMPTY]

    def get_rand_val_mov_indx(self):
        return random.choice(self.get_valid_index_moves())

    def get_tic_tac_str(self):
        row_val, col_val = self.tic_tac_board_2d.shape
        res_str = "--------\n"
        for row_int in range(row_val):
            for col_int in range(col_val):
                temp = get_symbol_in_cell(self.tic_tac_board_2d[row_int, col_int])
                if col_int == 0:
                    res_str += f"|{temp}|"
                elif col_int == 1:
                    res_str += f"{temp}|"
                else:
                    res_str += f"{temp}|\n"
        res_str += "--------\n"
        return res_str

    def print_tic_tac_toe(self):
        print(self.get_tic_tac_str())


def is_result_draw(tic_tac_board):
    is_draw = (tic_tac_board.get_result() == const.RESULT_DRAW)
    return is_draw


def get_symbol_in_cell(cell_value):
    if cell_value == const.CELL_X:
        return 'X'
    if cell_value == const.CELL_0:
        return 'O'
    return '-'


def get_all_row_and_dia(tic_tac_board_2d):
    row_no = tic_tac_board_2d.shape[0]
    row_val = [row for row in tic_tac_board_2d[range(row_no), :]]
    dia_val = [tic_tac_board_2d.diagonal()]
    row_dia_val = row_val + dia_val
    return row_dia_val


def get_all_row_col_and_dia(tic_tac_board_2d):
    row_and_dia = get_all_row_and_dia(tic_tac_board_2d)
    cols_and_anti_dia = get_all_row_and_dia(np.rot90(tic_tac_board_2d))
    all_vales = row_and_dia + cols_and_anti_dia
    return all_vales


def get_sym_board_ori(tic_tac_board_2d):
    return [(tr.transform(tic_tac_board_2d), tr) for tr in const.TRANSFORMATIONS]


def is_even(val):
    return val % 2 == 0


def is_empty(val):
    return val is None or len(val) == 0
