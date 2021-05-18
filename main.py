from graphics2 import *


import random
import time
import math
import operator

from button import Button

from game_constants import *
from piece import Piece


def createGameWindow(name):
    window = GraphWin(name, WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setCoords(0, 8, 8, 0)

    return window


def drawInitialBoard(window):
    for row in range(0, 8):
        for col in range(0, 8):
            rectangle = Rectangle(Point(row, col), Point(row + 1, col + 1))
            rectangle.setFill(
                color_rgb(240, 217, 181)
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0)
                else color_rgb(181, 136, 99)
            )
            rectangle.setOutline(
                color_rgb(240, 217, 181)
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0)
                else color_rgb(181, 136, 99)
            )
            rectangle.draw(window)

def findNode(clickPt, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)

def getUserSelectedInput(window, gameGrid, selected):
    clickPt = window.getMouse()
    colX,rowY = int(clickPt.getX()),int(clickPt.getY())
    x, y = findNode()

starting_order = {
    (0, 0): Piece("b", "r", "assets/pieces/br.png", Point(0, 0)),
    (1, 0): Piece("b", "n", "assets/pieces/bn.png", Point(1, 0)),
    (2, 0): Piece("b", "b", "assets/pieces/bb.png", Point(2, 0)),
    (3, 0): Piece("b", "k", "assets/pieces/bk.png", Point(3, 0)),
    (4, 0): Piece("b", "q", "assets/pieces/bq.png", Point(4, 0)),
    (5, 0): Piece("b", "b", "assets/pieces/bb.png", Point(5, 0)),
    (6, 0): Piece("b", "n", "assets/pieces/bn.png", Point(6, 0)),
    (7, 0): Piece("b", "r", "assets/pieces/br.png", Point(7, 0)),
    (0, 1): Piece("b", "p", "assets/pieces/bp.png", Point(0, 1)),
    (1, 1): Piece("b", "p", "assets/pieces/bp.png", Point(1, 1)),
    (2, 1): Piece("b", "p", "assets/pieces/bp.png", Point(2, 1)),
    (3, 1): Piece("b", "p", "assets/pieces/bp.png", Point(3, 1)),
    (4, 1): Piece("b", "p", "assets/pieces/bp.png", Point(4, 1)),
    (5, 1): Piece("b", "p", "assets/pieces/bp.png", Point(5, 1)),
    (6, 1): Piece("b", "p", "assets/pieces/bp.png", Point(6, 1)),
    (7, 1): Piece("b", "p", "assets/pieces/bp.png", Point(7, 1)),
    (0, 2): None,
    (1, 2): None,
    (2, 2): None,
    (3, 2): None,
    (4, 2): None,
    (5, 2): None,
    (6, 2): None,
    (7, 2): None,
    (0, 3): None,
    (1, 3): None,
    (2, 3): None,
    (3, 3): None,
    (4, 3): None,
    (5, 3): None,
    (6, 3): None,
    (7, 3): None,
    (0, 4): None,
    (1, 4): None,
    (2, 4): None,
    (3, 4): None,
    (4, 4): None,
    (5, 4): None,
    (6, 4): None,
    (7, 4): None,
    (0, 5): None,
    (1, 5): None,
    (2, 5): None,
    (3, 5): None,
    (4, 5): None,
    (5, 5): None,
    (6, 5): None,
    (7, 5): None,
    (0, 6): Piece("w", "p", "assets/pieces/wp.png", Point(0, 6)),
    (1, 6): Piece("w", "p", "assets/pieces/wp.png", Point(1, 6)),
    (2, 6): Piece("w", "p", "assets/pieces/wp.png", Point(2, 6)),
    (3, 6): Piece("w", "p", "assets/pieces/wp.png", Point(3, 6)),
    (4, 6): Piece("w", "p", "assets/pieces/wp.png", Point(4, 6)),
    (5, 6): Piece("w", "p", "assets/pieces/wp.png", Point(5, 6)),
    (6, 6): Piece("w", "p", "assets/pieces/wp.png", Point(6, 6)),
    (7, 6): Piece("w", "p", "assets/pieces/wp.png", Point(7, 6)),
    (0, 7): Piece("w", "r", "assets/pieces/wr.png", Point(0, 7)),
    (1, 7): Piece("w", "n", "assets/pieces/wn.png", Point(1, 7)),
    (2, 7): Piece("w", "b", "assets/pieces/wb.png", Point(2, 7)),
    (3, 7): Piece("w", "k", "assets/pieces/wk.png", Point(3, 7)),
    (4, 7): Piece("w", "q", "assets/pieces/wq.png", Point(4, 7)),
    (5, 7): Piece("w", "b", "assets/pieces/wb.png", Point(5, 7)),
    (6, 7): Piece("w", "n", "assets/pieces/wn.png", Point(6, 7)),
    (7, 7): Piece("w", "r", "assets/pieces/wr.png", Point(7, 7)),
}


def create_board(board):
    board[0] = [
        Piece("b", "r", "assets/pieces/br.png", Point(0, 0)),
        Piece("b", "n", "assets/pieces/bn.png", Point(1, 0)),
        Piece("b", "b", "assets/pieces/bb.png", Point(2, 0)),
        Piece("b", "k", "assets/pieces/bk.png", Point(3, 0)),
        Piece("b", "q", "assets/pieces/bq.png", Point(4, 0)),
        Piece("b", "b", "assets/pieces/bb.png", Point(5, 0)),
        Piece("b", "n", "assets/pieces/bn.png", Point(6, 0)),
        Piece("b", "r", "assets/pieces/br.png", Point(7, 0)),
    ]

    board[7] = [
        Piece("w", "r", "assets/pieces/wr.png", Point(0, 7)),
        Piece("w", "n", "assets/pieces/wn.png", Point(1, 7)),
        Piece("w", "b", "assets/pieces/wb.png", Point(2, 7)),
        Piece("w", "k", "assets/pieces/wk.png", Point(3, 7)),
        Piece("w", "q", "assets/pieces/wq.png", Point(4, 7)),
        Piece("w", "b", "assets/pieces/wb.png", Point(5, 7)),
        Piece("w", "n", "assets/pieces/wn.png", Point(6, 7)),
        Piece("w", "r", "assets/pieces/wr.png", Point(7, 7)),
    ]

    for i in range(8):
        board[1][i] = Piece("b", "p", "assets/pieces/bp.png", Point(i, 1))
        board[6][i] = Piece("w", "p", "assets/pieces/wp.png", Point(i, 6))
    return board


def main():

    board = [["  " for i in range(8)] for i in range(8)]
    moves = 0

    window = createGameWindow()
    createGameWindow("Chess")
    draw_board()


if __name__ == "__main__":
    main()
