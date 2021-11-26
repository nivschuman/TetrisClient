from Tetrino import Tetrino
from Position import Position
from Block import Block
from Exceptions import CannotRotateExceptions


class TShape(Tetrino):
    def __init__(self, block_side, length, width):
        # positions = [Position(0, 18), Position(1, 19), Position(1, 18), Position(2, 18)]
        middle_col = length // 2 - 1
        positions = [Position(middle_col-1, width - 2), Position(middle_col, width - 1),
                     Position(middle_col, width - 2), Position(middle_col+1, width - 2)]
        super().__init__(block_side, positions)

    def _set_direction(self, board_length, board_width, direction, board_status):
        new_blocks = []
        center_pos = self._blocks[2].pos
        positions = []
        if direction == 0:
            positions.append(Position(center_pos.col - 1, center_pos.row))
            positions.append(Position(center_pos.col, center_pos.row + 1))
            positions.append(center_pos)
            positions.append(Position(center_pos.col + 1, center_pos.row))

        elif direction == 90:
            positions.append(Position(center_pos.col, center_pos.row+1))
            positions.append(Position(center_pos.col+1, center_pos.row))
            positions.append(center_pos)
            positions.append(Position(center_pos.col, center_pos.row-1))

        elif direction == 180:
            positions.append(Position(center_pos.col-1, center_pos.row))
            positions.append(Position(center_pos.col, center_pos.row-1))
            positions.append(center_pos)
            positions.append(Position(center_pos.col+1, center_pos.row))

        elif direction == 270:
            positions.append(Position(center_pos.col, center_pos.row+1))
            positions.append(Position(center_pos.col-1, center_pos.row))
            positions.append(center_pos)
            positions.append(Position(center_pos.col, center_pos.row-1))

        for pos in positions:
            if (pos.col < 0 or pos.col >= board_length) or (pos.row < 0 or pos.row >= board_width):
                raise CannotRotateExceptions(direction)
            if board_status[pos.row][pos.col] == 1:
                raise CannotRotateExceptions(direction)

            new_blocks.append(Block(self._blockSide, pos))

        self._blocks = new_blocks
