from Tetrino import Tetrino
from Position import Position


class Square(Tetrino):
    def __init__(self, block_side, length, width):
        middle_col = length // 2 - 1
        positions = [Position(middle_col, width - 1), Position(middle_col, width - 2),
                     Position(middle_col+1, width - 1), Position(middle_col+1, width - 2)]
        super().__init__(block_side, positions)
