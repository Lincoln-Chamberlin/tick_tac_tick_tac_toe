"""A 2 player game of Tick Tac Tick Tac Toe

Project Name: Tick Tac Tick Tac Toe
Author: Lincoln Chamberlin

Game is played on a 3x3 grid of 3x3 playfields.
Each 3x3 grid acts like a game of tick tac toe.

the spaces of the outer board belong to the winner of the inner board

You must play on the inner board corsponding to the
location of the prevous player's move on their board.

If the designated board is complete (is a cat's game or someone won)
then you may play anywhere.

the game is won by the winner of the big board.
"""

from __future__ import annotations
import random
import turtle
import tkinter  # pylint: disable=unused-import


WIDTH = 800
HEIGHT = 800
SIZE = min(WIDTH, HEIGHT)
BOARD_SIZE = 3
LINE_WIDTH_THIN = 2  # used for drawing the boards
LINE_WIDTH_THICK = 10  # used for drawing the Xs and Os
PEN_COLOR = "black"
X_COLOR = "red2"
O_COLOR = "blue"
CELL_OFFSET_FACTOR = 0.9
BOARD_OFFSET_FACTOR = 0.9
OUTER_BOARD_OFFSET_FACTOR = 0.9

DEBUG_SHOW_HITBOXES = False
DEBUG_SHOW_TURTLE = False

# print(dir(screen._canvas))

random.seed("woo")


class Window:
    """contains functions to draw stuff to the screen"""

    screen: turtle._Screen
    pen: turtle.Turtle
    game_state: GameState

    def __init__(self, game_state) -> None:

        self.game_state = game_state

        self.screen = turtle.Screen()
        self.screen.setup(width=WIDTH, height=HEIGHT)
        # screen.screensize(canvwidth=int(width), canvheight=int(height),bg='red')
        self.screen.screensize(bg="lightgray")

        self.pen = turtle.Turtle()
        self.pen.color(PEN_COLOR)

        self.pen.penup()
        self.pen.speed(0)  # disable anamiations for the turtle
        self.pen.pensize(2)  # defualt pensize

        if not DEBUG_SHOW_TURTLE:
            self.screen.tracer(0, 0)  # disable updating to to screen automaticly
            # use screen.update() to update the screen

            self.pen.hideturtle()

    def create_window_hitbox(self) -> dict[int]:
        """create the hitbox for the top level board"""
        size = SIZE / 2
        hitbox = dict(
            e=+size,
            w=-size,
            n=+size,
            s=-size,
            size=2 * size,
        )
        print("here")

        hitbox = Board.shrink_hitbox(None, hitbox, OUTER_BOARD_OFFSET_FACTOR)

        return hitbox

    def outline_hitbox(self, hitbox) -> None:
        """debug function to outline a hitbox"""

        self.pen.color("purple")
        self.pen.goto(hitbox["w"], hitbox["s"])
        self.pen.pendown()

        self.pen.goto(hitbox["w"], hitbox["n"])
        self.pen.goto(hitbox["e"], hitbox["n"])
        self.pen.goto(hitbox["e"], hitbox["s"])
        self.pen.goto(hitbox["w"], hitbox["s"])

        self.pen.penup()
        self.pen.color(PEN_COLOR)

    def draw_point(self, location) -> None:
        """draw a point at location"""
        self.pen.goto(location)
        self.pen.dot(LINE_WIDTH_THICK)

    def center_size_to_hitbox(self, center, size) -> dict[int]:
        """take a center and size and return a hitbox"""
        hitbox = dict(
            e=center[0] + size / 2,
            w=center[0] - size / 2,
            n=center[1] + size / 2,
            s=center[1] - size / 2,
            size=size,
        )

        # self.outline_hitbox(hitbox)

        # self.draw_point([hitbox['w'], hitbox['s']])
        # self.draw_point([hitbox['e'], hitbox['n']])

        return hitbox

    def draw_grid(self, hitbox, board_size) -> None:
        "draw the grid for the playfield"

        # hitbox = self.center_size_to_hitbox(center, size)

        gap_width = hitbox["size"] / board_size

        # draw horisantal lines
        for i in range(1, board_size):

            self.pen.goto(hitbox["w"], hitbox["s"] + i * gap_width)
            self.pen.down()

            self.pen.goto(hitbox["e"], hitbox["s"] + i * gap_width)
            self.pen.up()

        # draw horisantal lines
        for i in range(1, board_size):

            self.pen.goto(hitbox["w"] + i * gap_width, hitbox["s"])
            self.pen.down()

            self.pen.goto(hitbox["w"] + i * gap_width, hitbox["n"])
            self.pen.up()

    def draw_x(self, hitbox) -> None:
        """draw a single x of size (size)"""

        # hitbox = self.center_size_to_hitbox(center, size)

        color = X_COLOR
        offset = LINE_WIDTH_THICK / 2

        self.pen.pensize(LINE_WIDTH_THICK)
        self.pen.color(color)

        self.pen.goto(hitbox["w"] + offset, hitbox["s"] + offset)
        self.pen.down()
        self.pen.goto(hitbox["e"] - offset, hitbox["n"] - offset)
        self.pen.up()

        self.pen.goto(hitbox["w"] + offset, hitbox["n"] - offset)
        self.pen.down()
        self.pen.goto(hitbox["e"] - offset, hitbox["s"] + offset)
        self.pen.up()

        self.pen.pensize(LINE_WIDTH_THIN)
        self.pen.color(PEN_COLOR)

    def draw_o(self, hitbox) -> None:
        """draw a single O of size size"""

        # hitbox = self.center_size_to_hitbox(center, size)

        color = O_COLOR

        radius = hitbox["size"] / 2 - LINE_WIDTH_THICK / 2

        self.pen.pensize(LINE_WIDTH_THICK)
        self.pen.color(color)

        self.pen.goto(
            hitbox["w"] + hitbox["size"] / 2,
            hitbox["s"] + LINE_WIDTH_THICK / 2,
        )

        self.pen.down()
        self.pen.circle(radius)
        self.pen.up()

        self.pen.pensize(LINE_WIDTH_THIN)
        self.pen.color(PEN_COLOR)

    def draw_board(self, board: Board) -> None:
        """Print the board 'board'"""

        self.draw_grid(board.hitbox, board.board_size)

        for cell in board.get_all_cells():

            if cell.owner == "X":
                self.draw_x(cell.hitbox)
            elif cell.owner == "O":
                self.draw_o(cell.hitbox)
            elif isinstance(cell, Board):
                self.draw_board(cell)

        # update the screen with the new board
        # needed because of the tracer command at the top
        # self.screen.update()

    def draw_all(self) -> None:
        """draw everything"""

        game_state = self.game_state

        board = game_state.board

        game_state.window.draw_board(board)

        game_state.window.screen.update()
        turtle.done()


