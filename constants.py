import numpy as np
from TicTacToe.matrix_transformation import Transform, Rotate90, Identity, Flip

TRANSFORMATIONS = [Identity(), Rotate90(1), Rotate90(2), Rotate90(3),
                   Flip(np.flipud), Flip(np.fliplr),
                   Transform(Rotate90(1), Flip(np.flipud)),
                   Transform(Rotate90(1), Flip(np.fliplr))]

BOARD_SIZE =3
BOARD_STATS =( BOARD_SIZE, BOARD_SIZE)

CELL_X =1
CELL_0 =-1
CELL_EMPTY =0

RESULT_X_WINS = 1
RESULT_O_WINS = -1
RESULT_DRAW = 0
RESULT_NOT_OVER = 2