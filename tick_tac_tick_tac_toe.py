"""
A 2 player game of Tick Tac Tick Tac Toe

Project Name: Tick Tac Tick Tac Toe
Author: Lincoln Chamberlin
Created: 8/2022

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
import time  # pylint: disable=unused-import
import tkinter  # pylint: disable=unused-import
import turtle

SIZE = 600
WIDTH = SIZE
HEIGHT = SIZE
# SIZE = min(WIDTH, HEIGHT)
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
# DEBUG_SHOW_HITBOXES = True
DEBUG_SHOW_TURTLE = False
# DEBUG_SHOW_TURTLE = True

# print(dir(screen._canvas))

# random.seed("woo")


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

        self.screen.onscreenclick(self.on_mouse_click)

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

    def on_mouse_click(self, x, y) -> None:  # pylint: disable=invalid-name
        """called when the user clicks on the screen"""

        # time.sleep(1)

        # self.draw_point([x, y])
        self.game_state.game_loop((x, y))


class Cell:
    """contains information and mothods for a single cell, including managing its hitbox"""

    hitbox: dict
    owner = "*"
    parent: Board | None
    game_state: GameState
    location: None | tuple[int]

    def __init__(self, game_state, parent, hitbox, location) -> None:

        self.game_state = game_state
        self.parent = parent
        self.hitbox = self.validate_hitbox(hitbox)
        self.location = location

        if DEBUG_SHOW_HITBOXES:
            self.game_state.window.outline_hitbox(hitbox)

        # symbols = ["X", "O", "*"]
        # self.owner = random.choice(symbols)
        self.owner = random.choice("*")

    def __str__(self) -> str:
        return f"Cell {self.location} in board {self.parent.location} is a {self.owner}"

    def __repr__(self) -> str:
        return str(self)

    def apply_owner(self, new_owner) -> bool:
        """
        apply owner to this cell, return True if sucsesful return False if cell was already full"""
        if self.owner == "*":
            self.owner = new_owner
            return True
        else:
            return False

    def is_playable(self) -> bool:
        """return true if a move can be played, return false if there is no leagal move"""

        return self.owner == "*"

    # hitbox utilities
    def in_hitbox(self, location) -> bool:
        """return true if the given location is inside the hitbox for this object"""
        if (
            location[0] > self.hitbox["w"]
            and location[0] < self.hitbox["e"]
            and location[1] > self.hitbox["s"]
            and location[1] < self.hitbox["n"]
        ):
            return True
        else:
            return False

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

    def __init__(
        self, game_state, parent, hitbox, location, board_size, is_top
    ) -> None:
        Cell.__init__(self, game_state, parent, hitbox, location)
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
                            self,
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
                            self,
                            self.divide_hitbox(x, y, CELL_OFFSET_FACTOR),
                            (x, y),
                        )
                    )

    def __str__(self) -> str:
        if self.is_top:
            return "The top board"
        else:
            return f"Subboard {self.location}"

    def get_cell(self, x, y) -> Board:  # pylint: disable=invalid-name
        """get the cell located at x,y"""
        return self.cell_array[x][y]

    def get_all_cells(self) -> list[Board]:
        """get all cells in this board"""

        cell_list = []
        for sub_list in self.cell_array:
            cell_list += sub_list

        return cell_list

    def is_playable(self) -> bool:
        """return true if a move can be played, return false if there is no leagal move"""

        if self.owner != "*":
            return False

        # make sure there is at least one playable cell
        playable = False
        for cell in self.get_all_cells():
            if cell.is_playable():
                playable = True

        return playable

    def get_clicked_board(self, location) -> Board | None:
        """take in a location and return the either a Cell or None"""

        if self.owner != "*":
            return None
            # pass

        for cell in self.get_all_cells():
            if cell.in_hitbox(location):
                return cell

        return None

    def all_same_owner(self, cell_list: list[Cell]) -> str | None:
        """if all elements are the same then it will return that, otherwise return None"""

        owner = cell_list[0].owner
        if owner == "*":
            return None

        for cell in cell_list:

            # print(cell)
            if cell.owner != owner:
                return None

        return owner

    def find_board_winner(self) -> str | None:
        """find the winner if the game"""

        # print("here at find_board_winner")

        if self.owner != "*":
            return self.owner

        cell_array = self.cell_array

        winner = None
        # test rows
        for row in cell_array:
            # is there a winner for this row, if so the board is theirs
            winner = self.all_same_owner(row) or winner

        # test columns
        for column in zip(*cell_array):
            # is there a winner for this row, if so the board is theirs
            winner = self.all_same_owner(column) or winner

        # test diagonals
        diagonal1 = []
        diagonal2 = []
        for i in range(len(cell_array)):  # pylint: disable=consider-using-enumerate
            diagonal1 += [cell_array[i][i]]
            diagonal2 += [cell_array[i][len(cell_array) - i - 1]]

        # is there a winner for this row, if so the board is theirs
        winner = self.all_same_owner(diagonal1) or winner
        winner = self.all_same_owner(diagonal2) or winner

        # print("winner", winner)
        return winner

    def apply_board_winner(self) -> str | None:
        """find and apply the winner of the board"""

        # print(self)

        winner = self.find_board_winner()

        if winner:
            self.owner = winner
        return winner


class GameState:
    """contains full data for gamedata"""

    board_size = BOARD_SIZE
    board: Board
    window: Window
    playable_subboard: tuple[int] | None
    player = "X"

    def __init__(self) -> None:

        self.window = Window(self)

        self.board = Board(
            self, None, self.window.create_window_hitbox(), None, self.board_size, True
        )

        self.playable_subboard = (1, 2)
        self.player = "X"

    def draw(self) -> None:
        """draw gameboard as it exists now"""
        self.window.draw_all()

    def swap_player(self) -> str:
        """swap the player between X and O"""
        if self.player == "X":
            self.player = "O"
        else:
            self.player = "X"

        return self.player

    def check_legal_subboard(self, subboard: Board) -> bool:
        """
        check if the clicked subboard is a legal move, return True if it is and False otherwise"""

        if self.playable_subboard is None:
            return True
        return subboard.location == self.playable_subboard

    def update_legal_subboard(self, cell: Cell) -> None:
        """update where the next subboard is allowed"""

        location = cell.location
        next_subboard = self.board.cell_array[location[0]][location[1]]
        if next_subboard.is_playable():
            self.playable_subboard = location
        else:
            self.playable_subboard = None

    def game_loop(self, location) -> None:  # pylint: disable=invalid-name
        """called when the user clicks on the screen"""

        try:
            # determine if the player clicked something
            subboard = self.board.get_clicked_board(location)
            if not self.check_legal_subboard(subboard):
                raise AttributeError
            cell = subboard.get_clicked_board(location)
            if cell.owner != "*":
                # raise Exception("ExistingOwner")
                raise AttributeError
        except AttributeError:
            # attribute error will occer if either there is no cell at the click location
            # the first raise will occer if the chosen subboard is not leagal
            # the 2nd raise will occer if there is alreadly a piece at that loction
            return
        # if the cell was placed, then swap the players

        cell.apply_owner(self.player)
        self.swap_player()

        self.draw()

        # print("draw1")
        # if the sub board has a winner, wait 1 sec then draw it
        if subboard.apply_board_winner():
            # print("redrawing")
            time.sleep(1)
            self.draw()

            # if self.board.apply_board_winner():
            #     time.sleep(1)
            #     self.draw()

        self.update_legal_subboard(cell)


def main() -> None:
    "main"

    game_state = GameState()

    game_state.draw()

    turtle.done()


if __name__ == "__main__":
    main()