class Cell:
    """contains information and mothods for a single cell, including managing its hitbox"""

    hitbox: dict
    owner = "*"
    # parent: Board | None
    game_state: GameState
    location: None | tuple[int]

    def __init__(self, game_state, hitbox, location) -> None:

        self.game_state = game_state
        self.hitbox = self.validate_hitbox(hitbox)
        self.location = location

        if DEBUG_SHOW_HITBOXES:
            self.game_state.window.outline_hitbox(hitbox)

        symbols = ["X", "O", "*"]
        self.owner = random.choice(symbols)

    # def __str__(self) -> str:
    #     return 'A cell'

    # def in_hitbox(self,location):
    #     '''return true if the given location is inside the hitbox for this object'''
    #     if location[0] > self.bottom_right[0] \
    #             and location[1] > self.bottom_right[1] \
    #             and location[0] < self.top_left[0] \
    #             and location[1] < self.top_left[1]:
    #         return True
    #     else:
    #         return False

    def validate_hitbox(self, hitbox: dict) -> dict[int]:
        """validate a hitbox is not malformed then return it, error otherwise"""

        # check all members exist
        assert "e" in hitbox, "hitbox does not have member 'e' (for east)"
        assert "w" in hitbox, "hitbox does not have member 'w' (for west)"
        assert "n" in hitbox, "hitbox does not have member 'n' (for north)"
        assert "s" in hitbox, "hitbox does not have member 's' (for south)"
        assert "size" in hitbox, "hitbox does not have member 'size'"

        # check all members are numberic
        # the "" at the end of the messages are required for black to auto format it properly
        assert isinstance(hitbox["e"], (int, float)), (
            "hitbox member 'e' (for east) is not numeric" ""
        )
        assert isinstance(hitbox["w"], (int, float)), (
            "hitbox member 'w' (for west) is not numeric" ""
        )
        assert isinstance(hitbox["n"], (int, float)), (
            "hitbox member 'n' (for north) is not numeric" ""
        )
        assert isinstance(hitbox["s"], (int, float)), (
            "hitbox member 's' (for south) is not numeric" ""
        )
        assert isinstance(hitbox["size"], (int, float)), (
            "hitbox member 'size' is not numeric" ""
        )

        # check there is nothing extra
        assert len(hitbox) == 5, "hitbox has too many items"

        # check the size member is accuret
        # checks if they are within elsilon to avoid floating point errors
        epislon = 0.001
        assert (
            abs((hitbox["e"] - hitbox["w"]) - (hitbox["n"] - hitbox["s"])) < epislon
        ), "hitbox is not square"
        assert (
            abs(hitbox["size"] - (hitbox["e"] - hitbox["w"])) < epislon
        ), "hitbox 'size' field does not match the real size of the hitbox"

        return hitbox

    def shrink_hitbox(self, old_hitbox: dict[int], shrink_factor) -> dict[int]:
        """shrink a hitbox by shrink_factor so it remains centered"""

        center_x = (old_hitbox["w"] + old_hitbox["e"]) / 2
        center_y = (old_hitbox["n"] + old_hitbox["s"]) / 2

        new_size = old_hitbox["size"] * shrink_factor

        new_hitbox = dict(
            e=center_x + new_size / 2,
            w=center_x - new_size / 2,
            n=center_y + new_size / 2,
            s=center_y - new_size / 2,
            size=new_size,
        )

        # self.outline_hitbox(new_hitbox)
        # self.draw_point([new_hitbox["w"], new_hitbox["s"]])
        # self.draw_point([old_hitbox["w"], old_hitbox["s"]])

        return new_hitbox

    def divide_hitbox(
        self, x, y, shrink_factor  # pylint: disable=invalid-name
    ) -> dict[int]:
        """find the hitbox of a smaller board at x,y"""

        old_hitbox = self.hitbox
        board_size = self.game_state.board_size
        stride = old_hitbox["size"] / board_size

        hitbox = dict(
            w=old_hitbox["w"] + x * stride,
            e=old_hitbox["w"] + (x + 1) * stride,
            s=old_hitbox["s"] + y * stride,
            n=old_hitbox["s"] + (y + 1) * stride,
            size=old_hitbox["size"] / board_size,
        )
        hitbox = self.shrink_hitbox(hitbox, shrink_factor)

        return hitbox


