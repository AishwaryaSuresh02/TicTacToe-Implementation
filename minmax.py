import random
import constants as const
from BoardCache import BoardCache
from tic_tac_toe_board import is_empty
from tic_tac_toe_board import Tic_Tac_Toe_Board

cache = BoardCache()


def create_min_max_player(is_rand):
    def play(tic_tac_board):
        return play_min_max_move(tic_tac_board, is_rand)

    return play


def pick_min_max_for_best(tic_tac_board):
    tr = tic_tac_board.check_whose_turn()
    return min if tr == const.CELL_0 else max


def filter_best_move(tic_tac_board, mvm_val_pair, rand):
    min_max = pick_min_max_for_best(tic_tac_board)
    mo, val = min_max(mvm_val_pair, key=lambda m: m[1])
    if not rand:
        return mo
    best_val_pair = [m for m in mvm_val_pair if m[1] == val]
    final_mvm = random.choice(best_val_pair)
    return final_mvm


def cal_pos_val(tic_tac_board):
    if tic_tac_board.check_is_game_over():
        return tic_tac_board.get_result()
    val_mov_indx = tic_tac_board.get_valid_index_moves()

    val = [get_position_value(tic_tac_board.assign_move(mv)) for mv in val_mov_indx]
    min_max = pick_min_max_for_best(tic_tac_board)
    pos_val = min_max(val)
    return pos_val


def get_position_value(tic_tac_board):
    res, val = cache.get_for_pos(tic_tac_board)
    if val:
        return res[0]
    pos_val = cal_pos_val(tic_tac_board)
    cache.set_for_pos(tic_tac_board, pos_val)
    return pos_val


def get_predicted_value_pairs(tic_tac_board):
    valid_index = tic_tac_board.get_valid_index_moves()
    assert not is_empty(valid_index), "Its A end Pos"

    move_value_pairs = [(m, get_position_value(tic_tac_board.assign_move(m)))
                        for m in valid_index]

    return move_value_pairs


def play_min_max_move(tic_tac_board, is_rand=False):
    predicted_value_pairs = get_predicted_value_pairs(tic_tac_board)
    final_move = filter_best_move(tic_tac_board, predicted_value_pairs, is_rand)
    return tic_tac_board.assign_move(final_move)
