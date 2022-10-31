'''A 2 player game of Tick Tac Tick Tac Toe

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
'''

import random
import turtle
import numpy as np


WIDTH = 800
HEIGHT = 800
SIZE = min(WIDTH,HEIGHT)
BOARD_SIZE = 3
LINE_WIDTH_THIN = 2 # used for drawing the boards
# LINE_WIDTH_THICK = 20 # used for drawing the Xs and Os
LINE_WIDTH_THICK = 10 # used for drawing the Xs and Os
PEN_COLOR = 'BLACK'
X_COLOR = 'red'
O_COLOR = 'blue'

# TODO_: change game_data from a dictonary to an object and add screen and pen to the object

screen = turtle.Screen()
screen.setup(width=WIDTH,height=HEIGHT)
# screen.screensize(canvwidth=int(width), canvheight=int(height),bg='red')
screen.screensize(bg='lightgray')

pen = turtle.Turtle()
pen.color(PEN_COLOR)

pen.penup()
pen.speed(0) # disable anamiations for the turtle
pen.pensize(2) # defualt pensize
screen.tracer(0,0) # disable updating to to screen automaticly
# use screen.update() to update the screen

pen.hideturtle()

# class Cell:
#     '''contains information about an object hitbox'''

#     top_left: np.array # top left point of the cell hitbox
#     bottom_right: np.array # bottom right point of the cell hitbox
#     owner = "*"

#     def __init__(self,top_left,bottom_right) -> None:
#         self.top_left = top_left
#         self.bottom_right = bottom_right
#         self.owner = ""

#     def in_hitbox(self,location):
#         '''return true if the given location is inside the hitbox for this object'''
#         if location[0] > self.bottom_right[0] \
#                 and location[1] > self.bottom_right[1] \
#                 and location[0] < self.top_left[0] \
#                 and location[1] < self.top_left[1]:
#             return True
#         else:
#             return False

# class Board(Cell):
#     '''a single game board or sub board'''

#     # a square array of boards obects
#     board = []

#     def __init__(self) -> None:
#         self.board = []




def write_header():
    'write header to consle'

    rules = '''A 2 player game of Tick Tac Tick Tac Toe

Game is played on a 3x3 grid of 3x3 playfields.
Each 3x3 grid acts like a game of tick tac toe.

the spaces of the outer board belong to the winner of the inner board

You must play on the inner board corsponding to the
location of the prevous player's move on their board.

If the designated board is complete (is a cat's game or someone won)
then you may play anywhere.

the game is won by the winner of the big board.
'''
    print(rules)

# section of code for all the drawing functions

def draw_grid(center, size, board_size):
    'draw the grid for the playfield'

    # np arrays are used to allow addition like vectors, instead of concation like lists
    # vector in the +x direction
    x_vector = np.array([1,0])
    # vector in the +y direction
    y_vector = np.array([0,1])

    gap_width = size / board_size

    # draw horisantal lines
    for i in range(1,board_size):
        # start at the center, go to the bottom right corner, go up by gap_width each loop
        pen.goto(center - 0.5*size*x_vector - 0.5*size*y_vector + i*gap_width*y_vector)
        pen.down() # start drawing
        # similar to above
        pen.goto(center + 0.5*size*x_vector - 0.5*size*y_vector + i*gap_width*y_vector)
        pen.up() # stop drawing

    # draw vertical lines
    for i in range(1,board_size):
        # start at the center, go to the bottom right corner, go left by gap_width each loop
        pen.goto(center - 0.5*size*x_vector - 0.5*size*y_vector + i*gap_width*x_vector)
        pen.down() # start drawing
        # similar to above
        pen.goto(center - 0.5*size*x_vector + 0.5*size*y_vector + i*gap_width*x_vector)
        pen.up() # stop drawing

def draw_x(center, size):
    '''draw a single x of size size'''

    color = X_COLOR

    distance = size /2 - LINE_WIDTH_THICK/2

    # np arrays are used to allow addition like vectors, instead of concation like lists
    # vector in the +x direction
    ne_vector = np.array([1,1])
    # vector in the +y direction
    se_vector = np.array([1,-1])

    pen.pensize(LINE_WIDTH_THICK)
    pen.color(color)

    pen.goto(center + distance * ne_vector)
    pen.down()
    pen.goto(center - distance * ne_vector)
    pen.up()

    pen.goto(center + distance * se_vector)
    pen.down()
    pen.goto(center - distance * se_vector)
    pen.up()

    pen.pensize(LINE_WIDTH_THIN)
    pen.color(PEN_COLOR)

def draw_o(center, size):
    '''draw a single O of size size'''

    color = O_COLOR

    radius = size /2 - LINE_WIDTH_THICK/2

    # np arrays are used to allow addition like vectors, instead of concation like lists
    # vector in the +x direction
    # x_vector = np.array([1,0])
    # vector in the +y direction
    y_vector = np.array([0,1])

    pen.pensize(LINE_WIDTH_THICK)
    pen.color(color)

    pen.goto(center - radius * y_vector)
    pen.down()
    pen.circle(radius)
    pen.up()

    pen.pensize(LINE_WIDTH_THIN)
    pen.color(PEN_COLOR)



def draw_board(board, center= np.array([0,0]), size = SIZE*0.9):
    '''Print the current board. Board is a square 2d list whose elements may be other boards or \
X,O,*. Center is the location of the center of the board as a numpy array, size is the distance \
from the one edge to the other edge of the board'''

    # note: all boards are square

    board_size = len(board)
    cell_size = size/board_size*0.9 # size to draw the contents of a cell
    cell_stride = size/board_size # distance from center of 1 cell to center of next cell

    lesser_board_size = size/board_size*0.8

    # np arrays are used to allow addition like vectors, instead of concation like lists
    # vector in the +x direction
    x_vector = np.array([1,0])
    # vector in the +y direction
    y_vector = np.array([0,1])

    sw_corrner = center - 0.5 * size * x_vector - 0.5 * size * y_vector


    draw_grid(center,size,board_size)
    # draw_o(center + cell_stride * x_vector, cell_size)

    i = 1
    j = 2


    for i in range(board_size):
        for j in range(board_size):

            location = sw_corrner \
                + (i + 0.5) * cell_stride * x_vector \
                + (j + 0.5) * cell_stride * y_vector

            cell = board[i][j]

            if cell == 'X':
                draw_x(location, cell_size)
            elif cell == 'O':
                draw_o(location, cell_size)
            elif isinstance(cell,list):
                draw_board(cell,location,lesser_board_size)


    # update the screen with the new board
    # needed because of the tracer command at the top
    # screen.update()


def create_one_board(board_size):
    'make 1 board from cell function'

    symbols = ['X','O','*']
    # symbols = ['X']
    board = [[[[random.choice(symbols) for _ in range(board_size)] \
        for _ in range(board_size)] \
        for _ in range(board_size)] \
        for _ in range(board_size)]

    # board[1][2] = 'X'
    # board[2][2] = 'O'

    return board

def create_gamestate():
    'initilise all nessary game data'

    board_size = BOARD_SIZE

    # TODO_: change game_data from a dictonary to an object
    game_data = {}

    # [pen,screen] = create_canvas()

    # game_data['pen'] = pen
    # game_data['screen'] = screen
    game_data['board_size'] = board_size

    game_data['board'] = create_one_board(board_size)
    game_data['player'] = 1


    return game_data



def main():
    'main'

    write_header()

    game_data = create_gamestate()

    board = game_data['board']

    draw_board(board)

    screen.update()
    turtle.done()


main()
