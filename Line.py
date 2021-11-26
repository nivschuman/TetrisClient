from Tetrino import Tetrino
from Position import Position
from Block import Block
from Exceptions import CannotRotateExceptions


class Line(Tetrino):
    def __init__(self, block_side, length, width):
        middle_col = length // 2 - 1
        positions = [Position(middle_col-1, width - 1), Position(middle_col, width - 1),
                     Position(middle_col+1, width - 1), Position(middle_col+2, width - 1)]
        super().__init__(block_side, positions)

    def _set_direction(self, board_length, board_width, direction, board_status):
        new_blocks = []
        positions = []
        center_pos = self._blocks[1].pos.__copy__()
        center_pos.col += 0.5
        center_pos.row -= 0.5

        if direction == 0 or direction == 180:
            positions.append(Position(int(center_pos.col-1.5), int(center_pos.row+0.5)))
            positions.append(Position(int(center_pos.col-0.5), int(center_pos.row+0.5)))
            positions.append(Position(int(center_pos.col + 0.5), int(center_pos.row + 0.5)))
            positions.append(Position(int(center_pos.col + 1.5), int(center_pos.row + 0.5)))
        elif direction == 90 or direction == 270:
            positions.append(Position(int(center_pos.col+0.5), int(center_pos.row+1.5)))
            positions.append(Position(int(center_pos.col + 0.5), int(center_pos.row + 0.5)))
            positions.append(Position(int(center_pos.col + 0.5), int(center_pos.row - 0.5)))
            positions.append(Position(int(center_pos.col + 0.5), int(center_pos.row - 1.5)))

        for pos in positions:
            if (pos.col < 0 or pos.col >= board_length) or (pos.row < 0 or pos.row >= board_width):
                raise CannotRotateExceptions(direction)
            if board_status[pos.row][pos.col] == 1:
                raise CannotRotateExceptions(direction)

            new_blocks.append(Block(self._blockSide, pos))

        self._blocks = new_blocks