class Board(Cell):
    """a the game logic of a game board or a single sub board"""

    # a square array of boards obects
    cell_array: list[list[Board]]
    board_size: int
    is_top: bool

    def __init__(self, game_state, hitbox, location, board_size, is_top) -> None:
        Cell.__init__(self, game_state, hitbox, location)
        # ,top_left,bottom_right
        self.board_size = board_size
        self.is_top = is_top

        self.cell_array = []
        for x in range(board_size):  # pylint: disable=invalid-name
            self.cell_array.append([])
            for y in range(board_size):  # pylint: disable=invalid-name
                if is_top:
                    self.cell_array[x].append(
                        Board(
                            game_state,
                            self.divide_hitbox(x, y, BOARD_OFFSET_FACTOR),
                            (x, y),
                            board_size,
                            False,
                        )
                    )
                else:
                    self.cell_array[x].append(
                        Cell(
                            game_state,
                            self.divide_hitbox(x, y, CELL_OFFSET_FACTOR),
                            (x, y),
                        )
                    )

    # def __str__(self) -> str:
    #     if self.is_top:
    #         return 'The top board'
    #     else:
    #         return 'A suboard'

    def get_cell(self, x, y) -> Board:  # pylint: disable=invalid-name
        """get the cell located at x,y"""
        return self.cell_array[x][y]

    def get_all_cells(self) -> list[Board]:
        """get all cells in this board"""

        cell_list = []
        for sub_list in self.cell_array:
            cell_list += sub_list

        return cell_list


class GameState:
    """contains full data for gamedata"""

    board_size = BOARD_SIZE
    board: Board
    window: Window
    player = "X"

    def __init__(self) -> None:

        self.window = Window(self)

        self.board = Board(
            self, self.window.create_window_hitbox(), None, self.board_size, True
        )
        self.player = "X"

    def draw(self) -> None:
        """draw gameboard as it exists now"""
        self.window.draw_all()


def main() -> None:
    "main"

    # write_header()

    game_state = GameState()

    game_state.draw()


if __name__ == "__main__":
    main()
