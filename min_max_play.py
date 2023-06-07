from TicTacToe.play_functions import play_games
from TicTacToe.play_functions import play_move_random
from TicTacToe.qlearning import (qtables,play_training_games_o,play_training_games_x,create_q_player)
from  TicTacToe.minmax import create_min_max_player


play_min_max_rand=create_min_max_player(True)
play_min_max_rand_not = create_min_max_player(False)


print("Playing min max with rand ")
print("---------------------------------------------")
play_games(1000,play_min_max_rand,play_move_random)
print("")

print("Playing min max with rand ")
print("---------------------------------------------")
play_games(1000,play_move_random,play_min_max_rand)
print("")

print("Playing min max with rand ")
print("---------------------------------------------")
play_games(1000,play_min_max_rand_not,play_move_random)
print("")

print("Playing min max with rand ")
print("---------------------------------------------")
play_games(1000,play_move_random,play_min_max_rand_not)
print("")

print("Playing min max with min max  ")
print("---------------------------------------------")
play_games(1000,play_move_random,play_move_random)
print("")

print("Playing min max with min max  ")
print("---------------------------------------------")
play_games(1000,play_min_max_rand_not,play_min_max_rand_not)
print("")

print("Playing min max with min max  ")
print("---------------------------------------------")
play_games(1000,play_min_max_rand_not,play_min_max_rand)
print("")

print("Playing min max with min max  ")
print("---------------------------------------------")
play_games(1000,play_min_max_rand,play_min_max_rand_not)
print("")