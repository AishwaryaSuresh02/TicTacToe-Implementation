from TicTacToe.play_functions import play_games
from TicTacToe.play_functions import play_move_random
from TicTacToe.qlearning import (qtables,play_training_games_o,play_training_games_x,create_q_player)
from  TicTacToe.minmax import create_min_max_player


# from tictac.mcts import (play_game_and_reset_playouts,
#                          play_mcts_move_with_live_playouts)

play_min_max_rand=create_min_max_player(False)
play_min_max_rand_not = create_min_max_player(False)



# print("Training qtable X vs. random...")
play_training_games_x(q_tables=qtables,
                      o_strategies=[play_move_random])
print("Training qtable O vs. random...")
play_training_games_o(q_tables=qtables,
                      x_strategies=[play_move_random])
print("")

play_q_table_move = create_q_player(qtables)
print("Playing qtable vs random:")
print("-------------------------")
play_games(1000, play_q_table_move, play_move_random)

print("")
print("Playing  random vs q table:")

play_games(1000, play_move_random,play_q_table_move)

print("Playing qtable vs  min max :")
print("-------------------------")
play_games(1000, play_q_table_move, play_min_max_rand)

print("")
print("Playing min max vs qtable:")

play_games(1000, play_min_max_rand,play_q_table_move)

print("")
print("Playing min max vs qtable:")

play_games(1000, play_q_table_move,play_q_table_move)


print("Training qtable X vs. Min Max...")
play_training_games_x(q_tables=qtables,
                      o_strategies=[play_min_max_rand])
print("Training qtable O vs. Min Max...")
play_training_games_o(q_tables=qtables,
                      x_strategies=[play_min_max_rand])
print("")

play_q_table_move_2 = create_q_player(qtables)
print("Playing qtable vs min_max:")
print("-------------------------")
play_games(1000, play_q_table_move_2, play_min_max_rand)

print("")
print("Playing min_max vs random:")

play_games(1000, play_min_max_rand,play_q_table_move_2)


print("")

print("Playing qtable vs random:")
print("-------------------------")
play_games(1000, play_q_table_move_2, play_move_random)

print("")
print("Playing qtable vs minmax :")

play_games(1000, play_move_random,play_q_table_move_2)

print("Playing qtable vs play_q_table_move:")
print("-------------------------")
play_games(1000, play_q_table_move_2, play_q_table_move_2)

print("Playing qtable vs play_q_table_move:")
print("-------------------------")
play_games(1000, play_q_table_move_2, play_q_table_move)

print("Playing qtable vs play_q_table_move:")
print("-------------------------")
play_games(1000, play_q_table_move, play_q_table_move_2)



#  Algo _vs_algo

print("Playing qtable vs minmax_rand:")
print("-------------------------")
play_games(1000, play_q_table_move,play_min_max_rand)

print("Playing qtable_2 vs minmax_rand:")
print("-------------------------")
play_games(1000, play_q_table_move_2,play_min_max_rand)


print("Playing qtable vs minmax_not_rand:")
print("-------------------------")
play_games(1000, play_q_table_move,play_min_max_rand_not)

print("Playing qtable_2 vs minmax_not_rand:")
print("-------------------------")
play_games(1000, play_q_table_move_2,play_min_max_rand_not)


print("Playing qtable vs minmax_not_rand vs qtable_2 vs:")
print("-------------------------")
play_games(1000, play_min_max_rand_not,play_q_table_move,)

print("Playing  minmax_not_rand vs qtable_2 vs:")
print("-------------------------")
play_games(1000,play_min_max_rand_not,play_q_table_move_2)


print("Playing qtable vs minmax_not_rand vs qtable_2 vs:")
print("-------------------------")
play_games(1000, play_min_max_rand,play_q_table_move,)

print("Playing  minmax_not_rand vs qtable_2 vs:")
print("-------------------------")
play_games(1000,play_min_max_rand,play_q_table_move_2)
