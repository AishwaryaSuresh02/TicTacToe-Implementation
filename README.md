# TicTacToe-Implementation
This repository contains Python implementations of the classic games Tic Tac Toe . The games is implemented using Python's NumPy library and pygame for graphical user interface.

## Implementation Details
- The Tic Tac Toe game is constructed using a 2D NumPy array with 3 rows and 3 columns.
- Players are denoted by X and O, represented by 1 and -1, respectively. Empty spaces are denoted by 0.
- After each player's turn, the matrix's status is assessed to check for a winning move in rows, columns, diagonals, or anti-diagonals.
- Two algorithms are implemented for playing Tic Tac Toe:
  - Minimax algorithm with alpha-beta pruning
  - Tabular Q-learning reinforcement learning algorithm
## Running the Game
- Run the tic_tac_toe.py file to play Tic Tac Toe against a default opponent.
- Use the keyboard's number pad to make moves (1-9 correspond to the board positions).
## Algorithm Comparison
- The implemented algorithms are compared against a default opponent.
- The report provides analysis and conclusions based on the algorithm performance in terms of winning percentages and draws.
