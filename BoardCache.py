import tic_tac_toe_board
class BoardCache:
    def __init__(self):
        self.cache={}

    def set_for_pos(self,tic_tac_board,o):
        self.cache[tic_tac_board.tic_tac_board_2d.tobytes()] = o

    def get_for_pos(self,tic_tac_board):
        temp_2d=tic_tac_board.tic_tac_board_2d
        orient=  tic_tac_toe_board.get_sym_board_ori(temp_2d)

        for b,t in orient:
            res= self.cache.get(b.tobytes())
            if res is not None:
                return (res,t), True

        return  None , False

    def rest(self):
        self.cache={}
